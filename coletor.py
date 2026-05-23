# ============================================================
#  PROJETO DETECTIVE — coletor.py
#  v7 — pausa maior + scroll para forçar renderização JS
# ============================================================

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL_ALVO = (
    "https://produto.mercadolivre.com.br/"
    "MLB-4288664161-mangote-termico-industrial-"
    "alta-temperatura-cozinha-par-epi-azul"
)

TIMEOUT  = 30
PAUSA_JS = 12  # aumentado para dar tempo ao JS renderizar


def criar_driver(modo_visivel=False):
    opcoes = uc.ChromeOptions()
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1366,768")
    opcoes.add_argument("--lang=pt-BR")
    opcoes.add_argument("--disable-popup-blocking")

    driver = uc.Chrome(
        options=opcoes,
        headless=not modo_visivel,
        version_main=148,
    )
    return driver


def buscar_pagina(url=URL_ALVO, modo_visivel=False):

    print("[COLETOR] Iniciando navegador...")
    driver = None

    try:
        driver = criar_driver(modo_visivel=modo_visivel)

        print(f"[COLETOR] Acessando: {url[:80]}...")
        driver.get(url)

        # Pausa inicial — deixa o JS carregar
        print(f"[COLETOR] Aguardando carregamento inicial (8s)...")
        time.sleep(8)

        # Scroll suave para baixo — simula comportamento humano
        # e força o lazy-loading de elementos como preço e avaliações
        print("[COLETOR] Simulando scroll humano...")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        print(f"[COLETOR] URL final: {driver.current_url[:80]}")

        # Aguarda elemento do produto
        try:
            WebDriverWait(driver, TIMEOUT).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "ui-pdp-title")),
                    EC.presence_of_element_located((By.CLASS_NAME, "andes-money-amount")),
                    EC.presence_of_element_located((By.TAG_NAME, "h1")),
                )
            )
            print("[COLETOR] ✅ Elemento do produto detectado!")
        except:
            print("[COLETOR] ⚠️  Timeout — capturando mesmo assim...")

        html = driver.page_source
        tamanho = len(html)
        print(f"[COLETOR] HTML capturado: {tamanho:,} caracteres")

        # Diagnóstico
        print("\n[COLETOR] Diagnóstico:")
        checks = {
            "Título (ui-pdp-title)"      : "ui-pdp-title" in html,
            "Preço (andes-money-amount)" : "andes-money-amount" in html,
            "Frete (ui-pdp-shipping)"    : "ui-pdp-shipping" in html,
            "Avaliações (ui-pdp-review)" : "ui-pdp-review" in html,
            "Página de erro"             : "não existe" in html or "no existe" in html,
        }
        for item, encontrado in checks.items():
            icone = "✅" if encontrado else "❌"
            print(f"   {icone} {item}")

        with open("html_selenium.txt", "w", encoding="utf-8") as f:
            f.write(html)
        print("\n[COLETOR] html_selenium.txt salvo.")

        return html if tamanho > 5000 else None

    except Exception as erro:
        print(f"[COLETOR] ❌ Erro: {erro}")
        return None

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
            print("[COLETOR] Navegador fechado.")


if __name__ == "__main__":

    print("=" * 55)
    print("   DETECTIVE — Testando coletor.py v7")
    print("=" * 55 + "\n")

    html = buscar_pagina(modo_visivel=True)

    if html:
        print(f"\n✅ {len(html):,} chars prontos para o extrator.")
    else:
        print("\n❌ Nenhum HTML coletado.")