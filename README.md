#  PROJETO DETECTIVE
### Selenium como estrela da automação inteligente

> *"Se ele respirar, saberemos."*

---

## O que é o DETECTIVE?

O DETECTIVE é um sistema de monitoramento de concorrentes desenvolvido exclusivamente para o Mercado Livre, o maior marketplace do Brasil. Criado para sempre estar um passo à frente da concorrência, seu objetivo é simples e direto: acompanhar em tempo real cada movimento de um concorrente dentro da plataforma.

Preço, estoque, frete e avaliações — qualquer mudança é capturada e transformada em alertas automáticos para tomada de decisão imediata.

---

## O Desafio

Sites como o Mercado Livre são robustos e bloqueiam qualquer sistema automatizado que tente acessar seus dados. O desafio foi ultrapassar essa proteção e fazer nosso programa se comportar de forma indistinguível de um ser humano navegando na internet.

### Por que o requests falhou?

A primeira tentativa usou a biblioteca `requests` — a mais famosa para web scraping em Python. O Mercado Livre respondeu com uma página de desafio JavaScript:

```
"This page requires JavaScript to work."
verifyChallenge() → resolve SHA-256...
```

O `requests` não executa JavaScript. Fim de jogo.

### A solução: Selenium + undetected-chromedriver

O **Selenium** abre um navegador Chrome real e navega como um humano. O **undetected-chromedriver** vai além — aplica patches profundos no Chrome para tornar o robô completamente invisível para sistemas anti-bot.

```python
import undetected_chromedriver as uc
driver = uc.Chrome(version_main=148)
# navigator.webdriver = undefined ← anti-bot não detecta!
```

---

## As Bibliotecas

| Biblioteca | Papel | Status |
|---|---|---|
| `requests` | Primeira tentativa — acesso HTTP | ❌ Bloqueado pelo anti-bot |
| `selenium` | Controla o Chrome real | ✅ Estrela do projeto |
| `undetected-chromedriver` | Torna o robô invisível | ✅ O diferencial |
| `beautifulsoup4` | Extrai dados do HTML | ✅ Parceiro do Selenium |
| `streamlit` | Dashboard visual interativo | ✅ A vitrine |

---

## Arquitetura do Projeto

```
📁 Dectetive ML/
│
├── fase1_teste_conexao.py   → Prova do processo: requests vs anti-bot
├── coletor.py               → Selenium + undetected: captura o HTML
├── extrator.py              → BeautifulSoup: extrai os dados
├── historico.py             → Salva cada coleta em CSV com timestamp
├── alertas.py               → Compara e dispara alertas automáticos
├── dashboard.py             → Streamlit: interface visual completa
├── main.py                  → Orquestrador: roda tudo com um comando
└── agendador.py             → Monitora automaticamente de 3 em 3 horas
```

### O fluxo completo

```
Selenium coleta HTML
      ↓
BeautifulSoup extrai dados
      ↓
CSV registra com timestamp
      ↓
Alertas comparam com coleta anterior
      ↓
Streamlit exibe tudo no dashboard
```

---

## O que o DETECTIVE monitora

- 💰 **Preço** — com ou sem desconto
- 🔖 **Desconto** — percentual aplicado
- 🚚 **Frete** — grátis ou pago
- 📦 **Estoque** — unidades disponíveis
- ⭐ **Avaliações** — quantidade de reviews
- 🏆 **Vendas** — volume de vendidos
- 🖼️ **Imagem** — foto do produto monitorado

---

## Sistema de Alertas Inteligentes

```
🔴 CRÍTICO  → Estoque zerou / frete grátis ativado
🟡 ATENÇÃO  → Concorrente baixou o preço
🟢 POSITIVO → Concorrente subiu o preço / estoque caindo
ℹ️  INFO     → Novas avaliações / sem mudanças
```

Cada alerta inclui a situação detectada e uma **ação estratégica sugerida**.

---

## Como usar

**Instalação:**
```bash
pip install selenium undetected-chromedriver beautifulsoup4 streamlit pandas
```

**Coleta manual:**
```bash
python main.py
```

**Monitoramento automático (a cada 3 horas):**
```bash
python agendador.py
```

**Dashboard visual:**
```bash
streamlit run dashboard.py
```

---

## Dashboard

O dashboard permite:
- Colar qualquer link do Mercado Livre e monitorar na hora
- Ver métricas em tempo real com variação desde a última coleta
- Acompanhar alertas automáticos com ações sugeridas
- Visualizar gráficos de evolução de preço e estoque
- Baixar o histórico completo em CSV

---

## A Apresentação

https://prezi.com/p/edit/nlftlcaz8rkn/
- O Selenium vai chegar de limusine. 🚗

---

## Contexto Acadêmico

Projeto desenvolvido como trabalho acadêmico com foco na demonstração prática de bibliotecas Python. O DETECTIVE nasceu como um exercício sobre automação web e se tornou uma ferramenta real de inteligência competitiva para o Mercado Livre.

**Tecnologias:** Python • Selenium • undetected-chromedriver • BeautifulSoup4 • Streamlit

---

*DETECTIVE v2.0 — 2026*
