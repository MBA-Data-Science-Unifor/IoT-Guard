"""
Design system do IoT Guard — componentes visuais reutilizáveis.

Uso típico:
    from utils.styles import page_header, kpi_grid, section, callout, pills, page_footer
    page_header(icon="🏠", title="Visão Geral", subtitle="...", badge="MBA · Unifor")
    kpi_grid([{"label": "Fluxos", "value": "123.117", "tone": "primary"}])
    section("1. Contexto", badge="Problema")
    callout("...", kind="warning")
    pills([("DoS SYN", "attack"), ("MQTT", "normal")])
    page_footer()
"""
from __future__ import annotations

import html
import textwrap
from typing import Iterable

import streamlit as st
from markdown_it import MarkdownIt


_MARKDOWN = MarkdownIt("commonmark", {"html": False})


_CSS = """
<style>
:root {
    --primary:       #1E40AF;
    --primary-light: #3B82F6;
    --accent:        #06B6D4;
    --success:       #10B981;
    --warning:       #F59E0B;
    --danger:        #EF4444;
    --bg:            #F8FAFC;
    --card-bg:       #FFFFFF;
    --text:          #0F172A;
    --text-muted:    #64748B;
    --border:        #E2E8F0;
}

#MainMenu, footer, header { visibility: hidden; }

.main .block-container {
    padding-top:    2rem;
    padding-bottom: 2rem;
    max-width:      1400px;
}

[data-testid="stAppViewContainer"] > .main { background: var(--bg); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
}
[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    border-radius: 8px;
    padding: 0.55rem 0.75rem;
    margin: 2px 0;
    transition: background 0.15s;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background: rgba(255, 255, 255, 0.08);
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(90deg, var(--primary), var(--accent));
    font-weight: 700;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #1E40AF 0%, #06B6D4 100%);
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    color: #FFFFFF;
    margin-bottom: 1.75rem;
    box-shadow: 0 10px 30px rgba(30, 64, 175, 0.25);
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute;
    right: -60px; top: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: #FFFFFF;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
    text-transform: uppercase;
    backdrop-filter: blur(4px);
}
.hero h1 {
    color: #FFFFFF;
    font-size: 2.15rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem 0;
    line-height: 1.15;
}
.hero p {
    color: rgba(255, 255, 255, 0.92);
    font-size: 1.05rem;
    margin: 0;
    max-width: 720px;
    line-height: 1.55;
    overflow-wrap: anywhere;
}

/* KPI grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 210px), 1fr));
    gap: 1rem;
    margin: 0 0 2rem 0;
}
.kpi-card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.35rem 1.5rem;
    border-left: 4px solid var(--primary);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    transition: transform 0.15s, box-shadow 0.15s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
.kpi-card.accent  { border-left-color: var(--accent); }
.kpi-card.success { border-left-color: var(--success); }
.kpi-card.warning { border-left-color: var(--warning); }
.kpi-card.danger  { border-left-color: var(--danger); }
.kpi-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 700;
    margin-bottom: 0.55rem;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.05;
    letter-spacing: -0.02em;
    font-size: clamp(1.25rem, 3vw, 1.9rem);
    overflow-wrap: anywhere;
}
.kpi-delta {
    font-size: 0.8rem;
    color: var(--success);
    margin-top: 0.5rem;
    font-weight: 600;
}
.kpi-delta.danger { color: var(--danger); }

/* Section header */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid var(--border);
}
.section-header h2 {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.section-header .badge {
    background: var(--primary);
    color: #FFFFFF;
    font-size: 0.7rem;
    padding: 0.22rem 0.6rem;
    border-radius: 999px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Callouts */
.callout {
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    border-left: 4px solid;
    font-size: 0.95rem;
    line-height: 1.65;
    overflow-wrap: anywhere;
}
.callout-info    { background: #EFF6FF; border-color: #3B82F6; color: #1E3A8A; }
.callout-success { background: #F0FDF4; border-color: #10B981; color: #065F46; }
.callout-warning { background: #FFFBEB; border-color: #F59E0B; color: #78350F; }
.callout-danger  { background: #FEF2F2; border-color: #EF4444; color: #7F1D1D; }
.callout > :first-child { margin-top: 0; }
.callout > :last-child { margin-bottom: 0; }

/* Pills */
.pill {
    display: inline-block;
    padding: 0.22rem 0.65rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    margin: 0 0.25rem 0.25rem 0;
}
.pill-normal { background: #DBEAFE; color: #1E40AF; }
.pill-attack { background: #FEE2E2; color: #991B1B; }
.pill-ok     { background: #D1FAE5; color: #065F46; }
.pill-warn   { background: #FEF3C7; color: #78350F; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    padding: 0.7rem 1.15rem;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
    color: var(--text-muted);
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: #FFFFFF !important;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    padding: 0.55rem 1.15rem;
    transition: all 0.15s;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1E40AF, #06B6D4);
    border: none;
    box-shadow: 0 2px 6px rgba(30,64,175,0.25);
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(30,64,175,0.32);
}

/* st.metric */
[data-testid="stMetric"] {
    background: var(--card-bg);
    padding: 1rem 1.15rem;
    border-radius: 10px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
[data-testid="stMetricLabel"] p {
    font-size: 0.75rem !important;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
}
[data-testid="stMetricValue"] {
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--primary);
}

/* Dataframes e plots */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
}
[data-testid="stPlotlyChart"] {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 0.75rem;
    border: 1px solid var(--border);
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* Expander */
[data-testid="stExpander"] {
    border-radius: 10px;
    border: 1px solid var(--border);
    overflow: hidden;
}
[data-testid="stExpander"] summary { font-weight: 600; }

/* Footer */
.app-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--text-muted);
    font-size: 0.82rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    line-height: 1.7;
}
.app-footer strong { color: var(--text); }

@media (max-width: 640px) {
    .main .block-container { padding: 1rem 0.75rem 2rem; }
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 100% !important;
        width: 100% !important;
        min-width: 0 !important;
    }
    .stTabs [data-baseweb="tab-list"] { overflow-x: auto; }
    [data-testid="stMarkdownContainer"] { overflow-wrap: anywhere; }
    .hero { padding: 1.25rem; border-radius: 12px; }
    .hero h1 { font-size: clamp(1.5rem, 7vw, 2.15rem); }
    .hero p { font-size: 0.95rem; }
    .kpi-grid { gap: 0.75rem; margin-bottom: 1.25rem; }
    .kpi-card { padding: 1rem; }
    .section-header { margin-top: 1.5rem; }
    .section-header h2 { font-size: 1.15rem; overflow-wrap: anywhere; }
    .callout { padding: 0.85rem 1rem; }
    .app-footer { padding: 1.5rem 0.5rem 1rem; }
}

/* Scrollbar */
::-webkit-scrollbar       { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
</style>
"""


def inject_css() -> None:
    """Injeta o CSS do design system uma única vez por sessão."""
    st.html(_CSS)


def _e(v) -> str:
    return html.escape(str(v))


def page_header(icon: str, title: str, subtitle: str, badge: str | None = None) -> None:
    """Hero com gradiente no topo da página."""
    badge_html = f'<div class="badge">{_e(badge)}</div>' if badge else ""
    st.html(
        f"""
        <div class="hero">
            {badge_html}
            <h1>{_e(icon)} {_e(title)}</h1>
            <p>{_e(subtitle)}</p>
        </div>
        """,
    )


def kpi_grid(items: Iterable[dict]) -> None:
    """Grid de KPIs. Cada item: {label, value, delta?, tone?, delta_tone?}."""
    cards = []
    for item in items:
        tone       = item.get("tone", "primary")
        delta      = item.get("delta")
        delta_cls  = "kpi-delta danger" if item.get("delta_tone") == "danger" else "kpi-delta"
        delta_html = f'<div class="{delta_cls}">{_e(delta)}</div>' if delta else ""
        cards.append(
            f'<div class="kpi-card {_e(tone)}">'
            f'<div class="kpi-label">{_e(item["label"])}</div>'
            f'<div class="kpi-value">{_e(item["value"])}</div>'
            f'{delta_html}</div>'
        )
    st.html(f'<div class="kpi-grid">{"".join(cards)}</div>')


def section(title: str, badge: str | None = None) -> None:
    """Cabeçalho de seção com divisória."""
    badge_html = f'<span class="badge">{_e(badge)}</span>' if badge else ""
    st.html(
        f'<div class="section-header"><h2>{_e(title)}</h2>{badge_html}</div>',
    )


def callout(text: str, kind: str = "info") -> None:
    """Caixa colorida (info / success / warning / danger) — aceita markdown."""
    content = _MARKDOWN.render(textwrap.dedent(text).strip())
    st.html(
        f'<div class="callout callout-{_e(kind)}">{content}</div>',
    )


def pills(items: Iterable[tuple[str, str]]) -> None:
    """Lista de badges. items: [(texto, kind)]; kinds: normal, attack, ok, warn."""
    tags = "".join(f'<span class="pill pill-{_e(k)}">{_e(t)}</span>' for t, k in items)
    st.html(tags)


def page_footer() -> None:
    """Rodapé institucional."""
    st.html(
        """
        <div class="app-footer">
            <strong>IoT Guard</strong> · Detecção de Intrusão em Redes IoT ·
            Base <strong>RT-IoT2022</strong> (UCI id 942)<br>
            MBA em Ciência de Dados — Unifor · Turma 12 · Prof. Caio Ponte
        </div>
        """,
    )


def sidebar_brand() -> None:
    """Card de branding no topo da sidebar."""
    st.html(
        """
        <div style="padding: 0.5rem 0.25rem 1.25rem 0.25rem; text-align: center;">
            <div style="font-size: 2.2rem; line-height: 1;">🛡️</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;
                        margin-top: 0.4rem; letter-spacing: -0.01em;">
                IoT Guard
            </div>
            <div style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.25rem;
                        text-transform: uppercase; letter-spacing: 0.08em;">
                Detecção de Intrusão · IoT
            </div>
        </div>
        """,
    )
