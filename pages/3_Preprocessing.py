import polars as pl
import plotly.express as px
import streamlit as st
import textwrap

from utils.config import (
    DISTRIBUICAO_TREINO, DISTRIBUICAO_TESTE, NOMES, N_FEATURES_RAW, N_FEATURES_ENC,
)
from utils.styles import page_header, kpi_grid, section, callout, page_footer

page_header(
    icon="⚙️",
    title="Pré-processamento",
    subtitle="Split antes de qualquer transformação, RobustScaler, undersampling "
             "do DoS e SMOTE nas classes raras — sem vazamento treino→teste.",
    badge="Etapa 02",
)

kpi_grid([
    {"label": "Treino (balanceado)", "value": "34.085", "tone": "success",
     "delta": "após SMOTE"},
    {"label": "Teste (real)",        "value": "24.624", "tone": "accent",
     "delta": "sem balanceamento"},
    {"label": "Features do modelo", "value": str(N_FEATURES_ENC), "tone": "primary",
     "delta": f"{N_FEATURES_RAW} colunas na base original"},
    {"label": "DoS (cap)",           "value": "10.000", "tone": "warning",
     "delta": "undersampling"},
])

callout(
    "**Limpeza e codificação no notebook 01:** a base tem **0 nulos e 0 infinitos**. "
    "Foram removidos `id`, `id.orig_p`, `id.resp_p` e a coluna constante "
    "`bwd_URG_flag_count`. `proto` e `service` foram codificados com "
    "`LabelEncoder`; o alvo `Attack_type` foi codificado e salvo também em "
    "`target_mapping.csv`. Das **85 colunas originais**, restaram **80 features**; "
    "o alvo fica separado em `y_train` e `y_test`.",
    kind="info",
)

section("1. Ordem dos Passos", badge="Metodologia")
st.markdown(textwrap.dedent(
    """
    1. **Limpar e codificar no EDA**: retirar identificadores e constante; codificar `proto`, `service` e o alvo.
    2. **Carregar** `dataset_encoded.csv` e separar `Attack_type` das features.
    3. **Split estratificado** 80/20 — **antes** do ajuste do scaler e da reamostragem.
    4. **`RobustScaler`** ajustado **apenas no treino**; aplicado ao treino e ao teste.
    5. **Undersampling** do DoS: limite de **10.000** amostras.
    6. **SMOTE** em classes com < 500 exemplos (raras), somente no treino.
    7. Exportar `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`, `metadata.json`.
    """
))

section("2. Distribuição Antes vs Depois", badge="Balanceamento")
df_treino = pl.DataFrame({
    "Classe": [NOMES[c] for c in DISTRIBUICAO_TREINO],
    "Treino (balanceado)": list(DISTRIBUICAO_TREINO.values()),
})
df_teste = pl.DataFrame({
    "Classe": [NOMES[c] for c in DISTRIBUICAO_TESTE],
    "Teste (real)": list(DISTRIBUICAO_TESTE.values()),
})
df = df_treino.join(df_teste, on="Classe", how="full", coalesce=True).fill_null(0)

fig = px.bar(
    df.unpivot(index="Classe", variable_name="Conjunto", value_name="Amostras"),
    x="Classe", y="Amostras", color="Conjunto", barmode="group",
    title="Distribuição por classe — treino (balanceado) e teste (real)",
    log_y=True,
)
fig.update_layout(height=520, xaxis_tickangle=-30)
st.plotly_chart(fig, width="stretch")

callout(
    "**Treino reamostrado:** DoS representa ~29,3% das amostras (10.000 de "
    "34.085), e as classes raras foram elevadas para **500 cada** com SMOTE (k=3). "
    "**Teste intocado:** mantém a distribuição real (~77% DoS).",
    kind="info",
)

section("3. Detalhes Técnicos", badge="Pipeline")
st.markdown(
    "- **`RobustScaler`**: usa mediana e IQR — imune a outliers.\n"
    "- **Undersampling (RandomUnderSampler)**: reduz DoS de 75.727 → 10.000.\n"
    "- **SMOTE (k=3)**: gera amostras sintéticas para `DDOS_Slowloris`, "
    "`Metasploit_Brute_Force_SSH`, `Wipro_bulb` e `NMAP_FIN_SCAN` — todas elevadas "
    "para 500.\n"
    "- **Sem leakage**: scaler e reamostragem são fitados **apenas no treino**."
)

section("4. Por que não remover outliers?", badge="Decisão")
callout(
    "No tráfego de rede, **valores extremos são a assinatura dos ataques**:\n"
    "- DoS SYN: fluxos de 1–2 pacotes com duração ~0 e taxa altíssima.\n"
    "- Slowloris: conexões longas, taxa baixa.\n"
    "- Varreduras Nmap: fluxos minúsculos, sem payload.\n\n"
    "Remover esses pontos apagaria a informação que separa as classes.",
    kind="warning",
)

page_footer()
