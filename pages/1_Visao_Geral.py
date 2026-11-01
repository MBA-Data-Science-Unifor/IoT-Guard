import streamlit as st

from utils.styles import page_header, section, page_footer


page_header(
    icon="🛡️",
    title="IoT Guard",
    subtitle="Detecção de intrusão em redes IoT por aprendizado de máquina supervisionado.",
    badge="MBA · Unifor · Turma 12",
)

section("O problema", badge="Contexto")
st.markdown(
    "Lâmpadas, sensores e assistentes de voz estão presentes em casas, indústrias "
    "e hospitais. Muitos desses dispositivos têm pouca memória, firmware simples "
    "e senhas fracas, o que amplia a exposição a ataques. Um **sistema de detecção "
    "de intrusão (IDS)** observa o tráfego de rede e identifica comportamentos "
    "suspeitos para apoiar a resposta a incidentes."
)

section("Equipe", badge="Membros")
st.markdown(
    """
    | Nome do Integrante | Matrícula |
    | :--- | :--- |
    | **Alexandre Franco** | `2650081` |
    | **Caio Cunha** | `2650555` |
    | **Rodrigo Franco** | `2650089` |
    """
)

page_footer()