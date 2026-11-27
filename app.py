from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================
# 1. PAGE CONFIGURATION + VISUAL SYSTEM
# ==========================================

st.set_page_config(
    page_title="NOCTURNE — Music Intelligence",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="expanded",
)

VIOLET = "#7547D8"
VIOLET_DARK = "#3B2A78"
CYAN = "#65D6E8"
LAVENDER = "#B69AFF"
INK = "#090711"
TEXT = "#F0E8FF"
MUTED = "#A99BC4"
GRID = "rgba(255,255,255,0.08)"

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
        --canvas: #090711;
        --surface: #171329;
        --surface-raised: #1C1733;
        --surface-glass: rgba(23, 19, 41, 0.76);
        --line: rgba(182, 154, 255, 0.12);
        --text: #F0E8FF;
        --muted: #A99BC4;
        --violet: #7547D8;
        --violet-soft: rgba(117, 71, 216, 0.12);
    }

    html { scroll-behavior: smooth; }
    .stApp {
        background:
            radial-gradient(ellipse at 82% 0%, rgba(117, 71, 216, 0.075), transparent 30%),
            linear-gradient(180deg, #0D0A1A 0%, var(--canvas) 38%, #090711 100%);
        color: var(--text);
    }
    [data-testid="stHeader"] { background: rgba(8, 11, 9, 0.45); }
    [data-testid="stAppViewContainer"] > .main > div {
        max-width: 1680px;
        padding-top: 1.55rem;
        padding-bottom: 3rem;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14102A 0%, #0B0916 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.35rem; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--muted); }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] { color: #E2D8F7; }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-rac][role="group"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-rac][role="group"],
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        color: var(--text) !important;
        background: rgba(255,255,255,0.035) !important;
        border-color: rgba(182, 154, 255, 0.16) !important;
        border-radius: 7px;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] {
        color: #E4DAFF !important;
        background: rgba(117, 71, 216, 0.15) !important;
        border-radius: 5px;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] * {
        color: #E4DAFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] input[role="combobox"],
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] input[role="combobox"] {
        color: var(--text) !important;
        caret-color: var(--violet);
    }
    [role="listbox"] {
        color: var(--text) !important;
        background: #1C1733 !important;
        border: 1px solid var(--line) !important;
    }
    [role="option"] { color: var(--text) !important; }
    [role="option"][aria-selected="true"] { background: rgba(117, 71, 216, 0.12) !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] span { color: var(--text); }
    [data-testid="stSidebar"] hr { border-color: var(--line); }

    h1, h2, h3, h4 { color: var(--text); letter-spacing: 0; }
    p, li, label { color: #CFC5E6; }
    a { color: var(--violet); }
    [data-testid="stCaptionContainer"] { color: var(--muted); }
    [data-testid="stPlotlyChart"] { margin-top: 0.1rem; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; }

    .side-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.15rem 0.25rem 1.35rem;
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.1rem;
    }
    .brand-mark {
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        color: #090711;
        background: linear-gradient(145deg, #B69AFF, var(--violet));
        box-shadow: 0 0 22px rgba(117, 71, 216, 0.20);
        font-size: 24px;
        font-weight: 800;
    }
    .brand-copy strong {
        display: block;
        color: var(--text);
        font-size: 13px;
        letter-spacing: 1.1px;
    }
    .brand-copy span {
        display: block;
        margin-top: 3px;
        color: var(--muted);
        font-size: 11px;
    }
    .side-label, .eyebrow {
        color: var(--violet);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.7px;
        text-transform: uppercase;
    }
    .side-nav { display: grid; gap: 4px; margin: 0.55rem 0 1.25rem; }
    .side-nav a {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        padding: 0.52rem 0.58rem;
        color: #BDB1D8;
        border-left: 2px solid transparent;
        border-radius: 0 6px 6px 0;
        font-size: 12px;
        text-decoration: none;
        transition: background 160ms ease, color 160ms ease, border-color 160ms ease;
    }
    .side-nav a:hover {
        color: var(--text);
        border-left-color: var(--violet);
        background: rgba(117, 71, 216, 0.07);
    }
    .side-footer {
        margin-top: 1.4rem;
        padding-top: 0.9rem;
        border-top: 1px solid var(--line);
        color: #7A6F94;
        font-size: 10px;
        letter-spacing: 0.8px;
    }

    .workspace-topline {
        display: flex;
        align-items: center;
        gap: 0.48rem;
        margin: 0.1rem 0 1.05rem;
        color: #8E82AA;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.4px;
    }
    .signal-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--violet);
        box-shadow: 0 0 12px rgba(117, 71, 216, 0.65);
    }
    .topline-spacer { flex: 1; }
    .dataset-pill {
        padding: 0.35rem 0.58rem;
        border: 1px solid rgba(117, 71, 216, 0.22);
        border-radius: 999px;
        color: #CFF4FA;
        background: rgba(117, 71, 216, 0.07);
        font-size: 9px;
        letter-spacing: 1px;
    }
    .hero-block {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1.5rem;
        padding: 0.2rem 0 1.55rem;
    }
    .hero-block h1 {
        margin: 0.52rem 0 0.35rem;
        color: var(--text);
        font-size: 43px;
        font-weight: 700;
        line-height: 1.06;
    }
    .hero-block p {
        max-width: 720px;
        margin: 0;
        color: #B3A8CC;
        font-size: 14px;
        line-height: 1.65;
    }
    .hero-aside {
        min-width: 170px;
        padding: 0.9rem 1rem;
        border-left: 1px solid rgba(117, 71, 216, 0.35);
        color: var(--muted);
        font-size: 10px;
        letter-spacing: 1.1px;
        text-transform: uppercase;
    }
    .hero-aside strong {
        display: block;
        margin-top: 0.4rem;
        color: var(--text);
        font-size: 19px;
        letter-spacing: 0;
        text-transform: none;
    }
    .hero-rule {
        height: 1px;
        margin-bottom: 1.45rem;
        background: linear-gradient(90deg, rgba(117,71,216,0.42), rgba(182,154,255,0.08) 68%, transparent);
    }

    .section-heading {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
        margin: 2.15rem 0 0.7rem;
        scroll-margin-top: 1rem;
    }
    .section-number {
        color: var(--violet);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.3px;
    }
    .section-title { color: var(--text); font-size: 17px; font-weight: 650; }
    .section-subtitle {
        margin-left: auto;
        color: #7F7499;
        font-size: 9px;
        letter-spacing: 1px;
        text-align: right;
        text-transform: uppercase;
    }
    .metric-card {
        position: relative;
        min-height: 135px;
        overflow: hidden;
        padding: 1.05rem 1.1rem 1rem;
        border: 1px solid rgba(182, 154, 255, 0.14);
        border-radius: 8px;
        background: linear-gradient(145deg, rgba(30, 24, 54, 0.83), rgba(17, 13, 32, 0.86));
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.035), 0 10px 28px rgba(0,0,0,0.12);
        backdrop-filter: blur(12px);
        transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
    }
    .metric-card::after {
        position: absolute;
        top: -35px;
        right: -26px;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: rgba(117, 71, 216, 0.055);
        content: "";
        filter: blur(22px);
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(117, 71, 216, 0.36);
        box-shadow: 0 12px 30px rgba(0,0,0,0.2), 0 0 20px rgba(117, 71, 216, 0.055);
    }
    .metric-top { display: flex; align-items: center; justify-content: space-between; }
    .metric-label {
        color: #B3A8CC;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.1px;
        text-transform: uppercase;
    }
    .metric-icon {
        display: grid;
        place-items: center;
        width: 27px;
        height: 27px;
        border: 1px solid rgba(117, 71, 216, 0.19);
        border-radius: 7px;
        color: var(--violet);
        background: rgba(117, 71, 216, 0.07);
        font-size: 13px;
    }
    .metric-value {
        position: relative;
        z-index: 1;
        margin-top: 0.72rem;
        color: var(--text);
        font-size: 26px;
        font-weight: 700;
        line-height: 1.1;
    }
    .metric-note { margin-top: 0.38rem; color: #8C81A6; font-size: 10px; }
    .chart-note {
        margin: -0.2rem 0 0.45rem;
        color: #877C9F;
        font-size: 10px;
    }
    .explorer-note {
        padding: 0.8rem 0.95rem;
        border-left: 2px solid rgba(117,71,216,0.58);
        background: rgba(255,255,255,0.025);
        color: #B3A8CC;
        font-size: 12px;
        line-height: 1.55;
    }
    div[data-testid="stDownloadButton"] button {
        border: 1px solid rgba(117, 71, 216, 0.35);
        border-radius: 7px;
        color: #090711;
        background: var(--violet);
        font-weight: 700;
        transition: filter 150ms ease, transform 150ms ease;
    }
    div[data-testid="stDownloadButton"] button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
    }
    .footer-line {
        margin-top: 2.4rem;
        padding-top: 1rem;
        border-top: 1px solid var(--line);
        color: #7A6F94;
        font-size: 10px;
        letter-spacing: 0.35px;
    }

    @media (max-width: 760px) {
        [data-testid="stAppViewContainer"] > .main > div { padding-top: 1rem; }
        .hero-block { align-items: flex-start; flex-direction: column; gap: 1rem; }
        .hero-block h1 { font-size: 34px; }
        .hero-aside { min-width: 0; padding: 0.5rem 0 0.5rem 0.75rem; }
        .section-heading { align-items: flex-start; flex-wrap: wrap; gap: 0.45rem 0.7rem; }
        .section-subtitle { width: 100%; margin-left: 0; text-align: left; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 2. HELPERS
# ==========================================


def fmt_num(value):
    if pd.isna(value):
        return "—"

    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def metric_card(label, value, note, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">{label}</div>
                <div class="metric-icon">{icon}</div>
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(number, title, subtitle, anchor):
    st.markdown(
        f"""
        <div id="{anchor}" class="section-heading">
            <span class="section-number">{number}</span>
            <span class="section-title">{title}</span>
            <span class="section-subtitle">{subtitle}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# NOCTURNE 3D LAYER
# ==========================================
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
html, body, .stApp, [class*="css"] { font-family: 'Sora', sans-serif; }
.stApp {
    background:
        radial-gradient(ellipse 60% 40% at 15% 0%, rgba(117,71,216,0.28), transparent 60%),
        radial-gradient(ellipse 50% 35% at 90% 10%, rgba(101,214,232,0.14), transparent 60%),
        radial-gradient(ellipse 70% 50% at 50% 110%, rgba(182,154,255,0.12), transparent 60%),
        #090711 !important;
}
.stApp::before {
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image:
        radial-gradient(1.5px 1.5px at 20% 30%, rgba(240,232,255,0.7), transparent),
        radial-gradient(1px 1px at 70% 20%, rgba(101,214,232,0.8), transparent),
        radial-gradient(1.5px 1.5px at 40% 80%, rgba(182,154,255,0.7), transparent),
        radial-gradient(1px 1px at 85% 65%, rgba(240,232,255,0.6), transparent),
        radial-gradient(1px 1px at 10% 70%, rgba(101,214,232,0.6), transparent);
    background-size: 600px 600px; animation: drift 60s linear infinite; opacity: 0.7;
}
.stApp::after {
    content: ""; position: fixed; top: -20%; left: -40%; width: 60%; height: 140%; pointer-events: none; z-index: 0;
    background: linear-gradient(100deg, transparent, rgba(182,154,255,0.06), rgba(101,214,232,0.05), transparent);
    transform: rotate(12deg); animation: streak 14s ease-in-out infinite;
}
@keyframes drift { from { background-position: 0 0; } to { background-position: 600px -600px; } }
@keyframes streak { 0%,100% { left: -60%; } 50% { left: 110%; } }
@keyframes pulse { 50% { opacity: 0.35; } }
.hero-block h1 {
    font-size: 54px !important; font-weight: 800 !important;
    background: linear-gradient(120deg, #F0E8FF 10%, #B69AFF 50%, #65D6E8 90%);
    -webkit-background-clip: text; background-clip: text; color: transparent !important;
}
.eyebrow, .side-label, .section-number { color: #65D6E8 !important; }
.signal-dot { background: #65D6E8 !important; box-shadow: 0 0 14px #65D6E8 !important; animation: pulse 2.4s ease-in-out infinite; }
.metric-card {
    transform-style: preserve-3d;
    transform: perspective(900px) rotateX(6deg) rotateY(-4deg);
    border: 1px solid rgba(182,154,255,0.22) !important;
    background: linear-gradient(150deg, rgba(36,28,66,0.85), rgba(17,13,32,0.9)) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 2px 4px rgba(0,0,0,0.3),
        0 18px 40px rgba(0,0,0,0.45), 0 30px 80px rgba(117,71,216,0.18) !important;
    transition: transform 400ms cubic-bezier(.2,.8,.2,1), box-shadow 400ms ease, border-color 400ms ease !important;
}
.metric-card::before {
    content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
    background: linear-gradient(120deg, rgba(255,255,255,0.10), transparent 40%);
}
.metric-card::after { background: rgba(101,214,232,0.18) !important; }
.metric-card:hover {
    transform: perspective(900px) rotateX(0) rotateY(0) translateY(-8px) scale(1.03) !important;
    border-color: rgba(101,214,232,0.55) !important;
    box-shadow: 0 30px 60px rgba(0,0,0,0.5), 0 0 40px rgba(117,71,216,0.35), 0 0 0 1px rgba(101,214,232,0.25) !important;
}
.metric-value { text-shadow: 0 0 18px rgba(182,154,255,0.45); font-size: 30px !important; }
.metric-icon { color: #65D6E8 !important; border-color: rgba(101,214,232,0.3) !important; background: rgba(101,214,232,0.08) !important; }
[data-testid="stPlotlyChart"] {
    padding: 0.6rem; border-radius: 16px;
    background: linear-gradient(160deg, rgba(30,24,54,0.7), rgba(13,10,26,0.75));
    border: 1px solid rgba(182,154,255,0.16);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 20px 50px rgba(0,0,0,0.45), 0 0 50px rgba(117,71,216,0.10);
    backdrop-filter: blur(14px); transition: transform 350ms ease, box-shadow 350ms ease;
}
[data-testid="stPlotlyChart"]:hover { transform: translateY(-4px); box-shadow: 0 28px 60px rgba(0,0,0,0.5), 0 0 60px rgba(117,71,216,0.22); }
[data-testid="stDataFrame"] { border-color: rgba(182,154,255,0.2) !important; box-shadow: 0 20px 50px rgba(0,0,0,0.4); border-radius: 14px !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(23,19,41,0.92), rgba(9,7,17,0.96)) !important;
    backdrop-filter: blur(18px); box-shadow: 10px 0 40px rgba(117,71,216,0.12);
}
.brand-mark { background: linear-gradient(145deg, #B69AFF, #7547D8 60%, #65D6E8) !important; color: #F0E8FF !important; box-shadow: 0 0 28px rgba(117,71,216,0.6) !important; }
.side-nav a:hover { border-left-color: #65D6E8 !important; }
.hero-rule { background: linear-gradient(90deg, #7547D8, #65D6E8 40%, transparent) !important; box-shadow: 0 0 12px rgba(117,71,216,0.6); }
.stDownloadButton button, .stButton button {
    background: linear-gradient(135deg, #7547D8, #B69AFF) !important; color: #F0E8FF !important;
    border: 0 !important; border-radius: 10px !important; box-shadow: 0 10px 30px rgba(117,71,216,0.4) !important;
}
@media (max-width: 768px) { .hero-block { flex-direction: column; align-items: flex-start; } .hero-block h1 { font-size: 36px !important; } }
</style>
    """,
    unsafe_allow_html=True,
)


def style_figure(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Sora, sans-serif", "color": TEXT, "size": 11},
        title={"x": 0, "xanchor": "left", "font": {"size": 15, "color": TEXT}},
        margin={"l": 8, "r": 10, "t": 58, "b": 12},
        height=height,
        hoverlabel={
            "bgcolor": "#1C1733",
            "bordercolor": "rgba(117,71,216,0.35)",
            "font": {"color": TEXT, "size": 11},
        },
    )
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(showgrid=False, zeroline=False, linecolor=GRID)
    return fig


def chart_message(message):
    st.info(message)


# ==========================================
# 3. LOAD + CLEAN THE DATASET
# ==========================================

@st.cache_data(show_spinner="Loading your music dataset…")
def load_data():
    file_path = Path(__file__).resolve().parent / "data" / "spotify.csv"
    if not file_path.exists():
        raise FileNotFoundError(
            "Dataset not found. Put spotify.csv inside a data folder next to app.py."
        )

    data = pd.read_csv(file_path, encoding="latin1", engine="python")
    data = data.drop_duplicates()
    data = data.dropna(axis=1, how="all")

    if "Artist" not in data.columns:
        raise ValueError("The dataset needs an 'Artist' column for the dashboard filters.")
    data = data.dropna(subset=["Artist"])

    if "Release Date" in data.columns:
        data["Release Date"] = pd.to_datetime(data["Release Date"], errors="coerce")

    numeric_columns = [
        "All Time Rank",
        "Track Score",
        "Spotify Streams",
        "Spotify Playlist Count",
        "Spotify Playlist Reach",
        "Spotify Popularity",
        "YouTube Views",
        "YouTube Likes",
        "TikTok Posts",
        "TikTok Likes",
        "TikTok Views",
        "YouTube Playlist Reach",
        "Apple Music Playlist Count",
        "AirPlay Spins",
        "SiriusXM Spins",
        "Deezer Playlist Count",
        "Deezer Playlist Reach",
        "Amazon Playlist Count",
        "Pandora Streams",
        "Pandora Track Stations",
        "Soundcloud Streams",
        "Shazam Counts",
        "TIDAL Popularity",
        "Explicit Track",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column].astype("string").str.replace(",", "", regex=False),
                errors="coerce",
            )

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()


# ==========================================
# 4. SIDEBAR + FILTERS
# ==========================================

st.sidebar.markdown(
    """
    <div class="side-brand">
        <div class="brand-mark">♫</div>
        <div class="brand-copy">
            <strong>NOCTURNE</strong>
            <span>Music intelligence</span>
        </div>
    </div>
    <div class="side-label">Workspace</div>
    <nav class="side-nav">
        <a href="#overview">◈ &nbsp; Overview</a>
        <a href="#performance">▤ &nbsp; Performance</a>
        <a href="#platforms">⇄ &nbsp; Platforms</a>
        <a href="#engagement">◉ &nbsp; Engagement</a>
        <a href="#correlations">⌘ &nbsp; Correlations</a>
        <a href="#explorer">▦ &nbsp; Data explorer</a>
    </nav>
    <div class="side-label">Refine the view</div>
    """,
    unsafe_allow_html=True,
)

filtered = df.copy()

if "Release Date" in filtered.columns:
    filtered["Release Year"] = filtered["Release Date"].dt.year
    years = sorted(filtered["Release Year"].dropna().unique().tolist())
    if years:
        selected_years = st.sidebar.multiselect(
            "Release year",
            options=years,
            default=years,
            placeholder="All release years",
        )
        if selected_years:
            filtered = filtered[filtered["Release Year"].isin(selected_years)]
else:
    st.sidebar.caption("Release year is unavailable: no Release Date column.")

artists = sorted(filtered["Artist"].dropna().astype(str).unique().tolist())
selected_artist = st.sidebar.selectbox("Artist", ["All artists"] + artists)
if selected_artist != "All artists":
    filtered = filtered[filtered["Artist"].astype(str) == selected_artist]

if "Explicit Track" in filtered.columns:
    track_type = st.sidebar.selectbox(
        "Track content",
        ["All tracks", "Explicit", "Non-explicit"],
    )
    if track_type == "Explicit":
        filtered = filtered[filtered["Explicit Track"] == 1]
    elif track_type == "Non-explicit":
        filtered = filtered[filtered["Explicit Track"] == 0]
else:
    st.sidebar.caption("Track content filter is unavailable in this dataset.")

st.sidebar.markdown(
    '<div class="side-footer">NOCTURNE &nbsp;·&nbsp; DATA EXPLORATION</div>',
    unsafe_allow_html=True,
)


# ==========================================
# 5. DASHBOARD HEADER
# ==========================================

st.markdown(
    f"""
    <div id="overview" class="workspace-topline">
        <span class="signal-dot"></span>
        <span>MUSIC INTELLIGENCE</span>
        <span>/</span>
        <span>ANALYTICS WORKSPACE</span>
        <span class="topline-spacer"></span>
        <span class="dataset-pill">LIVE DATASET</span>
    </div>
    <div class="hero-block">
        <div>
            <div class="eyebrow">SPOTIFY · MULTI-PLATFORM SIGNALS</div>
            <h1>Music, measured.</h1>
            <p>One clear view of track momentum, artist performance and audience engagement across platforms.</p>
        </div>
        <div class="hero-aside">Track universe<strong>{fmt_num(len(df))} records</strong></div>
    </div>
    <div class="hero-rule"></div>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No records match the selected filters. Adjust your filters to continue.")
    st.stop()


# ==========================================
# 6. FOUR KEY PERFORMANCE INDICATORS
# ==========================================

c1, c2, c3, c4 = st.columns(4, gap="medium")

with c1:
    metric_card("Tracks analysed", fmt_num(len(filtered)), "Records in current view", "♫")

with c2:
    total_streams = (
        filtered["Spotify Streams"].sum(min_count=1)
        if "Spotify Streams" in filtered.columns
        else np.nan
    )
    metric_card("Spotify streams", fmt_num(total_streams), "Total recorded streams", "↗")

with c3:
    average_score = (
        filtered["Track Score"].mean()
        if "Track Score" in filtered.columns
        else np.nan
    )
    score_label = f"{average_score:.1f}" if pd.notna(average_score) else "—"
    metric_card("Average track score", score_label, "Mean score across selected tracks", "✳")

with c4:
    metric_card(
        "Artists represented",
        fmt_num(filtered["Artist"].nunique()),
        "Unique artists in current view",
        "◎",
    )


# ==========================================
# 7. PERFORMANCE OVERVIEW
# ==========================================

section_header("01", "Performance overview", "TRACK RANKING · ARTIST MOMENTUM", "performance")
left, right = st.columns(2, gap="large")

with left:
    if {"Track", "Spotify Streams"}.issubset(filtered.columns):
        top_tracks = (
            filtered.dropna(subset=["Spotify Streams"])
            .nlargest(10, "Spotify Streams")
            .sort_values("Spotify Streams", ascending=True)
        )
        if not top_tracks.empty:
            hover_fields = [column for column in ["Artist", "Track Score"] if column in top_tracks.columns]
            fig = px.bar(
                top_tracks,
                x="Spotify Streams",
                y="Track",
                orientation="h",
                color="Spotify Streams",
                color_continuous_scale=[VIOLET_DARK, VIOLET],
                hover_data=hover_fields,
                title="Top tracks by Spotify streams",
            )
            fig.update_layout(coloraxis_showscale=False)
            style_figure(fig, 440)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            chart_message("No Spotify stream values are available in this selection.")
    else:
        chart_message("Top-track ranking needs both Track and Spotify Streams columns.")

with right:
    artist_aggregations = {
        "Tracks": ("Track", "count") if "Track" in filtered.columns else ("Artist", "size")
    }
    if "Spotify Streams" in filtered.columns:
        artist_aggregations["Spotify Streams"] = ("Spotify Streams", "sum")
    if "Track Score" in filtered.columns:
        artist_aggregations["Average track score"] = ("Track Score", "mean")

    artist_stats = filtered.groupby("Artist", dropna=True).agg(**artist_aggregations).reset_index()
    performance_column = "Spotify Streams" if "Spotify Streams" in artist_stats.columns else "Tracks"
    artist_top = artist_stats.nlargest(10, performance_column).sort_values(performance_column)
    artist_hover = [
        column for column in ["Tracks", "Average track score"] if column in artist_top.columns
    ]

    fig = px.bar(
        artist_top,
        x=performance_column,
        y="Artist",
        orientation="h",
        color=performance_column,
        color_continuous_scale=[VIOLET_DARK, VIOLET],
        hover_data=artist_hover,
        title=(
            "Artist performance · total Spotify streams"
            if performance_column == "Spotify Streams"
            else "Artists with most tracks"
        ),
    )
    fig.update_layout(coloraxis_showscale=False)
    style_figure(fig, 440)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ==========================================
# 8. PLATFORM RELATIONSHIPS
# ==========================================

section_header("02", "Platform relationships", "SPOTIFY · YOUTUBE · TRACK SIGNALS", "platforms")
left, right = st.columns(2, gap="large")

with left:
    if {"Spotify Streams", "Track Score"}.issubset(filtered.columns):
        score_data = filtered.dropna(subset=["Spotify Streams", "Track Score"]).copy()
        score_data = score_data[score_data["Spotify Streams"] > 0]
        if "Explicit Track" in score_data.columns:
            score_data["Track content"] = score_data["Explicit Track"].map(
                {0: "Non-explicit", 1: "Explicit"}
            )
            color_column = "Track content" if score_data["Track content"].notna().any() else None
        else:
            color_column = None

        if not score_data.empty:
            fig = px.scatter(
                score_data,
                x="Spotify Streams",
                y="Track Score",
                color=color_column,
                color_discrete_map={"Non-explicit": CYAN, "Explicit": VIOLET},
                hover_name="Track" if "Track" in score_data.columns else None,
                hover_data=["Artist"] if "Artist" in score_data.columns else None,
                opacity=0.74,
                title="Track score vs Spotify streams",
            )
            fig.update_xaxes(type="log", title="Spotify streams · log scale")
            fig.update_yaxes(title="Track score")
            style_figure(fig, 400)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            chart_message("No positive Spotify stream values are available for this comparison.")
    else:
        chart_message("This comparison needs Spotify Streams and Track Score columns.")

with right:
    if {"Spotify Streams", "YouTube Views"}.issubset(filtered.columns):
        cross_platform = filtered.dropna(subset=["Spotify Streams", "YouTube Views"]).copy()
        cross_platform = cross_platform[
            (cross_platform["Spotify Streams"] > 0) & (cross_platform["YouTube Views"] > 0)
        ]
        if "Explicit Track" in cross_platform.columns:
            cross_platform["Track content"] = cross_platform["Explicit Track"].map(
                {0: "Non-explicit", 1: "Explicit"}
            )
            color_column = "Track content" if cross_platform["Track content"].notna().any() else None
        else:
            color_column = None

        if not cross_platform.empty:
            fig = px.scatter(
                cross_platform,
                x="Spotify Streams",
                y="YouTube Views",
                color=color_column,
                color_discrete_map={"Non-explicit": CYAN, "Explicit": VIOLET},
                hover_name="Track" if "Track" in cross_platform.columns else None,
                hover_data=["Artist"] if "Artist" in cross_platform.columns else None,
                opacity=0.72,
                title="Spotify streams vs YouTube views",
            )
            fig.update_xaxes(type="log", title="Spotify streams · log scale")
            fig.update_yaxes(type="log", title="YouTube views · log scale")
            style_figure(fig, 400)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                '<div class="chart-note">Log scales make cross-platform performance easier to compare across very different audience sizes.</div>',
                unsafe_allow_html=True,
            )
        else:
            chart_message("No positive Spotify and YouTube values overlap in this selection.")
    else:
        chart_message("This comparison needs Spotify Streams and YouTube Views columns.")


# ==========================================
# 9. ENGAGEMENT ANALYTICS
# ==========================================

section_header("03", "Engagement analytics", "AUDIENCE RESPONSE · CONTENT MIX", "engagement")
left, right = st.columns(2, gap="large")

with left:
    if {"YouTube Likes", "YouTube Views"}.issubset(filtered.columns):
        engagement = filtered.dropna(subset=["YouTube Likes", "YouTube Views"]).copy()
        engagement = engagement[engagement["YouTube Views"] > 0]
        engagement["YouTube like rate"] = (
            engagement["YouTube Likes"] / engagement["YouTube Views"] * 100
        )
        if "Track" in engagement.columns:
            name_column = "Track"
        elif "Artist" in engagement.columns:
            name_column = "Artist"
        else:
            engagement["Record"] = engagement.index.astype(str)
            name_column = "Record"

        top_engagement = (
            engagement.nlargest(10, "YouTube like rate")
            .sort_values("YouTube like rate", ascending=True)
        )
        if not top_engagement.empty:
            hover_fields = [
                column
                for column in ["Artist", "YouTube Likes", "YouTube Views"]
                if column in top_engagement.columns and column != name_column
            ]
            fig = px.bar(
                top_engagement,
                x="YouTube like rate",
                y=name_column,
                orientation="h",
                color="YouTube like rate",
                color_continuous_scale=[VIOLET_DARK, VIOLET],
                hover_data=hover_fields,
                title="YouTube like rate · top tracks",
                labels={"YouTube like rate": "Likes / views (%)"},
            )
            fig.update_layout(coloraxis_showscale=False)
            style_figure(fig, 410)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            chart_message("No YouTube records with views are available in this selection.")
    elif "YouTube Likes" in filtered.columns:
        likes = filtered.dropna(subset=["YouTube Likes"]).nlargest(10, "YouTube Likes")
        if "Track" in likes.columns and not likes.empty:
            likes = likes.sort_values("YouTube Likes")
            fig = px.bar(
                likes,
                x="YouTube Likes",
                y="Track",
                orientation="h",
                color_discrete_sequence=[VIOLET],
                hover_data=["Artist"] if "Artist" in likes.columns else None,
                title="Most-liked tracks on YouTube",
            )
            style_figure(fig, 410)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            chart_message("YouTube Likes values or track labels are unavailable in this selection.")
    else:
        chart_message("Engagement ranking needs YouTube Likes and YouTube Views columns.")

with right:
    if "Explicit Track" in filtered.columns:
        content_mix = (
            filtered["Explicit Track"]
            .map({0: "Non-explicit", 1: "Explicit"})
            .fillna("Unknown")
            .value_counts()
            .rename_axis("Track type")
            .reset_index(name="Tracks")
        )
        fig = px.pie(
            content_mix,
            names="Track type",
            values="Tracks",
            hole=0.68,
            color="Track type",
            color_discrete_map={
                "Non-explicit": CYAN,
                "Explicit": VIOLET,
                "Unknown": "#5E5578",
            },
            title="Explicit content distribution",
        )
        fig.update_traces(textposition="inside", textinfo="percent+label", marker_line_color=INK, marker_line_width=2)
        style_figure(fig, 410)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        chart_message("Content mix is unavailable because the dataset has no Explicit Track column.")


# ==========================================
# 10. CORRELATION INTELLIGENCE
# ==========================================

section_header("04", "Correlation intelligence", "METRIC RELATIONSHIPS · NOT CAUSATION", "correlations")
correlation_candidates = [
    "Track Score",
    "Spotify Streams",
    "Spotify Playlist Count",
    "Spotify Popularity",
    "YouTube Views",
    "YouTube Likes",
    "TikTok Posts",
    "TikTok Likes",
    "TikTok Views",
    "Apple Music Playlist Count",
    "Deezer Playlist Count",
]
correlation_columns = [
    column
    for column in correlation_candidates
    if column in filtered.columns and filtered[column].nunique(dropna=True) > 1
]

if len(correlation_columns) >= 2:
    correlation = filtered[correlation_columns].corr().fillna(0)
    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=[LAVENDER, "#1C1733", VIOLET],
        color_continuous_midpoint=0,
        zmin=-1,
        zmax=1,
        title="How the music signals move together",
    )
    fig.update_layout(coloraxis_colorbar={"title": "Correlation", "thickness": 11})
    style_figure(fig, 550)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        '<div class="chart-note">Correlation describes association between metrics; it does not establish cause and effect.</div>',
        unsafe_allow_html=True,
    )
else:
    chart_message("At least two varying numeric metrics are needed to calculate correlations.")


# ==========================================
# 11. RAW DATA EXPLORER + DOWNLOAD
# ==========================================

section_header("05", "Data explorer", "FILTERED RECORDS · CSV EXPORT", "explorer")
left, right = st.columns([1.5, 1], vertical_alignment="center")
with left:
    st.markdown(
        f'<div class="explorer-note">Showing <strong>{fmt_num(len(filtered))}</strong> records after the selected filters. Open the table to inspect individual rows.</div>',
        unsafe_allow_html=True,
    )
with right:
    st.download_button(
        "Download filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="spotify_insights_filtered.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary",
    )

with st.expander("Open filtered dataset", expanded=False):
    st.dataframe(filtered, use_container_width=True, height=430, hide_index=True)


# ==========================================
# 12. FOOTER
# ==========================================

st.markdown(
    '<div class="footer-line">NOCTURNE &nbsp;·&nbsp; NOCTURNE &nbsp;·&nbsp; Built with Python, Pandas, Streamlit and Plotly</div>',
    unsafe_allow_html=True,
)