import streamlit as st

st.set_page_config(
    page_title="IoT Guard | Detecção de Intrusão",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_css, sidebar_brand

# Injetado uma única vez — as páginas herdam o CSS.
inject_css()
sidebar_brand()

pages = [
    st.Page("pages/1_Visao_Geral.py",   title="Visão Geral",       icon="🏠", default=True),
    st.Page("pages/2_EDA.py",           title="EDA",               icon="🔍"),
    st.Page("pages/3_Preprocessing.py", title="Pré-processamento", icon="⚙️"),
    st.Page("pages/4_Modelos.py",       title="Modelos",           icon="🤖"),
]

pg = st.navigation(pages)
pg.run()
