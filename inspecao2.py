# ============================================================
#  DETECTIVE — inspecao2.py
#  Testa as duas estratégias de acesso e decide qual usar
#  Rode: python inspecao2.py
# ============================================================

import requests
import json

ID_PRODUTO = "MLB4288664161"

print("=" * 55)
print("  DETECTIVE — Diagnóstico de acesso ao ML")
print("=" * 55)

# ─────────────────────────────────────────────────────────────
# ESTRATÉGIA 1 — API oficial do Mercado Livre
# Retorna JSON limpo com todos os dados do produto.
# Não precisa de BeautifulSoup, não sofre bloqueio anti-bot.
# ─────────────────────────────────────────────────────────────

print("\n[1/2] Testando API oficial...")
url_api = f"https://api.mercadolibre.com/items/{ID_PRODUTO}"

try:
    r = requests.get(url_api, timeout=15)
    print(f"      Status: {r.status_code}")

    if r.status_code == 200:
        dados = r.json()
        print("\n✅ API FUNCIONOU! Dados disponíveis:")
        print(f"   Título    : {dados.get('title')}")
        print(f"   Preço     : R$ {dados.get('price')}")
        print(f"   Estoque   : {dados.get('available_quantity')} unidades")
        print(f"   Vendidos  : {dados.get('sold_quantity')}")
        print(f"   Condição  : {dados.get('condition')}")
        print(f"   Frete gr. : {dados.get('shipping', {}).get('free_shipping')}")
        print(f"   Status    : {dados.get('status')}")
        print(f"\n   Todas as chaves: {list(dados.keys())}")

        # Salva o JSON completo para análise
        with open("api_retorno.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print("\n   Arquivo api_retorno.json salvo para análise completa.")

    elif r.status_code == 403:
        print("   ❌ API bloqueada — precisaremos de autenticação OAuth.")
    else:
        print(f"   ⚠️  Status inesperado: {r.status_code}")

except Exception as e:
    print(f"   ❌ Erro: {e}")

# ─────────────────────────────────────────────────────────────
# ESTRATÉGIA 2 — HTML via www.mercadolivre.com.br
# ─────────────────────────────────────────────────────────────

print("\n[2/2] Testando HTML via www...")
url_www = f"https://www.mercadolivre.com.br/p/{ID_PRODUTO}"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com.br/",
}

try:
    r = requests.get(url_www, headers=headers, timeout=15, allow_redirects=True)
    html = r.content.decode("utf-8", errors="replace")
    print(f"      Status: {r.status_code} | Tamanho: {len(html):,} chars")
    print(f"      URL final: {r.url[:70]}")

    if "verifyChallenge" in html:
        print("   ⚠️  Bloqueado pelo anti-bot do ML (página de desafio JS)")
    elif "andes-money-amount" in html or "ui-pdp-price" in html:
        print("   ✅ HTML real do produto chegou!")
        with open("html_www.txt", "w", encoding="utf-8") as f:
            f.write(html)
        print("   Arquivo html_www.txt salvo.")
    else:
        print("   ⚠️  Página chegou mas estrutura incerta.")
        print("   Primeiros 300 chars:", html[:300])

except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "=" * 55)
print("  Cole o resultado completo para o Claude analisar.")
print("=" * 55)