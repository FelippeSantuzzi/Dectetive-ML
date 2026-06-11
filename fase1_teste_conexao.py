
#  PROJETO DETECTIVE — Fase 1 (Teste)
#  Objetivo: instalar as bibliotecas e fazer o primeiro
#  contato com a página do concorrente no Mercado Livre.
#  pip install requests beautifulsoup4 streamlit


import requests


# 1. URL DO CONCORRENTE
#    ATENÇÃO — Dois tipos de URL no Mercado Livre:
#    Tipo 1 — Página agrupada (/up/MLBU...)
#    Lista vários vendedores do mesmo produto.
#    NÃO serve para monitorar um concorrente específico.
#    Tipo 2 — Anúncio direto (produto.mercadolivre/MLB-XXX)
#    É a página ESPECÍFICA do seu concorrente, com preço,
#    estoque, avaliações — este é o alvo do DETECTIVE.
#    O ID MLB-4288664161 veio do parâmetro wid= da sua URL.

URL_CONCORRENTE = "https://www.mercadolivre.com.br/mangote-termico-industrial-alta-temperatura-cozinha-par-epi/p/MLBU3534355699"

# 2. HEADERS — "Fingir" que somos um navegador real
#
#    O Mercado Livre bloqueia robôs que não se identificam.
#    O User-Agent diz ao site qual navegador estamos usando.
#    Sem isso, o site retorna erro 403 (acesso negado).

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/webp,*/*;q=0.8"
    ),
}

# 3. FAZENDO A REQUISIÇÃO
#
#    requests.get()   envia um pedido HTTP GET para a URL
#    timeout=15       para de esperar após 15 segundos
#    allow_redirects  segue redirecionamentos automaticamente


print("=" * 55)
print("   DETECTIVE — Fase 1: Conexão com o alvo")
print("=" * 55)
print(f"\nAlvo: {URL_CONCORRENTE}\n")

try:
    resposta = requests.get(URL_CONCORRENTE, headers=HEADERS, timeout=15, allow_redirects=True)

    print(f"Status code      : {resposta.status_code}")
    print(f"URL final        : {resposta.url[:70]}")
    print(f"Tipo de conteúdo : {resposta.headers.get('Content-Type', 'não informado')}")
    print(f"Tamanho do HTML  : {len(resposta.text):,} caracteres")

    if resposta.status_code == 200:
        print("\n Conexão bem-sucedida! O HTML chegou.")
        print("   Na Fase 2 vamos usar BeautifulSoup para")
        print("   extrair preço, estoque, frete e avaliações.\n")
        print("── Prévia do HTML (500 chars) ───────────────────")
        print(resposta.text[:500])
        print("─" * 50)

    elif resposta.status_code == 403:
        print("\n  Erro 403: acesso negado pelo site.")
        print("   Tente rodar novamente em alguns minutos.")

    elif resposta.status_code == 404:
        print("\n  Erro 404: página não encontrada.")
        print("   Verifique se o anúncio do concorrente ainda existe.")

    else:
        print(f"\n Status inesperado: {resposta.status_code}")

except requests.exceptions.ConnectionError:
    print("\n❌ Erro de conexão: sem acesso à internet.")
except requests.exceptions.Timeout:
    print("\n❌ Timeout: o site demorou demais para responder.")
except requests.exceptions.RequestException as erro:
    print(f"\n❌ Erro inesperado: {erro}")