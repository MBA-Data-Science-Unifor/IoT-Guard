from pathlib import Path

import polars as pl
import plotly.express as px
import streamlit as st

from utils.config import (
    DISTRIBUICAO_COMPLETA, NOMES, CORES, CLASSES_NORMAIS, CLASSES_ATAQUE,
    TOP_FEATURES_MI, TOP_SCORES_MI, N_DUPLICADAS, N_TOTAL, N_FEATURES_RAW,
)
from utils.styles import page_header, kpi_grid, section, callout, pills, page_footer

EDA_IMAGES = Path(__file__).resolve().parents[1] / "artifacts" / "presentation" / "eda"

page_header(
    icon="🔍",
    title="Análise Exploratória",
    subtitle="Base RT-IoT2022: tráfego real capturado com Zeek e Flowmeter. "
             "Distribuição, qualidade, leakage e relevância das features.",
    badge="Etapa 01",
)

kpi_grid([
    {"label": "Fluxos analisados", "value": f"{N_TOTAL:,}".replace(",", "."),
     "tone": "primary"},
    {"label": "Colunas originais", "value": str(N_FEATURES_RAW), "tone": "accent"},
    {"label": "Classes de tráfego", "value": str(len(CLASSES_NORMAIS) + len(CLASSES_ATAQUE)),
     "delta": "3 normais · 9 ataques", "tone": "warning"},
])

section("1. Dicionário de dados", badge="Entrada e alvo")
st.markdown(
    "As **83 features descritivas** estão agrupadas abaixo. `fwd` indica origem → "
    "destino; `bwd`, destino → origem."
)
st.dataframe(
    pl.DataFrame(
        [
            ("Identificação", "id", "Número sequencial da linha dentro de cada classe", "❌ Removida: vazamento"),
            ("Portas", "id.orig_p, id.resp_p", "Portas de origem e destino", "❌ Removidas: artefato da coleta"),
            ("Protocolo", "proto, service", "Transporte (tcp/udp/icmp) e serviço (dns, mqtt, http…)", "✅ Categóricas codificadas"),
            ("Duração e volume", "flow_duration, fwd_pkts_tot, bwd_pkts_tot, fwd_data_pkts_tot", "Duração e pacotes em cada sentido", "✅ Features"),
            ("Taxas", "fwd_pkts_per_sec, flow_pkts_per_sec, down_up_ratio, payload_bytes_per_second", "Velocidade de pacotes e bytes", "✅ Features"),
            ("Cabeçalhos", "fwd_header_size_tot/min/max, bwd_header_size_*", "Tamanho dos cabeçalhos", "✅ Features"),
            ("Flags TCP", "flow_SYN_flag_count, flow_ACK_flag_count, flow_FIN_flag_count, flow_RST_flag_count…", "Contagem das flags TCP", "✅ Features; bwd_URG_flag_count constante removida"),
            ("Payload", "fwd_pkts_payload.min/max/tot/avg/std, bwd_*, flow_*", "Estatísticas do conteúdo útil", "✅ Features"),
            ("Tempo entre pacotes (IAT)", "fwd_iat.*, bwd_iat.*, flow_iat.*", "Intervalos entre pacotes consecutivos", "✅ Features"),
            ("Subfluxos e rajadas", "fwd_subflow_*, fwd_bulk_*, bwd_bulk_*", "Comportamento em subsequências e rajadas", "✅ Features"),
            ("Atividade", "active.*, idle.*", "Tempo ativo ou ocioso do fluxo", "✅ Features"),
            ("Janela TCP", "fwd_init_window_size, bwd_init_window_size, fwd_last_window_size", "Tamanho da janela de recepção TCP", "✅ Features"),
            ("Target", "Attack_type", "Tipo de tráfego: 12 classes", "🎯 Alvo"),
        ],
        schema=["Grupo", "Colunas (exemplos)", "Descrição", "Uso no modelo"],
        orient="row",
    ),
    hide_index=True,
    width="stretch",
    row_height=58,
    column_config={
        "Grupo": st.column_config.TextColumn(width="medium"),
        "Colunas (exemplos)": st.column_config.TextColumn(width="large"),
        "Descrição": st.column_config.TextColumn(width="large"),
        "Uso no modelo": st.column_config.TextColumn(width="medium"),
    },
)

# ------------------------------------------------------------------ Distribuição
section("2. Distribuição de Classes", badge="Escala log")
df_dist = pl.DataFrame({
    "Classe": [NOMES[c] for c in DISTRIBUICAO_COMPLETA],
    "Fluxos": list(DISTRIBUICAO_COMPLETA.values()),
    "Grupo":  ["Normal" if c in CLASSES_NORMAIS else "Ataque"
               for c in DISTRIBUICAO_COMPLETA],
})
df_dist = df_dist.with_columns((pl.col("Fluxos") / pl.col("Fluxos").sum()).alias("Pct"))
fig = px.bar(
    df_dist, x="Fluxos", y="Classe", color="Grupo", orientation="h",
    color_discrete_map=CORES, log_x=True, text="Pct",
    title="Attack_type — azul = normal, vermelho = ataque",
)
fig.update_traces(texttemplate="%{text:.2%}", textposition="outside")
fig.update_layout(height=520, yaxis=dict(categoryorder="total ascending"))
st.plotly_chart(fig, width="stretch")

callout(
    "**Desbalanceamento extremo:** `DOS_SYN_Hping` representa **76,9%** dos "
    "fluxos, enquanto NMAP FIN e brute force SSH têm menos de **40 exemplos** cada. "
    "Um classificador que responde sempre DoS alcança **76,88% de acurácia**, "
    "mas apenas **7,24% de F1 macro**. Por isso, o benchmark dá o mesmo peso "
    "às 12 classes com F1 macro.",
    kind="warning",
)

col_normal, col_attack = st.columns(2)
with col_normal:
    st.markdown("**Tráfego normal**")
    pills([(NOMES[c], "normal") for c in CLASSES_NORMAIS])
with col_attack:
    st.markdown("**Ataques**")
    pills([(NOMES[c], "attack") for c in CLASSES_ATAQUE])

# ------------------------------------------------------------------ Qualidade
section("3. Qualidade dos Dados", badge="Sanity check")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Nulos",       "0")
c2.metric("Infinitos",   "0")
c3.metric("Duplicadas",  f"{N_DUPLICADAS:,}".replace(",", "."), "4,2%")
c4.metric("Constantes",  "1")

callout(
    "**Outliers são sinal, não ruído.** 14%–26% das linhas caem fora do IQR em "
    "6 das 8 features analisadas — isso é a assinatura dos ataques (fluxos DoS de "
    "1–2 pacotes, IAT zero, etc.). **Decisão: não remover outliers**; usar "
    "`RobustScaler` ajustado apenas no treino.",
    kind="info",
)
st.image(
    EDA_IMAGES / "distribuicao_features_por_classe.png",
    caption="Distribuição de oito medidas de fluxo por classe, em escala logarítmica. Os pontos fora das caixas mostram os valores extremos preservados.",
    width="stretch",
)

section("4. Estatísticas descritivas", badge="Features numéricas")
st.dataframe(
    pl.DataFrame([
        {"Feature": "flow_duration", "Mediana": "0,00", "Média": "3,81", "Máximo": "21.728,34", "Skew": "120,96"},
        {"Feature": "fwd_pkts_tot", "Mediana": "1,00", "Média": "2,27", "Máximo": "4.345", "Skew": "121,44"},
        {"Feature": "flow_pkts_per_sec", "Mediana": "493.447,53", "Média": "703.568,29", "Máximo": "2.097.152", "Skew": "0,99"},
        {"Feature": "flow_iat.avg", "Mediana": "4,05", "Média": "139.654,49", "Máximo": "72.835.760", "Skew": "26,18"},
    ]),
    hide_index=True,
    width="stretch",
)
st.caption("Valores da execução do notebook 01; skew é o coeficiente de assimetria.")
callout(
    "A assimetria absoluta mediana das features numéricas é **27,4**; "
    "**62 de 81** têm |skew| > 5. Mediana e média muito diferentes indicam "
    "distribuições concentradas com caudas longas.",
    kind="info",
)

# ------------------------------------------------------------------ Leakage
section("5. Data Leakage Detectado", badge="Crítico")
colA, colB = st.columns(2)
with colA:
    st.markdown(
        "#### `id` reinicia em cada classe\n"
        "- Árvore usando só `id` acerta **~70%**.\n"
        "- Um `id > 8.107` só pode ser DoS.\n"
        "- **Removida do dataset final.**"
    )
with colB:
    st.markdown(
        "#### `id.resp_p` concentra por classe\n"
        "- 100% do DoS SYN vai para a porta 21.\n"
        "- Árvore usando só `id.resp_p` acerta **~91%**.\n"
    "- **Removida** (MI ≈ 0,80)."
    )

section("6. Protocolo e serviço", badge="Perfil do tráfego")
st.image(
    EDA_IMAGES / "protocolo_servico_por_classe.png",
    caption="Proporção de protocolos e serviços em cada classe; o padrão de comunicação também ajuda a caracterizar os fluxos.",
    width="stretch",
)

# ------------------------------------------------------------------ Relevância
section("7. Relevância das Features", badge="Mutual Information")
fig = px.bar(
    x=TOP_SCORES_MI,
    y=TOP_FEATURES_MI[:10], orientation="h",
    title="Top-10 features por Mutual Information",
)
fig.update_layout(height=420, xaxis_title="MI", yaxis_title="", yaxis=dict(categoryorder="total ascending"))
st.plotly_chart(fig, width="stretch")

callout(
    "As features mais relevantes são **comportamentais** — tamanhos de pacote, "
    "taxas, IAT. Note que `id.resp_p` aparece no top-10 por MI **mas foi removido** "
    "do dataset final para evitar leakage.",
    kind="info",
)

# ------------------------------------------------------------------ Correlação
section("8. Redundância", badge="|r| ≥ 0,95")
st.markdown(
    "Há **180 pares** com |r| ≥ 0,95. O mapa abaixo mostra uma amostra "
    "representativa das correlações; as features redundantes foram mantidas no modelo."
)
st.image(
    EDA_IMAGES / "correlacao_spearman.png",
    caption="Correlação de Spearman entre 22 features representativas, calculada após log1p.",
    width="stretch",
)

# ------------------------------------------------------------------ Separação
section("9. Separabilidade", badge="PCA e t-SNE")
st.markdown(
    "As duas componentes do **PCA** explicam **62,1%** da variância. No **t-SNE**, "
    "a maioria das classes forma grupos mais definidos, embora ARP, tráfego normal "
    "e parte do Slowloris ainda se sobreponham. Isso favorece o uso de modelos "
    "não lineares no benchmark."
)
st.image(
    EDA_IMAGES / "pca_tsne.png",
    caption="Projeções PCA e t-SNE de até 300 fluxos por classe; os eixos do t-SNE representam apenas a posição na projeção.",
    width="stretch",
)

section("10. Conclusões do EDA", badge="Resumo")
callout(
    """
    - Base **sem nulos, sem infinitos, sem negativos** — mas com **5.195 duplicadas**.
    - **3 colunas causam leakage** (`id`, `id.orig_p`, `id.resp_p`) → removidas.
    - Features **muito assimétricas** (skew mediano ≈ 27) → o pipeline usa `RobustScaler`.
    - **Outliers são a assinatura dos ataques** → não remover.
    - **F1-Macro** é a métrica primária do projeto.
    """,
    kind="success",
)

page_footer()
