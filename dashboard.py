
#  PROJETO DETECTIVE — dashboard.py
#  Responsabilidade: exibir todos os dados numa interface
#  visual interativa usando Streamlit.
#
#  Biblioteca usada: Streamlit
#
#  Como rodar:
#    streamlit run dashboard.py
#
#  O dashboard exibe:
#    - Dossier atual do concorrente
#    - Alertas inteligentes em tempo real
#    - Gráfico histórico de preços
#    - Histórico de estoque
#    - Tabela completa de registros

import streamlit as st
import pandas as pd
from datetime import datetime

from coletor   import buscar_pagina
from extrator  import extrair_dados
from historico import salvar_historico, carregar_historico, resumo_historico
from alertas   import verificar_alertas


# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="DETECTIVE 🕵️",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown("""
<style>
    .main { background-color: #0a0a0a; }
    .block-container { padding-top: 1.5rem; }

    .detective-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #f5c842;
        border-radius: 12px;
        padding: 20px 30px;
        margin-bottom: 20px;
    }
    .detective-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #f5c842;
        letter-spacing: 4px;
        margin: 0;
    }
    .detective-subtitle {
        color: #888899;
        font-size: 0.95rem;
        margin-top: 4px;
    }

    .metric-card {
        background: #1e1e2e;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 4px solid #f5c842;
        margin-bottom: 10px;
    }
    .metric-label {
        color: #888899;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }

    .alerta-critico  { background:#2d1a1a; border-left:4px solid #e63946; border-radius:8px; padding:14px 18px; margin:8px 0; }
    .alerta-atencao  { background:#2d2a1a; border-left:4px solid #f5c842; border-radius:8px; padding:14px 18px; margin:8px 0; }
    .alerta-positivo { background:#1a2d1a; border-left:4px solid #2dc653; border-radius:8px; padding:14px 18px; margin:8px 0; }
    .alerta-info     { background:#1a1e2d; border-left:4px solid #3a86ff; border-radius:8px; padding:14px 18px; margin:8px 0; }

    .alerta-titulo  { font-weight:700; font-size:1rem; color:#ffffff; }
    .alerta-msg     { color:#cccccc; font-size:0.88rem; margin-top:4px; }
    .alerta-acao    { color:#f5c842; font-size:0.85rem; margin-top:6px; font-style:italic; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="detective-header">
    <div class="detective-title">🕵️ DETECTIVE</div>
    <div class="detective-subtitle">
        Inteligência Competitiva em tempo real • Mercado Livre
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SIDEBAR — Controles
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://http2.mlstatic.com/D_NQ_NP_2X_938282-MLB94905154016_102025-F.webp", width=200)
    st.markdown("### ⚙️ Controles")

    st.markdown("**Concorrente monitorado:**")
    st.code("MLB-4288664161", language=None)

    st.markdown("---")

    # Botão de atualização manual
    if st.button("🔄 Atualizar agora", use_container_width=True, type="primary"):
        with st.spinner("🕵️ DETECTIVE em ação..."):
            html  = buscar_pagina(modo_visivel=False)
            dados = extrair_dados(html) if html else None
            if dados:
                salvar_historico(dados)
                st.session_state["dados_atuais"] = dados
                st.success("✅ Dados atualizados!")
            else:
                st.error("❌ Falha na coleta.")

    st.markdown("---")
    st.markdown("### 📊 Resumo")
    resumo = resumo_historico()
    if resumo:
        st.metric("Total de coletas", resumo["total_registros"])
        st.metric("Preço mínimo", f"R$ {resumo['preco_minimo']:.2f}")
        st.metric("Preço máximo", f"R$ {resumo['preco_maximo']:.2f}")
        st.caption(f"Primeira coleta: {resumo['primeira_coleta']}")
        st.caption(f"Última coleta: {resumo['ultima_coleta']}")

    st.markdown("---")
    st.caption("DETECTIVE v1.0 • 2026")


# ─────────────────────────────────────────────────────────────
# CARREGA DADOS
# ─────────────────────────────────────────────────────────────

historico = carregar_historico()

# Pega o último registro como dados atuais
if historico:
    dados_atuais = historico[-1]
else:
    dados_atuais = None


# ─────────────────────────────────────────────────────────────
# BLOCO 1 — DOSSIER ATUAL (métricas principais)
# ─────────────────────────────────────────────────────────────

st.markdown("### 📋 Dossier do Concorrente")

if dados_atuais:
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        preco = float(dados_atuais.get("preco", 0))
        # Calcula variação em relação ao registro anterior
        delta = None
        if len(historico) >= 2:
            preco_ant = float(historico[-2].get("preco", preco))
            delta = f"R$ {preco - preco_ant:+.2f}"
        st.metric("💰 Preço Atual", f"R$ {preco:.2f}", delta=delta)

    with col2:
        desconto = dados_atuais.get("desconto", "Sem desconto")
        st.metric("🔖 Desconto", desconto)

    with col3:
        frete = dados_atuais.get("frete_gratis", "False")
        frete_ok = str(frete).lower() in ["true", "1", "sim"]
        st.metric("🚚 Frete Grátis", "✅ SIM" if frete_ok else "❌ NÃO")

    with col4:
        estoque = dados_atuais.get("estoque", "?")
        delta_est = None
        if len(historico) >= 2:
            est_ant = historico[-2].get("estoque", "")
            try:
                delta_est = f"{int(estoque) - int(est_ant):+d} un."
            except:
                pass
        st.metric("📦 Estoque", f"{estoque} un.", delta=delta_est, delta_color="inverse")

    with col5:
        aval = dados_atuais.get("avaliacoes", 0)
        delta_aval = None
        if len(historico) >= 2:
            aval_ant = historico[-2].get("avaliacoes", aval)
            try:
                diff = int(aval) - int(aval_ant)
                if diff != 0:
                    delta_aval = f"+{diff} novas"
            except:
                pass
        st.metric("⭐ Avaliações", aval, delta=delta_aval)

    st.caption(f"📦 {dados_atuais.get('titulo', '')}  |  🏆 {dados_atuais.get('vendas', '')}  |  🕐 Última coleta: {dados_atuais.get('data_hora', '')}")

else:
    st.warning("⚠️ Nenhum dado disponível. Clique em 'Atualizar agora' na barra lateral.")


# ─────────────────────────────────────────────────────────────
# BLOCO 2 — ALERTAS
# ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 🚨 Central de Alertas")

if dados_atuais:
    # Converte string para tipos corretos
    dados_conv = dict(dados_atuais)
    try:
        dados_conv["preco"]      = float(dados_atuais.get("preco", 0))
        dados_conv["avaliacoes"] = int(dados_atuais.get("avaliacoes", 0))
        dados_conv["estoque"]    = int(dados_atuais.get("estoque", 0)) if dados_atuais.get("estoque") else None
    except:
        pass

    alertas = verificar_alertas(dados_conv)

    for alerta in alertas:
        nivel = alerta.get("nivel", "info")
        st.markdown(f"""
        <div class="alerta-{nivel}">
            <div class="alerta-titulo">{alerta['emoji']} {alerta['titulo']}</div>
            <div class="alerta-msg">📋 {alerta['mensagem']}</div>
            <div class="alerta-acao">⚡ {alerta['acao']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Nenhum dado para analisar ainda.")


# ─────────────────────────────────────────────────────────────
# BLOCO 3 — GRÁFICOS
# ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 📈 Histórico Visual")

if len(historico) >= 2:
    df = pd.DataFrame(historico)

    # Converte tipos
    df["preco"]     = pd.to_numeric(df["preco"], errors="coerce")
    df["estoque"]   = pd.to_numeric(df["estoque"], errors="coerce")
    df["avaliacoes"]= pd.to_numeric(df["avaliacoes"], errors="coerce")
    df["data_hora"] = pd.to_datetime(df["data_hora"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
    df = df.sort_values("data_hora")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("**💰 Evolução do Preço**")
        st.line_chart(df.set_index("data_hora")["preco"], color="#f5c842", height=250)

    with col_g2:
        st.markdown("**📦 Evolução do Estoque**")
        st.line_chart(df.set_index("data_hora")["estoque"], color="#e63946", height=250)

else:
    st.info("📊 Acumule pelo menos 2 coletas para ver os gráficos de evolução.")
    st.caption("Clique em 'Atualizar agora' algumas vezes ao longo do dia.")


# ─────────────────────────────────────────────────────────────
# BLOCO 4 — TABELA HISTÓRICA
# ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 📂 Tabela de Registros")

if historico:
    df_tabela = pd.DataFrame(historico)

    # Renomeia colunas para português
    df_tabela = df_tabela.rename(columns={
        "data_hora"      : "Data/Hora",
        "preco"          : "Preço (R$)",
        "desconto"       : "Desconto",
        "frete_gratis"   : "Frete Grátis",
        "estoque"        : "Estoque (un.)",
        "avaliacoes"     : "Avaliações",
        "vendas"         : "Vendas",
    })

    # Mostra colunas relevantes (sem titulo e estoque_texto)
    colunas_exibir = ["Data/Hora", "Preço (R$)", "Desconto", "Frete Grátis", "Estoque (un.)", "Avaliações", "Vendas"]
    colunas_exibir = [c for c in colunas_exibir if c in df_tabela.columns]

    st.dataframe(
        df_tabela[colunas_exibir].sort_values("Data/Hora", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    # Botão de download do CSV
    csv_data = df_tabela.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar histórico completo (CSV)",
        data=csv_data,
        file_name=f"detective_historico_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
else:
    st.info("Nenhum registro no histórico ainda.")