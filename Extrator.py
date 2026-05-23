# ============================================================
#  PROJETO DETECTIVE — extrator.py
#  Responsabilidade: receber o HTML coletado pelo coletor.py
#  e extrair os dados do concorrente usando BeautifulSoup.
#
#  Biblioteca usada: BeautifulSoup4
#
#  Dados extraídos:
#    - Título do produto
#    - Preço atual (com desconto, se houver)
#    - Preço original (se houver desconto)
#    - Percentual de desconto
#    - Frete grátis (sim/não)
#    - Estoque disponível
#    - Avaliações (quantidade)
#    - Vendas (+X vendidos)
# ============================================================

from bs4 import BeautifulSoup
import re


# ─────────────────────────────────────────────────────────────
# FUNÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────

def extrair_dados(html):
    """
    Recebe o HTML da página do concorrente e retorna
    um dicionário com todos os dados extraídos.

    Parâmetros:
        html (str): HTML completo retornado pelo coletor.py

    Retorna:
        dict: dicionário com os dados do concorrente,
              ou None se o HTML for inválido
    """

    if not html:
        print("[EXTRATOR] ❌ HTML vazio ou inválido.")
        return None

    print("[EXTRATOR] Iniciando extração com BeautifulSoup...")
    soup = BeautifulSoup(html, "html.parser")
    dados = {}

    # ── 1. TÍTULO ─────────────────────────────────────────────
    try:
        titulo = soup.find(class_="ui-pdp-title")
        dados["titulo"] = titulo.text.strip() if titulo else "Não encontrado"
    except:
        dados["titulo"] = "Erro"
    print(f"[EXTRATOR] Título    : {dados['titulo']}")

    # ── 2. PREÇO ATUAL (com desconto se houver) ───────────────
    # ui-pdp-price__second-line → preço real que o cliente paga
    # ui-pdp-price__original-value → preço original riscado
    try:
        preco_box = soup.find("div", class_="ui-pdp-price__second-line")
        if preco_box:
            fracao   = preco_box.find(class_="andes-money-amount__fraction")
            centavos = preco_box.find(class_="andes-money-amount__cents")
            valor = fracao.text.strip() if fracao else "0"
            cents = centavos.text.strip() if centavos else "00"
            dados["preco"] = float(f"{valor}.{cents}".replace(",", ""))
        else:
            fracao = soup.find(class_="andes-money-amount__fraction")
            dados["preco"] = float(fracao.text.strip()) if fracao else 0.0
    except:
        dados["preco"] = 0.0
    print(f"[EXTRATOR] Preço     : R$ {dados['preco']:.2f}")

    # ── 3. PREÇO ORIGINAL (riscado) ───────────────────────────
    try:
        original_box = soup.find("div", class_="ui-pdp-price__original-value")
        if original_box:
            fracao_orig = original_box.find(class_="andes-money-amount__fraction")
            dados["preco_original"] = float(fracao_orig.text.strip()) if fracao_orig else None
        else:
            dados["preco_original"] = None
    except:
        dados["preco_original"] = None
    print(f"[EXTRATOR] Preço orig: R$ {dados['preco_original']}")

    # ── 4. DESCONTO ───────────────────────────────────────────
    try:
        desconto = soup.find(class_="andes-money-amount__discount")
        dados["desconto"] = desconto.text.strip() if desconto else "Sem desconto"
    except:
        dados["desconto"] = "Sem desconto"
    print(f"[EXTRATOR] Desconto  : {dados['desconto']}")

    # ── 5. FRETE GRÁTIS ───────────────────────────────────────
    try:
        frete_box = soup.find(class_="ui-pdp-shipping")
        if frete_box:
            texto_frete = frete_box.text.strip().lower()
            dados["frete_gratis"] = "grátis" in texto_frete or "gratis" in texto_frete
            dados["frete_texto"] = frete_box.text.strip()[:80]
        else:
            dados["frete_gratis"] = False
            dados["frete_texto"] = "Não informado"
    except:
        dados["frete_gratis"] = False
        dados["frete_texto"] = "Erro"
    icone = "✅" if dados["frete_gratis"] else "❌"
    print(f"[EXTRATOR] Frete gr. : {icone} {dados['frete_texto'][:50]}")

    # ── 6. ESTOQUE ────────────────────────────────────────────
    # Seletor: ui-pdp-buybox__quantity
    # Retorna texto como: "Quantidade: 1 unidade (+25 disponíveis)"
    # Extraímos o número de unidades disponíveis com regex.
    #
    # Por que isso importa?
    # Se o estoque zerar → você é o único vendedor → pode subir o preço.
    # Lei da oferta e da procura aplicada em tempo real!
    try:
        estoque_box = soup.find(class_="ui-pdp-buybox__quantity")
        if estoque_box:
            texto_estoque = estoque_box.text.strip()
            dados["estoque_texto"] = texto_estoque

            # Extrai o número de disponíveis com regex
            # Exemplos: "+25 disponíveis", "1 disponível", "Último disponível"
            match = re.search(r'\+?(\d+)\s+disponív', texto_estoque, re.IGNORECASE)
            if match:
                dados["estoque"] = int(match.group(1))
            elif "último" in texto_estoque.lower():
                dados["estoque"] = 1
            else:
                dados["estoque"] = None
        else:
            dados["estoque"] = None
            dados["estoque_texto"] = "Não informado"
    except:
        dados["estoque"] = None
        dados["estoque_texto"] = "Erro"
    print(f"[EXTRATOR] Estoque   : {dados['estoque_texto']}")

    # ── 7. AVALIAÇÕES ─────────────────────────────────────────
    try:
        avaliacoes = soup.find(class_="ui-pdp-review__amount")
        if avaliacoes:
            dados["avaliacoes"] = int(
                avaliacoes.text.strip().replace("(", "").replace(")", "")
            )
        else:
            dados["avaliacoes"] = 0
    except:
        dados["avaliacoes"] = 0
    print(f"[EXTRATOR] Avaliações: {dados['avaliacoes']}")

    # ── 8. VENDAS ─────────────────────────────────────────────
    try:
        vendas = soup.find(class_="ui-pdp-subtitle")
        dados["vendas"] = vendas.text.strip() if vendas else "Não informado"
    except:
        dados["vendas"] = "Não informado"
    print(f"[EXTRATOR] Vendas    : {dados['vendas']}")

    print("[EXTRATOR] ✅ Extração concluída!")
    return dados


# ─────────────────────────────────────────────────────────────
# TESTE ISOLADO
# Lê o html_selenium.txt salvo pelo coletor.py
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 55)
    print("   DETECTIVE — Testando extrator.py")
    print("=" * 55 + "\n")

    try:
        with open("html_selenium.txt", "r", encoding="utf-8") as f:
            html = f.read()
        print(f"HTML carregado: {len(html):,} caracteres\n")
    except FileNotFoundError:
        print("❌ html_selenium.txt não encontrado.")
        print("   Rode o coletor.py primeiro.")
        exit()

    dados = extrair_dados(html)

    if dados:
        print("\n" + "=" * 55)
        print("   DOSSIER DO CONCORRENTE")
        print("=" * 55)
        print(f"  📦 Produto  : {dados['titulo']}")
        print(f"  💰 Preço    : R$ {dados['preco']:.2f}")
        if dados['preco_original']:
            print(f"  🏷️  Original : R$ {dados['preco_original']:.2f}")
        print(f"  🔖 Desconto : {dados['desconto']}")
        print(f"  🚚 Frete    : {'GRÁTIS ✅' if dados['frete_gratis'] else 'Pago ❌'}")
        print(f"  📊 Estoque  : {dados['estoque_texto']}")
        if dados['estoque'] is not None:
            if dados['estoque'] <= 5:
                print(f"  ⚠️  ALERTA   : Estoque BAIXO ({dados['estoque']} unidades)!")
            else:
                print(f"  ✅ Unidades  : {dados['estoque']}+ disponíveis")
        print(f"  ⭐ Avaliações: {dados['avaliacoes']}")
        print(f"  🏆 Vendas   : {dados['vendas']}")
        print("=" * 55)