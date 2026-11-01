from pathlib import Path

import polars as pl
import plotly.express as px
import streamlit as st

from utils.config import (
    BENCHMARK, BEST_MODEL_NAME, BEST_MODEL_PARAMS,
)
from utils.styles import page_header, kpi_grid, section, callout, page_footer

MODEL_IMAGES = Path(__file__).resolve().parents[1] / "artifacts" / "presentation" / "model"

page_header(
    icon="🤖",
    title="Benchmark e Avaliação",
    subtitle="Comparação dos 3 modelos baseados em árvore (boosting + bagging) "
             "no teste intocado. Métrica primária: F1-Macro.",
    badge="Etapa 03",
)

best = next(b for b in BENCHMARK if b["Modelo"] == BEST_MODEL_NAME)
kpi_grid([
    {"label": "Modelo campeão",     "value": BEST_MODEL_NAME, "tone": "primary"},
    {"label": "F1-Macro (teste)",   "value": f"{best['F1 macro']:.4f}", "tone": "success",
     "delta": "+88pp vs baseline DoS"},
    {"label": "Acurácia (teste)",   "value": f"{best['Acurácia']:.4f}", "tone": "accent"},
    {"label": "ROC-AUC (OvR)",      "value": f"{best['ROC-AUC (OvR)']:.4f}", "tone": "warning"},
])

callout(
    "O benchmark compara **LightGBM, HistGradientBoosting e RandomForest**. "
    "Os hiperparâmetros foram buscados com `RandomizedSearchCV`, usando "
    "**F1 macro** na validação cruzada do treino. A tabela abaixo mostra o "
    "desempenho no teste com a distribuição real das classes.",
    kind="info",
)

section("1. Tabela Comparativa", badge="Teste")
st.caption("Kappa e MCC medem concordância além do acaso; Log-Loss avalia as probabilidades previstas (menor é melhor). O baseline constante não fornece probabilidades para Log-Loss.")
df = pl.DataFrame(BENCHMARK)
st.dataframe(
    df,
    width="stretch",
    hide_index=True,
    column_config={column: st.column_config.NumberColumn(format="%.4f")
                   for column in df.columns if column != "Modelo"},
)

section("2. Comparação Visual", badge="Desempenho e generalização")
col_metrics, col_generalization = st.columns(2)
metricas_plot = ["Acurácia", "F1 macro", "Recall macro", "F1 ponderado"]
df_long = df.select(["Modelo", *metricas_plot]).unpivot(
    index="Modelo", variable_name="Métrica", value_name="Score"
)
fig = px.bar(
    df_long, x="Modelo", y="Score", color="Métrica", barmode="group",
    title="Benchmark — teste intocado (distribuição real)",
    range_y=[0, 1.05],
)
fig.update_layout(height=420)
with col_metrics:
    st.plotly_chart(fig, width="stretch")

fig_generalization = px.bar(
    x=["Teste completo", "Fluxos inéditos"],
    y=[best["F1 macro"], 0.7935],
    text=[f"{best['F1 macro']:.4f}", "0.7935"],
    title=f"F1 macro do {BEST_MODEL_NAME} por recorte",
    labels={"x": "Recorte do teste", "y": "F1 macro"},
)
fig_generalization.update_layout(height=420, yaxis_range=[0, 1.05])
with col_generalization:
    st.plotly_chart(fig_generalization, width="stretch")

callout(
    "**85,5%** dos fluxos do teste repetem vetores presentes no treino. "
    "Nos **3.576 fluxos inéditos**, o F1 macro do campeão cai para **0,7935**. "
    "Brute force SSH e Nmap FIN têm apenas **7 e 6 exemplos** no teste, "
    "respectivamente; a estimativa para essas classes é pouco estável.",
    kind="warning",
)

section("3. Desempenho por classe", badge="Matriz de confusão")
st.image(
    MODEL_IMAGES / "confusao_RandomForest.png",
    caption="Matriz de confusão do RandomForest no teste: contagens absolutas e proporções por classe real.",
    width="stretch",
)
st.image(
    MODEL_IMAGES / "por_classe_RandomForest.png",
    caption="Precisão, recall e F1 por classe; n indica a quantidade de exemplos reais no teste.",
    width="stretch",
)

section(f"4. Modelo Final — {BEST_MODEL_NAME}", badge="Champion")
st.markdown("**Hiperparâmetros escolhidos**")
st.json(BEST_MODEL_PARAMS)

page_footer()
