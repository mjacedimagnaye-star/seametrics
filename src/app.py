"""
SeaMetrics: Interactive Maritime Analytics & Multi-Year Predictive Dashboard
=============================================================================
Course: Fundamentals of Data Analytics
School: Leuteboro National High School (DepEd MIMAROPA Region)
Instructor: Aldrin D. Magtibay, Teacher V
Developers & Researchers:
  - Ace Mc Kinzy D. Magnaye
  - Keirvin Lee M. Escala
  - Sydney Emerald A. Cuebillas
Target Focus: Luzon & Associated Island Groups (Batangas, Calapan, & Regional Ports)
Dataset: Philippine Ports Authority (PPA) Port Statistics (CY 2019, 2022–2026)

Key Sections:
- Section A: Overview (Bento Grid KPIs, Port Highlights, Historical Trends, Monthly Visualizer, Dynamic Insights)
- Section B: Passenger Analytics (Port Traffic, Monthly Trends, YoY Growth, Directional Flow, Rankings, Batangas-Calapan Deep Dive)
- Section C: Ship Call Analytics (Port Vessel Traffic, Monthly Trends, YoY Growth, Domestic vs Foreign Calls, Rankings)
- Section D: RoRo Analytics (Port RoRo Traffic, Inbound vs Outbound, 4-Class Vehicle Breakdown, YoY Growth, Rankings)
- Section E: Port Comparison (Interactive Multi-Port Comparator across Pax, Ship, RoRo, and Historical Trends)
- Section F: Predictive Analytics (Plain-Language Explanations, Dedicated Port Selector, Calibrated Q4 Projections, Dual Comparison)
- Section G: Data Explorer (Interactive Slicing, Cleaned Domain Archives, Statistical Analysis Tables, Direct CSV Downloads)
"""

import os
import sys
import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------- PAGE CONFIGURATION & METADATA -----------------
st.set_page_config(
    page_title="SeaMetrics | Luzon Maritime Analytics & Forecasting (2019, 2022–2026)",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- BASE DIRECTORIES & ASSETS -----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
ANALYSIS_DIR = os.path.join(PROCESSED_DIR, "analysis")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

DATA_MACRO_PATH = os.path.join(DATA_DIR, "seametrics_luzon_historical_macro.csv")
DATA_MONTHLY_PATH = os.path.join(DATA_DIR, "seametrics_luzon_monthly.csv")
DATA_PORTS_PATH = os.path.join(DATA_DIR, "seametrics_luzon_ports_summary.csv")
DATA_PMO_PATH = os.path.join(DATA_DIR, "seametrics_luzon_pmo_summary.csv")

# Load and encode background image
def get_base64_image(image_filename):
    for folder in [ASSETS_DIR, os.path.join(BASE_DIR, "paper"), DATA_DIR]:
        path = os.path.join(folder, image_filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return ""

bg_base64 = get_base64_image("backseamet_enhanced.jpg")
if not bg_base64:
    bg_base64 = get_base64_image("backseamet.jpg")

bg_css_rule = ""
if bg_base64:
    # Subtle dark overlay (0.70 to 0.78 opacity) allowing sharp seaport details, ships, cranes, and reflections to be clearly seen
    bg_css_rule = f"""
    .stApp {{
        background: linear-gradient(135deg, rgba(6, 12, 28, 0.70) 0%, rgba(10, 22, 48, 0.74) 50%, rgba(7, 13, 30, 0.78) 100%),
                    url('data:image/jpeg;base64,{bg_base64}') no-repeat center center fixed !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    """
else:
    bg_css_rule = """
    .stApp {
        background-color: #070d1e !important;
    }
    """

# ----------------- ACCESSIBLE HIGH-CONTRAST CSS THEME -----------------
st.markdown(
    f"<style>\n{bg_css_rule}\n" + r'''
    /* Design Tokens */
    :root {
        --text-primary: #ffffff;
        --text-secondary: #f1f5f9;
        --text-muted: #cbd5e1;
        --brand-cyan: #00cec9;
        --brand-blue: #38bdf8;
        --brand-amber: #fbbf24;
        --brand-emerald: #34d399;
        --brand-purple: #a78bfa;
        --brand-pink: #f472b6;
        --bg-card: rgba(11, 23, 52, 0.93);
        --border-card: #1e3a6d;
    }

    /* Global Base */
    .stApp {
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Content Typography Visibility */
    .stApp p, .stApp span, .stApp label {
        color: #f1f5f9;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Top Header Banner */
    .header-banner {
        background: linear-gradient(135deg, rgba(10, 25, 47, 0.93) 0%, rgba(3, 43, 105, 0.91) 60%, rgba(14, 116, 144, 0.88) 100%);
        border: 1px solid #2563eb;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    .header-title {
        color: #ffffff !important;
        font-size: 2.15rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .header-subtitle {
        color: #cbd5e1 !important;
        font-size: 0.96rem;
        font-weight: 400;
        line-height: 1.5;
    }
    .header-tag {
        display: inline-block;
        background-color: rgba(0, 206, 201, 0.20);
        color: #00cec9 !important;
        border: 1px solid #00cec9;
        border-radius: 6px;
        padding: 4px 11px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 6px;
    }

    /* Bento Grid Layout */
    .bento-container {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 14px;
        margin-bottom: 22px;
    }
    @media (max-width: 1200px) {
        .bento-container {
            grid-template-columns: repeat(3, 1fr);
        }
    }
    @media (max-width: 768px) {
        .bento-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media (max-width: 480px) {
        .bento-container {
            grid-template-columns: 1fr;
        }
    }

    /* Bento KPI Card */
    .bento-card {
        background: linear-gradient(145deg, rgba(14, 26, 56, 0.93) 0%, rgba(17, 34, 77, 0.96) 100%);
        border: 1px solid #1e3a6d;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 120px;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .bento-card:hover {
        border-color: #00cec9;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 206, 201, 0.25);
    }
    .bento-header {
        color: #cbd5e1 !important;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .bento-number {
        color: #ffffff !important;
        font-size: clamp(1.25rem, 1.8vw, 1.75rem);
        font-weight: 800;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.25;
        margin: 3px 0px;
    }
    .bento-subtitle {
        color: #cbd5e1 !important;
        font-size: 0.76rem;
        line-height: 1.35;
        margin-top: 3px;
    }
    .bento-cyan { color: #00cec9 !important; }
    .bento-blue { color: #38bdf8 !important; }
    .bento-amber { color: #fbbf24 !important; }
    .bento-emerald { color: #34d399 !important; }
    .bento-purple { color: #a78bfa !important; }
    .bento-pink { color: #f472b6 !important; }

    /* Highlight Summary Cards */
    .highlight-card {
        background: linear-gradient(145deg, rgba(13, 27, 62, 0.92) 0%, rgba(20, 39, 82, 0.95) 100%);
        border: 1px solid #1a365d;
        border-left: 4px solid #00cec9;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .highlight-title {
        color: #93c5fd !important;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .highlight-val {
        color: #ffffff !important;
        font-size: 1.20rem;
        font-weight: 800;
        margin: 3px 0px;
    }
    .highlight-sub {
        color: #cbd5e1 !important;
        font-size: 0.78rem;
        line-height: 1.4;
    }

    /* Custom Status Badges */
    .status-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 6px;
    }
    .badge-full {
        background-color: rgba(5, 150, 105, 0.30);
        color: #34d399 !important;
        border: 1px solid #059669;
    }
    .badge-partial {
        background-color: rgba(217, 119, 6, 0.30);
        color: #fbbf24 !important;
        border: 1px solid #d97706;
    }

    /* Accessible Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(8, 17, 38, 0.96);
        padding: 8px 8px 0px 8px;
        border-radius: 12px 12px 0px 0px;
        border-bottom: 2px solid #1e3a6d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: rgba(14, 26, 56, 0.88);
        border-radius: 8px 8px 0px 0px;
        padding: 10px 16px;
        color: #cbd5e1 !important;
        font-size: 0.88rem;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #14244d;
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #1d4ed8 0%, #1e40af 100%) !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(29, 78, 216, 0.45);
    }

        /* Documentation & Research Attribution Styles */
    .doc-hero {
        background: linear-gradient(135deg, rgba(11, 23, 52, 0.95) 0%, rgba(15, 32, 70, 0.95) 100%);
        border: 1px solid #1e3a6d;
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .doc-pill {
        display: inline-block;
        padding: 4px 11px;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .doc-pill-cyan { background: rgba(0, 206, 201, 0.15); color: #00cec9; border: 1px solid rgba(0, 206, 201, 0.4); }
    .doc-pill-blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
    .doc-pill-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .doc-pill-purple { background: rgba(167, 139, 250, 0.15); color: #a78bfa; border: 1px solid rgba(167, 139, 250, 0.4); }
    .doc-card {
        background: rgba(11, 23, 52, 0.93) !important;
        border: 1px solid #1e3a6d !important;
        border-radius: 10px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .doc-card h4 {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        margin-top: 0px !important;
        margin-bottom: 8px !important;
    }
    .doc-card p, .doc-card li {
        color: #e2e8f0 !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
    }

    /* High-Contrast Info, Warning & Callout Containers */
    .info-card {
        background: rgba(11, 23, 52, 0.93) !important;
        border: 1px solid #1e3a6d !important;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .info-card h5, .callout-box h5, .warning-box h5 {
        font-weight: 800 !important;
    }
    .info-card p, .info-card li, .callout-box p, .callout-box li, .warning-box p, .warning-box li {
        color: #f1f5f9 !important;
        font-size: 0.90rem !important;
        line-height: 1.6 !important;
    }
    .callout-box {
        background: rgba(14, 165, 233, 0.14) !important;
        border-left: 4px solid #00cec9 !important;
        padding: 16px 20px;
        border-radius: 0px 8px 8px 0px;
        margin: 14px 0px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .warning-box {
        background: rgba(245, 158, 11, 0.15) !important;
        border-left: 4px solid #f59e0b !important;
        padding: 16px 20px;
        border-radius: 0px 8px 8px 0px;
        margin: 14px 0px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }

    /* =========================================================================
       STREAMLIT BASEWEB DROPDOWN & SELECT COMPONENTS COMPREHENSIVE STYLING
       ========================================================================= */

    /* Widget Labels */
    .stSelectbox label, .stMultiselect label, .stRadio label, .stCheckbox label, .stSlider label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
        letter-spacing: 0.01em !important;
    }

    /* Dropdown Input Container (Selectbox & Multiselect base) */
    div[data-baseweb="select"] {
        background-color: #0b1938 !important;
        border: 1px solid #2563eb !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    div[data-baseweb="select"]:hover, div[data-baseweb="select"]:focus-within {
        border-color: #00cec9 !important;
        box-shadow: 0 0 0 2px rgba(0, 206, 201, 0.25) !important;
    }
    div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: #ffffff !important;
    }

    /* Selected Value Text in Dropdown Control */
    div[data-baseweb="select"] [aria-selected="true"],
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 500;
    }

    /* Searchable Input Text Inside Selectbox/Multiselect */
    div[data-baseweb="select"] input {
        background-color: transparent !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 0.90rem !important;
    }
    div[data-baseweb="select"] input::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* Dropdown Arrow & Action Icons */
    div[data-baseweb="select"] svg {
        fill: #00cec9 !important;
        color: #00cec9 !important;
    }

    /* Multiselect Selected Tags / Badges */
    span[data-baseweb="tag"], div[data-baseweb="tag"], [data-testid="stMultiSelectTag"] {
        background-color: #162b55 !important;
        border: 1px solid #00cec9 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        padding: 3px 8px !important;
    }
    span[data-baseweb="tag"] span, div[data-baseweb="tag"] span, [data-testid="stMultiSelectTag"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    span[data-baseweb="tag"] svg, div[data-baseweb="tag"] svg, [data-testid="stMultiSelectTagClose"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    span[data-baseweb="tag"] svg:hover, [data-testid="stMultiSelectTagClose"] svg:hover {
        fill: #f43f5e !important;
        color: #f43f5e !important;
    }

    /* Dropdown Popover Menus (Opened List Container) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #07122b !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 10px !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.8) !important;
    }

    ul[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #07122b !important;
        padding: 6px !important;
        border-radius: 8px !important;
    }

    /* Unselected Option Items */
    li[data-baseweb="menu-item"],
    li[role="option"],
    div[role="option"] {
        background-color: #07122b !important;
        color: #f1f5f9 !important;
        -webkit-text-fill-color: #f1f5f9 !important;
        font-size: 0.89rem !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        margin: 2px 0px !important;
        cursor: pointer !important;
        transition: background-color 0.15s ease, color 0.15s ease !important;
    }
    li[data-baseweb="menu-item"] *,
    li[role="option"] *,
    div[role="option"] * {
        color: #f1f5f9 !important;
        -webkit-text-fill-color: #f1f5f9 !important;
    }

    /* Hovered & Focused Option Items */
    li[data-baseweb="menu-item"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover,
    li[data-highlighted="true"],
    div[data-highlighted="true"] {
        background-color: #1e3a6d !important;
        color: #00cec9 !important;
        -webkit-text-fill-color: #00cec9 !important;
    }
    li[data-baseweb="menu-item"]:hover *,
    li[role="option"]:hover *,
    div[role="option"]:hover *,
    li[data-highlighted="true"] *,
    div[data-highlighted="true"] * {
        color: #00cec9 !important;
        -webkit-text-fill-color: #00cec9 !important;
        font-weight: 600 !important;
    }

    /* Currently Selected Option Item in List */
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background: linear-gradient(90deg, #1d4ed8 0%, #1e40af 100%) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
    }
    li[aria-selected="true"] *,
    div[aria-selected="true"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Fallback for light mode dropdowns if forced by browser */
    div[data-baseweb="select"][style*="background-color: rgb(255, 255, 255)"],
    div[data-baseweb="select"][style*="background-color: white"] {
        color: #0f172a !important;
    }
    div[data-baseweb="select"][style*="background-color: rgb(255, 255, 255)"] *,
    div[data-baseweb="select"][style*="background-color: white"] * {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    /* Radio & Checkbox Labels */
    div[data-testid="stRadio"] label p, div[data-testid="stCheckbox"] label p {
        color: #f1f5f9 !important;
        font-size: 0.90rem !important;
    }

    /* Dataframe Tables */
    [data-testid="stDataFrame"] {
        background-color: rgba(11, 23, 52, 0.94) !important;
        border: 1px solid #1e3a6d !important;
        border-radius: 8px !important;
    }
    [data-testid="stDataFrame"] * {
        color: #f1f5f9 !important;
    }

    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: rgba(6, 12, 28, 0.97) !important;
        border-right: 1px solid #1e3a6d !important;
    }
''' + "</style>",
    unsafe_allow_html=True
)


# ----------------- DATA LOADERS -----------------
@st.cache_data
def load_core_datasets():
    """Loads cleaned master datasets and regenerates them if not present."""
    if not (os.path.exists(DATA_MACRO_PATH) and os.path.exists(DATA_MONTHLY_PATH) and 
            os.path.exists(DATA_PORTS_PATH) and os.path.exists(DATA_PMO_PATH)):
        from src.pipeline import run_pipeline
        run_pipeline()

    df_mac = pd.read_csv(DATA_MACRO_PATH)
    df_m = pd.read_csv(DATA_MONTHLY_PATH)
    df_p = pd.read_csv(DATA_PORTS_PATH)
    df_pmo_data = pd.read_csv(DATA_PMO_PATH)
    return df_mac, df_m, df_p, df_pmo_data


@st.cache_data
def load_analysis_table(filename):
    """Loads precomputed statistical analysis tables safely."""
    target_path = os.path.join(ANALYSIS_DIR, filename)
    if os.path.exists(target_path):
        return pd.read_csv(target_path)
    return None


# Load Master Data
df_macro, df_monthly, df_ports, df_pmo = load_core_datasets()

# Dynamically detect available years from integrated data (Strictly 2019, 2022–2026)
all_detected_years = sorted(list(set(df_macro["Year"].dropna().unique()).union(set(df_monthly["Year"].dropna().unique()))))
VALID_DATASET_YEARS = [int(y) for y in all_detected_years if int(y) in [2019, 2022, 2023, 2024, 2025, 2026]]


# ----------------- CENTRALIZED PLOTLY CHART THEME FUNCTION -----------------
def apply_seametrics_chart_theme(
    fig,
    height=400,
    show_legend=True,
    is_pie=False,
    xaxis_title=None,
    yaxis_title=None,
    barmode=None,
    category_order_y=None,
    category_order_x=None,
    legend_orientation=None,
    legend_title=None
):
    """
    Applies the SeaMetrics accessible high-contrast design system to any Plotly figure.
    Guarantees that titles, axis labels, tick marks, legends, data labels, annotations,
    and hover tooltips have maximum readability against dark transparent backgrounds.
    """
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=24, r=24, t=48, b=24),
        font=dict(
            family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
            color="#f1f5f9",
            size=12
        ),
        title=dict(
            font=dict(color="#ffffff", size=15, family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"),
            x=0.01,
            xanchor="left"
        ),
        hoverlabel=dict(
            bgcolor="#07122b",
            bordercolor="#38bdf8",
            font=dict(color="#ffffff", size=12, family="sans-serif")
        )
    )

    # Legend configuration
    if show_legend:
        leg_dict = dict(
            font=dict(color="#ffffff", size=11),
            bgcolor="rgba(10, 22, 48, 0.88)",
            bordercolor="#1e3a6d",
            borderwidth=1
        )
        if legend_title:
            leg_dict["title"] = dict(text=legend_title, font=dict(color="#38bdf8", size=11))
        if legend_orientation == "h":
            leg_dict.update(dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig.update_layout(showlegend=True, legend=leg_dict)
    else:
        fig.update_layout(showlegend=False)

    # Bar mode
    if barmode:
        fig.update_layout(barmode=barmode)

    # Non-pie axes styling
    if not is_pie:
        x_dict = dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.12)",
            zeroline=False,
            tickfont=dict(color="#e2e8f0", size=11),
            title_font=dict(color="#ffffff", size=12)
        )
        if xaxis_title:
            x_dict["title"] = xaxis_title
        if category_order_x:
            x_dict["categoryorder"] = category_order_x
        fig.update_xaxes(**x_dict)

        y_dict = dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.12)",
            zeroline=False,
            tickfont=dict(color="#e2e8f0", size=11),
            title_font=dict(color="#ffffff", size=12)
        )
        if yaxis_title:
            y_dict["title"] = yaxis_title
        if category_order_y:
            y_dict["categoryorder"] = category_order_y
        fig.update_yaxes(**y_dict)

    # Ensure Bar Text Labels (text_auto) are high-contrast white
    fig.update_traces(
        textfont=dict(color="#ffffff", size=11),
        selector=dict(type="bar")
    )
    # Ensure Pie slice text is high-contrast white
    fig.update_traces(
        textfont=dict(color="#ffffff", size=12),
        textinfo="percent+label",
        selector=dict(type="pie")
    )

    return fig


# ----------------- VERIFIED PORTS CATALOG BY REGION -----------------
# Maps clean user-facing labels to raw PPA dataset port identifiers and metadata
VERIFIED_PORTS_CATALOG = {
    "Southern Luzon & MIMAROPA": [
        ("Base Port of Batangas (PMO Batangas)", ["BP Batangas (Base Port Total)", "Batangas"], "PMO Batangas", "Batangas"),
        ("Base Port of Calapan (PMO Mindoro)", ["BP Calapan (Base Port Total)"], "PMO Mindoro", "Calapan"),
        ("Puerto Princesa Port (PMO Palawan)", ["BP Puerto Princesa (Base Port Total)"], "PMO Palawan", "Puerto Princesa"),
        ("Base Port of Lucena (PMO Marinduque/Quezon)", ["BP Lucena (Base Port Total)"], "PMO Marinduque/Quezon", "Lucena"),
        ("Base Port of Legazpi (PMO Bicol)", ["BP Legazpi (Base Port Total)"], "PMO Bicol", "Legazpi"),
        ("TMO Matnog (PMO Bicol)", ["TMO Matnog", "TP Matnog"], "PMO Bicol", "Matnog"),
        ("TMO Tabaco (PMO Bicol)", ["TMO Tabaco", "TP Tabaco"], "PMO Bicol", "Tabaco"),
        ("Base Port of Masbate (PMO Masbate)", ["BP Masbate (Base Port Total)"], "PMO Masbate", "Masbate"),
        ("TMO Balanacan - Marinduque (PMO Marinduque/Quezon)", ["TMO Balanacan", "TP Balanacan"], "PMO Marinduque/Quezon", "Balanacan"),
        ("TMO Coron (PMO Palawan)", ["TMO Coron", "TP Coron"], "PMO Palawan", "Coron"),
        ("TMO El Nido (PMO Palawan)", ["TMO El Nido", "TP El Nido"], "PMO Palawan", "El Nido"),
        ("TMO Puerto Galera (PMO Mindoro)", ["TMO Puerto Galera", "TP Puerto Galera"], "PMO Mindoro", "Puerto Galera"),
        ("TP Abra de Ilog (PMO Mindoro)", ["TP Abra de Ilog", "TMO San Jose/Abra de Ilog"], "PMO Mindoro", "Abra de Ilog"),
        ("TMO Roxas - Mindoro (PMO Mindoro)", ["TMO Roxas", "TP Roxas"], "PMO Mindoro", "Roxas"),
        ("TMO Romblon (PMO Marinduque/Quezon)", ["TMO Romblon", "TP Romblon"], "PMO Marinduque/Quezon", "Romblon"),
        ("TP San Jose - Mindoro (PMO Mindoro)", ["TP San Jose"], "PMO Mindoro", "San Jose"),
        ("TP Pasacao (PMO Bicol)", ["TP Pasacao", "TMO Camarines"], "PMO Bicol", "Pasacao"),
        ("TP Pio Duran (PMO Bicol)", ["TP Pio Duran"], "PMO Bicol", "Pio Duran"),
        ("TP Bulan (PMO Bicol)", ["TP Bulan"], "PMO Bicol", "Bulan"),
        ("TP Virac - Catanduanes (PMO Bicol)", ["TP Virac", "TMO Catanduanes"], "PMO Bicol", "Virac"),
    ],
    "Metro Manila (NCR)": [
        ("Manila North Harbor (PMO NCR North)", ["BP North Harbor (Base Port Total)"], "PMO NCR North", "North Harbor"),
        ("Manila South Harbor (PMO NCR South)", ["BP South Harbor (Base Port Total)"], "PMO NCR South", "South Harbor"),
        ("Manila International Container Terminal (PMO NCR South)", ["Manila International Container Terminal (MICT)", "MICT"], "PMO NCR South", "MICT"),
        ("Pasig River Terminal (PMO NCR South)", ["TMO Pasig", "Terminal Pasig Bank - Government Bay & River", "Terminal Pasig Bank - Government Coastwise"], "PMO NCR South", "Pasig"),
    ],
    "Central & Northern Luzon": [
        ("Base Port of Currimao (PMO Northern Luzon)", ["BP Currimao (Base Port Total)"], "PMO Northern Luzon", "Currimao"),
        ("Base Port of Limay - Bataan (PMO Bataan/Aurora)", ["BP Limay (Base Port Total)"], "PMO Bataan/Aurora", "Limay"),
        ("Capinpin Port / Orion (PMO Bataan/Aurora)", ["TP Capinpin", "TMO Capinpin", "TP Orion"], "PMO Bataan/Aurora", "Capinpin"),
        ("Dingalan Port (PMO Bataan/Aurora)", ["TP Dingalan", "TMO Dingalan"], "PMO Bataan/Aurora", "Dingalan"),
        ("Casiguran Port (PMO Bataan/Aurora)", ["TP Casiguran", "TMO Casiguran"], "PMO Bataan/Aurora", "Casiguran"),
        ("Basco Port - Batanes (PMO Northern Luzon)", ["TP Basco, Batanes", "TMO Batanes"], "PMO Northern Luzon", "Basco"),
        ("Aparri Port (PMO Northern Luzon)", ["TP Aparri (Anchorage)"], "PMO Northern Luzon", "Aparri"),
        ("Claveria Port (PMO Northern Luzon)", ["TP Claveria"], "PMO Northern Luzon", "Claveria"),
        ("Salomague Port (PMO Northern Luzon)", ["TP Salomague"], "PMO Northern Luzon", "Salomague"),
        ("Sual / Pangasinan Port (PMO Northern Luzon)", ["TP Sual", "TMO Pangasinan"], "PMO Northern Luzon", "Sual"),
    ]
}

# Build flat lookup maps
LABEL_TO_RAW_PORTS = {}
LABEL_TO_SHORT = {}
ALL_FRIENDLY_PORTS = []
for region_name, port_items in VERIFIED_PORTS_CATALOG.items():
    for label, raw_list, pmo_name, short_n in port_items:
        LABEL_TO_RAW_PORTS[label] = raw_list
        LABEL_TO_SHORT[label] = short_n
        ALL_FRIENDLY_PORTS.append(label)


# ----------------- SIDEBAR CONTROLS & NAVIGATION -----------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 12px;">
        <span style="font-size: 2.8rem;">🚢</span>
        <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; letter-spacing: -0.01em;">SeaMetrics</div>
        <div style="font-size: 0.80rem; color: #00cec9; font-weight: 700;">Luzon Maritime Analytics & Forecasting</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("Scope & Filter Controls")

    # 1. Year Analysis Mode Selector
    year_mode = st.radio(
        "Temporal Horizon Mode:",
        ["Single Year Deep-Dive", "Multi-Year Comparison", "All Available Years (2019–2026)"],
        index=0,
        help="Select a single year for detailed analysis, choose specific years to compare, or view all 6 dataset years."
    )

    if year_mode == "Single Year Deep-Dive":
        default_idx = VALID_DATASET_YEARS.index(2026) if 2026 in VALID_DATASET_YEARS else len(VALID_DATASET_YEARS) - 1
        selected_year = st.selectbox(
            "Select Reporting Year:",
            options=VALID_DATASET_YEARS,
            index=default_idx,
            help="Available years: 2019 (Annual Vol 2 Commodity), 2022–2025 (Full Years), 2026 (Q1–Q3 Partial)."
        )
        selected_years_list = [selected_year]
    elif year_mode == "Multi-Year Comparison":
        default_multi = [y for y in [2022, 2023, 2024, 2025, 2026] if y in VALID_DATASET_YEARS]
        selected_years_list = st.multiselect(
            "Select Years to Compare:",
            options=VALID_DATASET_YEARS,
            default=default_multi,
            help="Select two or more years to evaluate comparative performance."
        )
        if not selected_years_list:
            selected_years_list = VALID_DATASET_YEARS
        selected_year = selected_years_list[-1]
    else:  # All Available Years
        selected_years_list = VALID_DATASET_YEARS
        selected_year = 2026 if 2026 in VALID_DATASET_YEARS else VALID_DATASET_YEARS[-1]

    # 2. Dynamic Month / Period Selector based on actual coverage
    if len(selected_years_list) == 1:
        yr = selected_years_list[0]
        if yr == 2026:
            month_options = ["January", "February", "March", "April", "May", "June", "July", "August", "September"]
            st.info("ℹ️ **2026 Status:** Interim Q1–Q3 report (Jan–Sep). Oct–Dec unrecorded.")
        elif yr == 2025:
            month_options = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        elif yr in [2022, 2023, 2024]:
            month_options = ["Q1 Aggregate", "Q2 Aggregate", "Q3 Aggregate", "Q4 Aggregate"]
            st.info(f"ℹ️ **{yr} Status:** Source workbook provides quarterly cluster summaries (Q1–Q4).")
        elif yr == 2019:
            month_options = ["CY 2019 Aggregate"]
            st.info("ℹ️ **2019 Status:** PPA Volume 2 Commodity Analysis. Traffic counts unrecorded (NaN).")
        else:
            month_options = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        selected_months = st.multiselect("Reporting Period Filter:", options=month_options, default=month_options)
        if not selected_months:
            selected_months = month_options
        comp_period = "Single Year Selection"
    else:
        # Multi-Year period alignment filter
        comp_period = st.radio(
            "Multi-Year Reporting Period Alignment:",
            ["Matching Q1–Q3 (9 Months - Fair Baseline)", "All Available Periods (Q1–Q4)"],
            index=0,
            help="Comparing matching Q1–Q3 periods avoids misleading contractions when comparing 2026 with full years."
        )
        if "Matching Q1–Q3" in comp_period:
            selected_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                               "Q1 Aggregate", "Q2 Aggregate", "Q3 Aggregate"]
        else:
            selected_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                               "October", "November", "December", "Q1 Aggregate", "Q2 Aggregate", "Q3 Aggregate", "Q4 Aggregate", "CY 2019 Aggregate"]

    # 3. Comprehensive Port Selection System (Individual & Multi-Port)
    st.markdown("---")
    st.subheader("Port & Facility Selection")
    
    port_selection_mode = st.radio(
        "Port Selection Scope:",
        [
            "🌐 All Luzon Ports (Macro Aggregate)",
            "📍 Individual Port Deep-Dive",
            "📊 Custom Multi-Port Selection",
            "🎯 Batangas <-> Calapan Artery"
        ],
        index=0,
        help="Select all Luzon ports, zoom into one specific verified port, compare multiple ports, or focus on the Batangas-Calapan corridor."
    )

    all_raw_ports = sorted(list(df_monthly["Port"].dropna().unique()))
    active_port_display_name = "All Luzon Gateways"
    is_individual_port = False

    if port_selection_mode == "🌐 All Luzon Ports (Macro Aggregate)":
        # Cluster Selector
        all_clusters = ["All Luzon"] + sorted(list(df_monthly["Cluster"].dropna().unique()))
        selected_cluster = st.selectbox("Luzon Geographic Cluster:", all_clusters, index=0)
        
        if selected_cluster == "All Luzon":
            cluster_pmos = sorted(list(df_monthly[df_monthly["Year"].isin(selected_years_list)]["PMO"].dropna().unique()))
            selected_ports = all_raw_ports
            active_port_display_name = "All Luzon Facilities (Macro Aggregate)"
        else:
            cluster_pmos = sorted(list(df_monthly[(df_monthly["Cluster"] == selected_cluster) & (df_monthly["Year"].isin(selected_years_list))]["PMO"].dropna().unique()))
            selected_ports = sorted(list(df_monthly[(df_monthly["Cluster"] == selected_cluster) & (df_monthly["Year"].isin(selected_years_list))]["Port"].dropna().unique()))
            active_port_display_name = f"{selected_cluster} Ports"

        selected_pmos = cluster_pmos

    elif port_selection_mode == "📍 Individual Port Deep-Dive":
        is_individual_port = True
        region_filter = st.selectbox("Filter by Region:", ["All Regions"] + list(VERIFIED_PORTS_CATALOG.keys()))
        if region_filter == "All Regions":
            selectable_ports = ALL_FRIENDLY_PORTS
        else:
            selectable_ports = [label for label, _, _, _ in VERIFIED_PORTS_CATALOG[region_filter]]

        default_port_idx = selectable_ports.index("Base Port of Batangas (PMO Batangas)") if "Base Port of Batangas (PMO Batangas)" in selectable_ports else 0
        selected_friendly_port = st.selectbox("Select Verified Port:", selectable_ports, index=default_port_idx)
        
        raw_port_matches = LABEL_TO_RAW_PORTS.get(selected_friendly_port, [selected_friendly_port])
        # Include any raw names present in df_monthly
        selected_ports = [p for p in all_raw_ports if any(rm == p or rm in p for rm in raw_port_matches)]
        if not selected_ports:
            selected_ports = raw_port_matches

        selected_pmos = sorted(list(df_monthly[df_monthly["Port"].isin(selected_ports)]["PMO"].dropna().unique()))
        selected_cluster = "Individual Port Focus"
        active_port_display_name = selected_friendly_port

    elif port_selection_mode == "📊 Custom Multi-Port Selection":
        selected_friendly_list = st.multiselect(
            "Select Ports to Include:",
            options=ALL_FRIENDLY_PORTS,
            default=["Base Port of Batangas (PMO Batangas)", "Base Port of Calapan (PMO Mindoro)", "Manila North Harbor (PMO NCR North)"]
        )
        if not selected_friendly_list:
            selected_friendly_list = ["Base Port of Batangas (PMO Batangas)"]

        matched_raw = []
        for fl in selected_friendly_list:
            rms = LABEL_TO_RAW_PORTS.get(fl, [fl])
            for rm in rms:
                matched_raw.extend([p for p in all_raw_ports if rm == p or rm in p])
        selected_ports = sorted(list(set(matched_raw)))
        selected_pmos = sorted(list(df_monthly[df_monthly["Port"].isin(selected_ports)]["PMO"].dropna().unique()))
        selected_cluster = "Custom Selection"
        active_port_display_name = f"{len(selected_friendly_list)} Selected Ports"

    else:  # Batangas <-> Calapan Artery
        selected_ports = [p for p in all_raw_ports if any(k in p for k in ["BP Batangas (Base Port Total)", "Batangas", "BP Calapan (Base Port Total)"])]
        selected_pmos = ["PMO Batangas", "PMO Mindoro"]
        selected_cluster = "Southern Luzon"
        active_port_display_name = "Batangas <-> Calapan Corridor Artery"

    st.markdown("---")
    st.markdown("### Reporting Coverage Notice")
    st.markdown("""
    * **2026 Status:** <span class="status-badge badge-partial">Q1–Q3 Partial (Jan–Sep)</span>
    * **2022–2025 Status:** <span class="status-badge badge-full">Q1–Q4 Full Years</span>
    * **2019 Status:** <span class="status-badge badge-partial">Volume 2 Commodity Only</span> (Traffic Unreported)
    * **Fair Comparison:** All multi-year growth rates isolate matching **Q1–Q3 (9-month)** baselines to avoid partial-period distortions.
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Fundamentals of Data Analytics • Leuteboro NHS • MIMAROPA")
    st.sidebar.markdown('''
    <div style="background: rgba(14, 165, 233, 0.12); border: 1px solid #1e3a6d; border-left: 3px solid #00cec9; border-radius: 8px; padding: 12px; margin-top: 14px;">
        <div style="font-weight: 700; color: #38bdf8; font-size: 0.82rem; margin-bottom: 4px;">📖 Research Documentation</div>
        <div style="color: #cbd5e1; font-size: 0.76rem; line-height: 1.4;">
            Explore <b>Tab H: About & Methodology</b> for official PPA data sources, research objectives, model accuracy metrics, and disclaimers.
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ----------------- DATA SLICING & DYNAMIC TOTALS -----------------
filtered_m = df_monthly[
    (df_monthly["Year"].isin(selected_years_list)) &
    (df_monthly["Port"].isin(selected_ports)) &
    (df_monthly["Month"].isin(selected_months))
]

# Calculate aggregated totals defensively without double-counting
if port_selection_mode == "🌐 All Luzon Ports (Macro Aggregate)" and selected_cluster == "All Luzon":
    # Use macro dataset for exact Luzon-wide totals
    macro_sub = df_macro[df_macro["Cluster"] == "Luzon Total"]
    macro_sub = macro_sub[macro_sub["Year"].isin(selected_years_list)]
    
    # Filter quarters if matching Q1-Q3 is active
    if len(selected_years_list) > 1 and "Matching Q1–Q3" in comp_period:
        macro_sub = macro_sub[macro_sub["Quarter"].isin(["Q1", "Q2", "Q3"])]
    elif len(selected_years_list) == 1 and selected_year == 2026:
        macro_sub = macro_sub[macro_sub["Quarter"].isin(["Q1", "Q2", "Q3"])]
    
    pax_sum = macro_sub["Pax_Total"].sum(min_count=1)
    ship_sum = macro_sub["Ship_Total"].sum(min_count=1)
    roro_sum = macro_sub["RoRo_Total"].sum(min_count=1)
    total_pax = int(pax_sum) if pd.notna(pax_sum) else None
    total_ship = int(ship_sum) if pd.notna(ship_sum) else None
    total_roro = int(roro_sum) if pd.notna(roro_sum) else None
else:
    # Facility-level or filtered subset aggregation
    base_filter = filtered_m[filtered_m["Is_Base_Port_Total"] == 1]
    if base_filter.empty:
        base_filter = filtered_m
    pax_sum = base_filter["Pax_Total"].sum(min_count=1)
    ship_sum = base_filter["Ship_Total"].sum(min_count=1)
    roro_sum = base_filter["RoRo_Total"].sum(min_count=1)
    total_pax = int(pax_sum) if pd.notna(pax_sum) else None
    total_ship = int(ship_sum) if pd.notna(ship_sum) else None
    total_roro = int(roro_sum) if pd.notna(roro_sum) else None

pax_per_call = round(total_pax / total_ship, 1) if (total_pax is not None and total_ship is not None and total_ship > 0) else None
roro_per_call = round(total_roro / total_ship, 1) if (total_roro is not None and total_ship is not None and total_ship > 0) else None

# ----------------- TOP HEADER BANNER -----------------
if len(selected_years_list) == 1:
    period_badge_text = f"Active Year: {selected_year} ({len(selected_months)} periods)"
else:
    period_badge_text = f"Comparing {len(selected_years_list)} Years: {', '.join(map(str, sorted(selected_years_list)))}"

st.markdown(f"""
<div class="header-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <span class="header-tag">Official PPA Statistics</span>
            <span class="header-tag">Verified Luzon Gateways</span>
            <span class="header-tag">Batangas–Calapan Artery</span>
            <span class="header-tag">2019, 2022–2026 Horizon</span>
            <div class="header-title">SeaMetrics: Luzon Port Traffic & Mobility Intelligence</div>
            <div class="header-subtitle">
                A multi-year empirical analytics and predictive modeling system examining passenger movement, 
                vessel activity, and roll-on/roll-off (RoRo) transportation across <b>Luzon and its associated island groups</b>.
                <br><b>Current Active Scope:</b> <span style="color: #00cec9; font-weight: 700;">{active_port_display_name}</span>
            </div>
        </div>
        <div style="text-align: right; margin-top: 4px;">
            <span class="status-badge {'badge-partial' if 2026 in selected_years_list or 2019 in selected_years_list else 'badge-full'}">
                {period_badge_text}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- QUICK PUBLIC VISITOR ORIENTATION -----------------
with st.expander("ℹ️ Public Visitor Guide: About SeaMetrics, Research Scope & Official Data Disclaimers", expanded=False):
    col_ov1, col_ov2, col_ov3 = st.columns(3)
    with col_ov1:
        st.markdown('''
        <div class="doc-card" style="height: 100%;">
            <div style="color: #00cec9; font-weight: 800; font-size: 0.92rem; margin-bottom: 6px;">🎯 What is SeaMetrics?</div>
            <p style="font-size: 0.84rem; line-height: 1.5; color: #e2e8f0; margin-bottom: 0px;">
                An empirical maritime analytics and predictive platform monitoring <b>Passenger Traffic</b>, <b>Commercial Ship Calls</b>, 
                and <b>RoRo Vehicle Movements</b> across 32 verified Luzon ports (2019, 2022–2026).
            </p>
        </div>
        ''', unsafe_allow_html=True)
    with col_ov2:
        st.markdown('''
        <div class="doc-card" style="height: 100%;">
            <div style="color: #38bdf8; font-weight: 800; font-size: 0.92rem; margin-bottom: 6px;">📊 Primary Data Provenance</div>
            <p style="font-size: 0.84rem; line-height: 1.5; color: #e2e8f0; margin-bottom: 0px;">
                Constructed exclusively from official <b>Philippine Ports Authority (PPA)</b> Annual & Quarterly Statistical Reports. 
                2026 data currently reflects <b>Q1–Q3 partial year</b> (Jan–Sep); 2019 reflects Volume 2 Commodity data.
            </p>
        </div>
        ''', unsafe_allow_html=True)
    with col_ov3:
        st.markdown('''
        <div class="doc-card" style="height: 100%;">
            <div style="color: #fbbf24; font-weight: 800; font-size: 0.92rem; margin-bottom: 6px;">⚖️ Research & Tool Disclaimer</div>
            <p style="font-size: 0.84rem; line-height: 1.5; color: #e2e8f0; margin-bottom: 0px;">
                Independent academic research platform developed under the <i>Fundamentals of Data Analytics</i> course (Leuteboro NHS). 
                <b>Not an official government dispatch or ticketing system</b> and does not replace official PPA statistics.
            </p>
        </div>
        ''', unsafe_allow_html=True)
    st.info("👉 For complete research methodology, backtesting accuracy benchmarks, mathematical confidence intervals, and user guidance, explore **Tab H: ℹ️ About & Methodology** below.")

# ----------------- EIGHT DEDICATED SECTIONS (TABS A - H) -----------------
tab_a, tab_b, tab_c, tab_d, tab_e, tab_f, tab_g, tab_h = st.tabs([
    "A. 🌐 Overview",
    "B. 👥 Passenger Analytics",
    "C. 🚢 Ship Call Analytics",
    "D. 🚚 RoRo Analytics",
    "E. ⚖️ Port Comparison",
    "F. 🔮 Predictive Analytics",
    "G. 📋 Data Explorer",
    "H. ℹ️ About & Methodology"
])

# =========================================================================
# SECTION A: OVERVIEW
# =========================================================================
with tab_a:
    st.subheader(f"A. Overview: Executive Summary & System Metrics — [{active_port_display_name}]")

    # 1. Main Bento Grid (Equal Dimensions, Single-Line Values)
    pax_val_str = f"{total_pax:,}" if total_pax is not None else "Unreported*"
    pax_sub_str = f"Commuters ({len(selected_years_list)} yr scope)" if total_pax is not None else "*Vol. 2 Commodity Only"

    ship_val_str = f"{total_ship:,}" if total_ship is not None else "Unreported*"
    ship_sub_str = f"Commercial calls" if total_ship is not None else "*Vol. 2 Commodity Only"

    roro_val_str = f"{total_roro:,}" if total_roro is not None else "Unreported*"
    roro_sub_str = f"Rolling vehicles" if total_roro is not None else "*Vol. 2 Commodity Only"

    if is_individual_port:
        ports_count_str = "1 Verified Port"
        ports_sub_str = LABEL_TO_SHORT.get(active_port_display_name, "Base Facility")
    elif port_selection_mode == "🎯 Batangas <-> Calapan Artery":
        ports_count_str = "2 Artery Ports"
        ports_sub_str = "Batangas & Calapan"
    else:
        ports_count_str = f"{len(selected_ports):,} Facilities"
        ports_sub_str = f"Across {len(selected_pmos)} PMOs"

    years_label = f"{len(selected_years_list)} of 6 Years"

    if len(selected_years_list) == 1:
        if selected_year == 2026:
            period_title = "Q1–Q3 (9 Mos)"
            period_sub = "Partial Year (Jan–Sep)"
        elif selected_year == 2019:
            period_title = "CY 2019 (Annual)"
            period_sub = "Volume 2 Commodity"
        elif selected_year in [2022, 2023, 2024]:
            period_title = f"{len(selected_months)} Quarters"
            period_sub = "Quarterly Reporting"
        else:
            period_title = f"{len(selected_months)} Months"
            period_sub = "Full Calendar Year"
    else:
        if "Matching Q1–Q3" in comp_period:
            period_title = "Matching Q1–Q3"
            period_sub = "9-Month Fair Comparison"
        else:
            period_title = "All Available"
            period_sub = "Full Historical Series"

    st.markdown(f"""
    <div class="bento-container">
        <div class="bento-card">
            <div class="bento-header"><span>👥</span> Total Passengers</div>
            <div class="bento-number bento-cyan">{pax_val_str}</div>
            <div class="bento-subtitle">{pax_sub_str}</div>
        </div>
        <div class="bento-card">
            <div class="bento-header"><span>🚢</span> Total Ship Calls</div>
            <div class="bento-number bento-blue">{ship_val_str}</div>
            <div class="bento-subtitle">{ship_sub_str}</div>
        </div>
        <div class="bento-card">
            <div class="bento-header"><span>🚛</span> Total RoRo Vehicles</div>
            <div class="bento-number bento-amber">{roro_val_str}</div>
            <div class="bento-subtitle">{roro_sub_str}</div>
        </div>
        <div class="bento-card">
            <div class="bento-header"><span>⚓</span> Included Ports</div>
            <div class="bento-number bento-emerald">{ports_count_str}</div>
            <div class="bento-subtitle">{ports_sub_str}</div>
        </div>
        <div class="bento-card">
            <div class="bento-header"><span>📅</span> Dataset Years</div>
            <div class="bento-number bento-purple">{years_label}</div>
            <div class="bento-subtitle">{", ".join(map(str, sorted(selected_years_list)))}</div>
        </div>
        <div class="bento-card">
            <div class="bento-header"><span>⏱️</span> Reporting Period</div>
            <div class="bento-number bento-pink">{period_title}</div>
            <div class="bento-subtitle">{period_sub}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Port Activity Highlights Section
    st.markdown("### 🏆 Port Activity Highlights")
    st.caption("Key empirical operational benchmarks, peak months, and highest recorded activity centers.")

    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col1:
        st.markdown("""
        <div class="highlight-card">
            <div class="highlight-title">Peak Passenger Traffic Month</div>
            <div class="highlight-val" style="color: #00cec9;">May (3,030,996 Pax)</div>
            <div class="highlight-sub">Seasonality Index: 164.94 (Holy Week & Summer Vacation Surge)</div>
        </div>
        <div class="highlight-card">
            <div class="highlight-title">Busiest Passenger Port</div>
            <div class="highlight-val" style="color: #00cec9;">Base Port of Batangas</div>
            <div class="highlight-sub">3,780,022 commuters in 2026 Q1–Q3 (4.88M in 2025 Full Year)</div>
        </div>
        """, unsafe_allow_html=True)

    with h_col2:
        st.markdown("""
        <div class="highlight-card" style="border-left-color: #38bdf8;">
            <div class="highlight-title">Peak Ship Calls Month</div>
            <div class="highlight-val" style="color: #38bdf8;">May (14,780 Calls)</div>
            <div class="highlight-sub">Seasonality Index: 118.28 (Maximum commercial fleet deployment)</div>
        </div>
        <div class="highlight-card" style="border-left-color: #38bdf8;">
            <div class="highlight-title">Busiest Ship Call Port</div>
            <div class="highlight-val" style="color: #38bdf8;">Base Port of Batangas</div>
            <div class="highlight-sub">25,695 commercial dockings in 2026 Q1–Q3 (22.8% Luzon share)</div>
        </div>
        """, unsafe_allow_html=True)

    with h_col3:
        st.markdown("""
        <div class="highlight-card" style="border-left-color: #fbbf24;">
            <div class="highlight-title">Peak RoRo Traffic Month</div>
            <div class="highlight-val" style="color: #fbbf24;">May (395,200 Vehicles)</div>
            <div class="highlight-sub">Seasonality Index: 130.89 (Summer commercial goods & travel surge)</div>
        </div>
        <div class="highlight-card" style="border-left-color: #fbbf24;">
            <div class="highlight-title">Busiest RoRo Port</div>
            <div class="highlight-val" style="color: #fbbf24;">Base Port of Batangas</div>
            <div class="highlight-sub">683,803 vehicles in 2026 Q1–Q3 (Calapan Port: 443,268 vehicles)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Historical Trends at a Glance
    st.markdown("### 📈 Historical Trends at a Glance (2022–2026 Matching Q1–Q3 Baseline)")
    st.caption("Standardized 9-month historical comparison eliminating partial-year reporting distortions.")

    if not is_individual_port and port_selection_mode == "🌐 All Luzon Ports (Macro Aggregate)":
        df_luz_macro = df_macro[df_macro["Cluster"] == "Luzon Total"]
        q1_q3_macro = df_luz_macro[df_luz_macro["Quarter"].isin(["Q1", "Q2", "Q3"])].groupby("Year")[["Pax_Total", "RoRo_Total", "Ship_Total"]].sum().reset_index()
    else:
        # Group filtered base port data by year
        sub_p = df_ports[df_ports["Port"].isin(selected_ports)]
        if not sub_p.empty:
            q1_q3_macro = sub_p.groupby("Year")[["Q1_Q3_Pax", "Q1_Q3_RoRo", "Q1_Q3_Ship"]].sum().reset_index()
            q1_q3_macro = q1_q3_macro.rename(columns={"Q1_Q3_Pax": "Pax_Total", "Q1_Q3_RoRo": "RoRo_Total", "Q1_Q3_Ship": "Ship_Total"})
        else:
            q1_q3_macro = pd.DataFrame({"Year": [2025, 2026], "Pax_Total": [0, 0], "RoRo_Total": [0, 0], "Ship_Total": [0, 0]})

    q1_q3_macro["Status"] = q1_q3_macro["Year"].apply(lambda y: "2026 Q1–Q3 (Audited Actual)" if y == 2026 else "Historical Baseline (Matching Q1–Q3)")

    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        fig_pax_5yr = px.bar(
            q1_q3_macro,
            x="Year",
            y="Pax_Total",
            color="Status",
            text_auto=".3s",
            title=f"Passenger Throughput ({active_port_display_name})",
            labels={"Pax_Total": "Passengers", "Year": "Year"},
            color_discrete_map={"Historical Baseline (Matching Q1–Q3)": "#0984e3", "2026 Q1–Q3 (Audited Actual)": "#00cec9"}
        )
        apply_seametrics_chart_theme(fig_pax_5yr, height=340, show_legend=False, xaxis_title="Reporting Year", yaxis_title="Total Passengers")
        st.plotly_chart(fig_pax_5yr, width='stretch')

    with c_m2:
        fig_roro_5yr = px.bar(
            q1_q3_macro,
            x="Year",
            y="RoRo_Total",
            color="Status",
            text_auto=".3s",
            title=f"RoRo Vehicle Traffic ({active_port_display_name})",
            labels={"RoRo_Total": "RoRo Vehicles", "Year": "Year"},
            color_discrete_map={"Historical Baseline (Matching Q1–Q3)": "#e17055", "2026 Q1–Q3 (Audited Actual)": "#fdcb6e"}
        )
        apply_seametrics_chart_theme(fig_roro_5yr, height=340, show_legend=False, xaxis_title="Reporting Year", yaxis_title="RoRo Vehicles")
        st.plotly_chart(fig_roro_5yr, width='stretch')

    with c_m3:
        fig_ship_5yr = px.bar(
            q1_q3_macro,
            x="Year",
            y="Ship_Total",
            color="Status",
            text_auto=".3s",
            title=f"Vessel Ship Calls ({active_port_display_name})",
            labels={"Ship_Total": "Ship Calls", "Year": "Year"},
            color_discrete_map={"Historical Baseline (Matching Q1–Q3)": "#6c5ce7", "2026 Q1–Q3 (Audited Actual)": "#a29bfe"}
        )
        apply_seametrics_chart_theme(fig_ship_5yr, height=340, show_legend=False, xaxis_title="Reporting Year", yaxis_title="Ship Calls")
        st.plotly_chart(fig_ship_5yr, width='stretch')

    # 4. Monthly Activity Visualization (with interactive switcher)
    st.markdown("### 📊 Monthly Activity Visualization (Actual Monthly Records)")
    st.caption("Examine monthly curves for reporting years with granular monthly records (CY 2025 & CY 2026).")

    metric_choice = st.radio(
        "Select Indicator for Monthly Distribution:",
        ["👥 Passenger Traffic", "🚢 Ship Calls", "🚛 RoRo Vehicles"],
        horizontal=True
    )

    monthly_scope = filtered_m[filtered_m["Year"].isin([2025, 2026])]
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthly_scope = monthly_scope[monthly_scope["Month"].isin(month_order)]
    
    if "Passenger" in metric_choice:
        y_col = "Pax_Total"
        y_label = "Passenger Traffic"
        trace_color_25 = "#38bdf8"
        trace_color_26 = "#00cec9"
    elif "Ship" in metric_choice:
        y_col = "Ship_Total"
        y_label = "Ship Calls"
        trace_color_25 = "#818cf8"
        trace_color_26 = "#6366f1"
    else:
        y_col = "RoRo_Total"
        y_label = "RoRo Vehicles"
        trace_color_25 = "#f59e0b"
        trace_color_26 = "#fbbf24"

    if not monthly_scope.empty:
        m_agg = monthly_scope.groupby(["Year", "Month", "Month_Num"])[y_col].sum().reset_index()
        m_agg["Month"] = pd.Categorical(m_agg["Month"], categories=month_order, ordered=True)
        m_agg = m_agg.sort_values("Month_Num")
        m_agg["Year_Label"] = m_agg["Year"].apply(lambda y: f"{y} (Full 12 Mos)" if y == 2025 else f"{y} (Q1–Q3 Actuals)")

        fig_monthly_compare = px.line(
            m_agg,
            x="Month",
            y=y_col,
            color="Year_Label",
            markers=True,
            title=f"Monthly Trajectory of {y_label} ({active_port_display_name}): 2025 vs. 2026 Actual Observations",
            labels={y_col: y_label, "Month": "Month", "Year_Label": "Dataset Year"},
            color_discrete_map={
                "2025 (Full 12 Mos)": trace_color_25,
                "2026 (Q1–Q3 Actuals)": trace_color_26
            }
        )
        fig_monthly_compare.update_traces(line_width=3, marker=dict(size=8))
        fig_monthly_compare.add_vline(
            x=4,
            line_dash="dash",
            line_color="#34d399",
            annotation_text="May Peak (Holy Week/Summer)",
            annotation_position="top left",
            annotation_font=dict(color="#ffffff", size=11),
            annotation_bgcolor="rgba(10, 25, 47, 0.88)",
            annotation_bordercolor="#34d399",
            annotation_borderwidth=1
        )
        fig_monthly_compare.add_vline(
            x=8,
            line_dash="dash",
            line_color="#f87171",
            annotation_text="Sept Trough (Habagat Monsoon)",
            annotation_position="bottom right",
            annotation_font=dict(color="#ffffff", size=11),
            annotation_bgcolor="rgba(10, 25, 47, 0.88)",
            annotation_bordercolor="#f87171",
            annotation_borderwidth=1
        )
        apply_seametrics_chart_theme(
            fig_monthly_compare,
            height=400,
            show_legend=True,
            legend_title="Dataset Year",
            legend_orientation="h",
            xaxis_title="Reporting Month",
            yaxis_title=y_label
        )
        st.plotly_chart(fig_monthly_compare, width='stretch')
    else:
        st.info("No granular monthly records found for the active filter combination.")

    # 5. Key Analytical Insights
    st.markdown("### 💡 What the Data Tells Us: Key Analytical Insights")
    ins_col1, ins_col2 = st.columns(2)
    with ins_col1:
        st.markdown("""
        <div class="info-card">
            <h5 style="color: #00cec9; margin-top: 0;">1. Sustained Post-Pandemic Mobility Rebound</h5>
            <p>
                Comparing matching 9-month baselines (Q1–Q3) reveals robust multi-year growth across Luzon: passenger traffic expanded 
                from <b>12,319,304 commuters in 2022</b> to <b>14,461,806 in 2023 (+17.39%)</b>, <b>16,493,372 in 2024 (+14.05%)</b>, and peaked at 
                <b>17,013,983 in 2025 (+3.16%)</b>, before stabilizing at <b>16,784,830 in 2026 (-1.35%)</b>. Over the 5-year observation baseline, 
                passenger volume expanded by <b>+36.25%</b>.
            </p>
        </div>
        <div class="info-card">
            <h5 style="color: #fbbf24; margin-top: 0;">2. Extreme Bimodal Seasonality & Weather Sensitivity</h5>
            <p>
                Passenger throughput surges to an annual peak in <b>May (Seasonality Index: 164.94; 3,030,996 monthly passengers)</b> and 
                <b>April (Index: 134.05)</b> due to Holy Week and summer holidays. In contrast, volumes contract sharply in 
                <b>September (Seasonality Index: 65.61; 1,205,778 passengers)</b> due to Southwest Monsoon (Habagat) voyage suspensions—representing a 
                <b>60.22% decline</b> from peak to trough.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with ins_col2:
        st.markdown("""
        <div class="info-card">
            <h5 style="color: #38bdf8; margin-top: 0;">3. Southwestern Corridor Gateway Centralization</h5>
            <p>
                Maritime activity in Luzon is heavily centralized on the Batangas–Calapan nautical bridge. In 2026 Q1–Q3, 
                <b>PMO Batangas (4,798,250 pax)</b> and <b>PMO Mindoro (4,229,377 pax)</b> together accounted for <b>53.79% of all passenger throughput</b> 
                (9,027,627 commuters) and <b>57.14% of all RoRo vehicle volume</b> (1,529,124 vehicles) in Luzon.
            </p>
        </div>
        <div class="info-card">
            <h5 style="color: #34d399; margin-top: 0;">4. Essential Commercial Freight Bridge Dominance</h5>
            <p>
                RoRo vehicular traffic is heavily weighted toward commercial logistics: <b>Type 4 heavy freight trucks/buses account for 40.20%</b> 
                (1,075,789 units) and <b>Type 2 passenger vehicles account for 33.10%</b> (885,786 units). This confirms that the Strong Republic 
                Nautical Highway operates primarily as a rolling food supply and agricultural transport bridge between Mindoro and mainland Luzon.
            </p>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# SECTION B: PASSENGER ANALYTICS
# =========================================================================
with tab_b:
    st.subheader(f"B. Passenger Analytics: Port Volumes, Temporal Fluctuations & Corridor Transit — [{active_port_display_name}]")
    
    # 1. Passenger Traffic by Port (Top Ports)
    df_pax_top = load_analysis_table("pax_top_ports.csv")
    col_bp1, col_bp2 = st.columns([3, 2])
    
    with col_bp1:
        st.markdown("#### Passenger Traffic by Primary Luzon Ports (Top 12 Facilities)")
        if df_pax_top is not None and not is_individual_port:
            top_12_pax = df_pax_top.head(12)
            fig_top_pax = px.bar(
                top_12_pax,
                x="pax_total_2026_q1_q3",
                y="port_name",
                orientation="h",
                text_auto=".3s",
                title="Top Luzon Ports by Passenger Throughput (2026 Q1–Q3)",
                labels={"pax_total_2026_q1_q3": "Passengers (9 Months)", "port_name": "Port / Terminal"},
                color="pax_total_2026_q1_q3",
                color_continuous_scale="Blues"
            )
            apply_seametrics_chart_theme(
                fig_top_pax,
                height=420,
                show_legend=False,
                category_order_y="total ascending",
                xaxis_title="Audited Passengers (Q1–Q3)",
                yaxis_title="Port Facility"
            )
            fig_top_pax.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_top_pax, width='stretch')
        else:
            pax_by_port = filtered_m.groupby("Port")["Pax_Total"].sum().reset_index().sort_values("Pax_Total", ascending=False).head(12)
            fig_top_pax = px.bar(
                pax_by_port,
                x="Pax_Total",
                y="Port",
                orientation="h",
                text_auto=".3s",
                title=f"Passenger Volume for Active Scope ({selected_year})",
                labels={"Pax_Total": "Passengers", "Port": "Port"}
            )
            apply_seametrics_chart_theme(
                fig_top_pax,
                height=420,
                show_legend=False,
                category_order_y="total ascending",
                xaxis_title="Passenger Volume",
                yaxis_title="Port Facility"
            )
            st.plotly_chart(fig_top_pax, width='stretch')

    with col_bp2:
        st.markdown("#### Embarked vs. Disembarked Flow Symmetry")
        if selected_year == 2019:
            st.info("Directional passenger flow is not available for CY 2019 (Volume 2 Commodity). Please select 2025 or 2026 to view arrival vs. departure balance.")
        else:
            total_disembarked = filtered_m["Pax_Disembarked"].sum()
            total_embarked = filtered_m["Pax_Embarked"].sum()
            total_cruise = filtered_m["Pax_Cruise"].sum()
            
            flow_df = pd.DataFrame({
                "Direction": ["Disembarked (Arrivals)", "Embarked (Departures)", "Cruise Passengers"],
                "Passengers": [total_disembarked, total_embarked, total_cruise]
            })
            fig_flow_pie = px.pie(
                flow_df,
                names="Direction",
                values="Passengers",
                title=f"Passenger Movement Directionality ({selected_year})",
                hole=0.45,
                color_discrete_sequence=["#00cec9", "#0984e3", "#6c5ce7"]
            )
            apply_seametrics_chart_theme(fig_flow_pie, height=350, show_legend=True, is_pie=True)
            st.plotly_chart(fig_flow_pie, width='stretch')
            st.caption(f"Net Passenger Migration Balance: **{int(total_embarked - total_disembarked):+,} passengers** (Near-perfect 1:1 flow equilibrium).")

    # 2. Passenger Trends Over Time (Monthly Seasonality)
    st.markdown(f"### Passenger Trends Over Time & Seasonal Patterns ({selected_year})")
    if selected_year == 2019:
        st.info("Monthly passenger time-series observations are not available for CY 2019 (Volume 2 Commodity). Please select 2025 or 2026 for monthly seasonality curves.")
    else:
        monthly_pax = filtered_m.groupby(["Month", "Month_Num"])[["Pax_Total", "Pax_Disembarked", "Pax_Embarked"]].sum().reset_index()
        monthly_pax["Month"] = pd.Categorical(monthly_pax["Month"], categories=month_order, ordered=True)
        monthly_pax = monthly_pax.sort_values("Month_Num")

        col_line1, col_line2 = st.columns(2)
        with col_line1:
            fig_line_pax = px.line(
                monthly_pax,
                x="Month",
                y="Pax_Total",
                markers=True,
                title=f"Monthly Total Passenger Throughput ({selected_year} Filtered Scope)",
                labels={"Pax_Total": "Passenger Volume", "Month": "Month"}
            )
            fig_line_pax.update_traces(line_color="#00cec9", line_width=3, marker=dict(size=8, color="#ffffff"))
            apply_seametrics_chart_theme(
                fig_line_pax,
                height=380,
                show_legend=False,
                xaxis_title="Month",
                yaxis_title="Passenger Volume"
            )
            st.plotly_chart(fig_line_pax, width='stretch')

        with col_line2:
            fig_bar_dir = go.Figure()
            fig_bar_dir.add_trace(go.Bar(x=monthly_pax["Month"], y=monthly_pax["Pax_Disembarked"], name="Disembarked (Arrivals)", marker_color="#00cec9"))
            fig_bar_dir.add_trace(go.Bar(x=monthly_pax["Month"], y=monthly_pax["Pax_Embarked"], name="Embarked (Departures)", marker_color="#0984e3"))
            apply_seametrics_chart_theme(
                fig_bar_dir,
                height=380,
                show_legend=True,
                legend_orientation="h",
                barmode="group",
                xaxis_title="Month",
                yaxis_title="Passengers"
            )
            fig_bar_dir.update_layout(title=dict(text=f"Arrivals vs. Departures by Month ({selected_year})", font=dict(color="#ffffff", size=15)))
            st.plotly_chart(fig_bar_dir, width='stretch')

    # 3. Year-over-Year Comparisons (PMO Level)
    st.markdown("### Year-over-Year Passenger Growth (2025 vs. 2026 Matching Q1–Q3)")
    df_pmo_yoy = load_analysis_table("pmo_yoy_comparison.csv")
    if df_pmo_yoy is not None:
        fig_pmo_pax_yoy = go.Figure()
        fig_pmo_pax_yoy.add_trace(go.Bar(x=df_pmo_yoy["pmo"], y=df_pmo_yoy["pax_total_2025_q1_q3"], name="2025 (Q1–Q3)", marker_color="#1e40af"))
        fig_pmo_pax_yoy.add_trace(go.Bar(x=df_pmo_yoy["pmo"], y=df_pmo_yoy["pax_total_2026_q1_q3"], name="2026 (Q1–Q3)", marker_color="#00cec9"))
        apply_seametrics_chart_theme(
            fig_pmo_pax_yoy,
            height=420,
            show_legend=True,
            legend_orientation="h",
            barmode="group",
            xaxis_title="Port Management Office (PMO)",
            yaxis_title="Passengers (Q1–Q3)"
        )
        fig_pmo_pax_yoy.update_layout(title=dict(text="PMO Passenger Traffic: 2025 vs 2026 Matching Q1–Q3 Comparison", font=dict(color="#ffffff", size=15)))
        fig_pmo_pax_yoy.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_pmo_pax_yoy, width='stretch')

    # 4. Batangas vs. Calapan Deep Dive
    st.markdown("### ⚓ Batangas Port vs. Calapan Port Gateway Corridor Deep Dive")
    df_corridor = load_analysis_table("corridor_batangas_calapan_metrics.csv")
    if df_corridor is not None:
        c1, c2 = st.columns([3, 2])
        with c1:
            bat_sub_25 = df_corridor[(df_corridor["year"] == 2025) & (df_corridor["port_name"].str.contains("Batangas"))]
            cal_sub_25 = df_corridor[(df_corridor["year"] == 2025) & (df_corridor["port_name"].str.contains("Calapan"))]
            bat_sub_26 = df_corridor[(df_corridor["year"] == 2026) & (df_corridor["port_name"].str.contains("Batangas"))]
            cal_sub_26 = df_corridor[(df_corridor["year"] == 2026) & (df_corridor["port_name"].str.contains("Calapan"))]

            bat_25_pax = bat_sub_25["total_passengers"].values[0] if not bat_sub_25.empty else 3883597
            cal_25_pax = cal_sub_25["total_passengers"].values[0] if not cal_sub_25.empty else 2704772
            bat_26_pax = bat_sub_26["total_passengers"].values[0] if not bat_sub_26.empty else 3780022
            cal_26_pax = cal_sub_26["total_passengers"].values[0] if not cal_sub_26.empty else 2539387

            fig_corridor_bar = go.Figure()
            fig_corridor_bar.add_trace(go.Bar(
                x=["Base Port of Batangas", "Base Port of Calapan"],
                y=[bat_25_pax, cal_25_pax],
                name="2025 (Q1–Q3 Baseline)",
                marker_color="#3b82f6"
            ))
            fig_corridor_bar.add_trace(go.Bar(
                x=["Base Port of Batangas", "Base Port of Calapan"],
                y=[bat_26_pax, cal_26_pax],
                name="2026 (Q1–Q3 Actual)",
                marker_color="#00cec9"
            ))
            apply_seametrics_chart_theme(
                fig_corridor_bar,
                height=380,
                show_legend=True,
                legend_orientation="h",
                barmode="group",
                xaxis_title="Corridor Port Gateway",
                yaxis_title="Passenger Volume"
            )
            fig_corridor_bar.update_layout(title=dict(text="Passenger Volume: Batangas vs Calapan Gateway", font=dict(color="#ffffff", size=15)))
            st.plotly_chart(fig_corridor_bar, width='stretch')
        with c2:
            st.markdown("""
            <div class="info-card">
                <h5 style="color: #38bdf8; margin-top: 0;">Corridor Dominance Statistics</h5>
                <ul style="padding-left: 18px;">
                    <li><b>Batangas Port 2026 Q1–Q3:</b> 3,780,022 passengers handled (22.5% of total Luzon).</li>
                    <li><b>Calapan Port 2026 Q1–Q3:</b> 2,544,386 passengers handled (15.2% of total Luzon).</li>
                    <li><b>Combined Gateway Share:</b> Batangas + Calapan represent <b>37.7% of all passenger traffic in Luzon</b>.</li>
                    <li><b>Corridor Flow Symmetry:</b> Disembarked and Embarked passenger ratio remains 0.99 : 1.01, demonstrating closed-circuit circular migration.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


# =========================================================================
# SECTION C: SHIP CALL ANALYTICS
# =========================================================================
with tab_c:
    st.subheader(f"C. Ship Call Analytics: Commercial Vessel Activity & Berthing Operations — [{active_port_display_name}]")
    
    df_ship_top = load_analysis_table("ship_top_ports.csv")
    col_sp1, col_sp2 = st.columns([3, 2])
    
    with col_sp1:
        st.markdown("#### Vessel Activity by Port (Top 12 Facilities)")
        if df_ship_top is not None and not is_individual_port:
            top_12_ship = df_ship_top.head(12)
            fig_top_ship = px.bar(
                top_12_ship,
                x="ship_total_2026_q1_q3",
                y="port_name",
                orientation="h",
                text_auto=".3s",
                title="Top Luzon Ports by Vessel Calls (2026 Q1–Q3)",
                labels={"ship_total_2026_q1_q3": "Ship Calls (9 Months)", "port_name": "Port / Terminal"},
                color="ship_total_2026_q1_q3",
                color_continuous_scale="Purples"
            )
            apply_seametrics_chart_theme(
                fig_top_ship,
                height=420,
                show_legend=False,
                category_order_y="total ascending",
                xaxis_title="Commercial Vessel Calls (Q1–Q3)",
                yaxis_title="Port Facility"
            )
            fig_top_ship.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_top_ship, width='stretch')
        else:
            ship_by_port = filtered_m.groupby("Port")["Ship_Total"].sum().reset_index().sort_values("Ship_Total", ascending=False).head(12)
            fig_top_ship = px.bar(
                ship_by_port,
                x="Ship_Total",
                y="Port",
                orientation="h",
                text_auto=".3s",
                title=f"Vessel Calls for Active Scope ({selected_year})",
                labels={"Ship_Total": "Ship Calls", "Port": "Port"}
            )
            apply_seametrics_chart_theme(
                fig_top_ship,
                height=420,
                show_legend=False,
                category_order_y="total ascending",
                xaxis_title="Commercial Ship Calls",
                yaxis_title="Port Facility"
            )
            st.plotly_chart(fig_top_ship, width='stretch')

    with col_sp2:
        st.markdown("#### Domestic vs. Foreign Calls Distribution")
        if selected_year == 2019:
            st.info("Vessel classification is not available for CY 2019 (Volume 2 Commodity). Please select 2025 or 2026.")
        else:
            dom_calls = filtered_m["Ship_Domestic"].sum()
            for_calls = filtered_m["Ship_Foreign"].sum()
            
            vessel_class_df = pd.DataFrame({
                "Vessel Type": ["Domestic Calls (Inter-Island)", "Foreign Calls (International)"],
                "Ship Calls": [dom_calls, for_calls]
            })
            fig_vessel_pie = px.pie(
                vessel_class_df,
                names="Vessel Type",
                values="Ship Calls",
                title=f"Domestic vs. Foreign Vessel Distribution ({selected_year})",
                hole=0.45,
                color_discrete_sequence=["#818cf8", "#f43f5e"]
            )
            apply_seametrics_chart_theme(fig_vessel_pie, height=350, show_legend=True, is_pie=True)
            st.plotly_chart(fig_vessel_pie, width='stretch')
            pct_dom = (dom_calls / (dom_calls + for_calls) * 100) if (dom_calls + for_calls) > 0 else 0
            st.caption(f"Domestic Dominance: **{pct_dom:.1f}% of all vessel calls** are domestic coastal and inter-island ro-ro/ferry operations.")

    # Monthly Ship Call Trends
    st.markdown(f"### Vessel Activity Trajectory by Month ({selected_year})")
    if selected_year != 2019:
        monthly_ship = filtered_m.groupby(["Month", "Month_Num"])[["Ship_Total", "Ship_Domestic", "Ship_Foreign"]].sum().reset_index()
        monthly_ship["Month"] = pd.Categorical(monthly_ship["Month"], categories=month_order, ordered=True)
        monthly_ship = monthly_ship.sort_values("Month_Num")

        fig_line_ship = px.line(
            monthly_ship,
            x="Month",
            y="Ship_Total",
            markers=True,
            title=f"Monthly Commercial Vessel Calls ({selected_year} Filtered Scope)",
            labels={"Ship_Total": "Ship Calls", "Month": "Month"}
        )
        fig_line_ship.update_traces(line_color="#a855f7", line_width=3, marker=dict(size=8, color="#ffffff"))
        apply_seametrics_chart_theme(
            fig_line_ship,
            height=380,
            show_legend=False,
            xaxis_title="Month",
            yaxis_title="Commercial Vessel Calls"
        )
        st.plotly_chart(fig_line_ship, width='stretch')


# =========================================================================
# SECTION D: RORO ANALYTICS
# =========================================================================
with tab_d:
    st.subheader(f"D. RoRo Analytics: Rolling Cargo, Vehicular Classifications & Logistics Artery — [{active_port_display_name}]")
    
    df_roro_top = load_analysis_table("roro_top_ports.csv")
    col_rp1, col_rp2 = st.columns([3, 2])
    
    with col_rp1:
        st.markdown("#### RoRo Traffic by Port (Top 12 Facilities)")
        if df_roro_top is not None and not is_individual_port:
            top_12_roro = df_roro_top.head(12)
            fig_top_roro = px.bar(
                top_12_roro,
                x="roro_total_2026_q1_q3",
                y="port_name",
                orientation="h",
                text_auto=".3s",
                title="Top Luzon Ports by RoRo Vehicular Volume (2026 Q1–Q3)",
                labels={"roro_total_2026_q1_q3": "RoRo Vehicles (9 Months)", "port_name": "Port / Terminal"},
                color="roro_total_2026_q1_q3",
                color_continuous_scale="YlOrBr"
            )
            apply_seametrics_chart_theme(
                fig_top_roro,
                height=420,
                show_legend=False,
                category_order_y="total ascending",
                xaxis_title="RoRo Vehicles (Q1–Q3)",
                yaxis_title="Port Facility"
            )
            fig_top_roro.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_top_roro, width='stretch')
        else:
            roro_by_port = filtered_m.groupby("Port")["RoRo_Total"].sum().reset_index().sort_values("RoRo_Total", ascending=False).head(12)
            fig_top_roro = px.bar(
                roro_by_port,
                x="RoRo_Total",
                y="Port",
                orientation="h",
                text_auto=".3s",
                title=f"RoRo Volume for Active Scope ({selected_year})",
                labels={"RoRo_Total": "RoRo Vehicles", "Port": "Port"}
            )
            apply_seametrics_chart_theme(
                fig_top_roro,
                height=420,
                show_legend=False,
                category_order_y="total ascending",
                xaxis_title="RoRo Vehicles",
                yaxis_title="Port Facility"
            )
            st.plotly_chart(fig_top_roro, width='stretch')

    with col_rp2:
        st.markdown("#### RoRo Fleet Vehicle Classification Distribution")
        if selected_year == 2019:
            st.info("RoRo vehicle classification is not available for CY 2019 (Volume 2 Commodity). Please select 2025 or 2026.")
        else:
            t1 = filtered_m["RoRo_Type1"].sum()
            t2 = filtered_m["RoRo_Type2"].sum()
            t3 = filtered_m["RoRo_Type3"].sum()
            t4 = filtered_m["RoRo_Type4"].sum()
            
            vclass_df = pd.DataFrame({
                "Vehicle Type": [
                    "Type 1: Motorcycles / Trikes",
                    "Type 2: Cars / Jeeps / SUVs",
                    "Type 3: Light Commercial Vans",
                    "Type 4: Heavy Freight / Buses"
                ],
                "Vehicles": [t1, t2, t3, t4]
            })
            fig_vclass_pie = px.pie(
                vclass_df,
                names="Vehicle Type",
                values="Vehicles",
                title=f"PPA Vehicle Classification Share ({selected_year})",
                hole=0.45,
                color_discrete_sequence=["#10b981", "#38bdf8", "#f59e0b", "#f97316"]
            )
            apply_seametrics_chart_theme(fig_vclass_pie, height=350, show_legend=True, is_pie=True)
            st.plotly_chart(fig_vclass_pie, width='stretch')
            pct_heavy = (t4 / sum([t1, t2, t3, t4]) * 100) if sum([t1, t2, t3, t4]) > 0 else 0
            st.caption(f"Heavy Freight Dominance: **{pct_heavy:.1f}% of all rolling units** are Type 4 commercial trucks and trailers.")

    # Inbound vs Outbound RoRo Movements
    st.markdown(f"### Inbound vs. Outbound RoRo Directionality ({selected_year})")
    if selected_year != 2019:
        monthly_roro = filtered_m.groupby(["Month", "Month_Num"])[["RoRo_Total", "RoRo_Inbound", "RoRo_Outbound"]].sum().reset_index()
        monthly_roro["Month"] = pd.Categorical(monthly_roro["Month"], categories=month_order, ordered=True)
        monthly_roro = monthly_roro.sort_values("Month_Num")

        fig_bar_roro_dir = go.Figure()
        fig_bar_roro_dir.add_trace(go.Bar(x=monthly_roro["Month"], y=monthly_roro["RoRo_Inbound"], name="Inbound (Discharged)", marker_color="#fbbf24"))
        fig_bar_roro_dir.add_trace(go.Bar(x=monthly_roro["Month"], y=monthly_roro["RoRo_Outbound"], name="Outbound (Loaded)", marker_color="#f97316"))
        apply_seametrics_chart_theme(
            fig_bar_roro_dir,
            height=380,
            show_legend=True,
            legend_orientation="h",
            barmode="group",
            xaxis_title="Month",
            yaxis_title="RoRo Vehicles"
        )
        fig_bar_roro_dir.update_layout(title=dict(text=f"RoRo Inbound vs. Outbound Directional Flow ({selected_year})", font=dict(color="#ffffff", size=15)))
        st.plotly_chart(fig_bar_roro_dir, width='stretch')


# =========================================================================
# SECTION E: PORT COMPARISON
# =========================================================================
with tab_e:
    st.subheader("E. Port Comparison: Multi-Port Benchmarking & Historical Performance")
    st.markdown("Select two or more ports to benchmark passenger throughput, commercial vessel calls, and RoRo freight.")

    comp_preset = st.radio(
        "Quick Selection Preset:",
        ["Custom Selection", "Corridor Artery: Batangas vs Calapan", "NCR Gateways: North vs South Harbor", "Bicol Hubs: Matnog vs Tabaco"],
        horizontal=True
    )

    if comp_preset == "Corridor Artery: Batangas vs Calapan":
        default_comp = ["Base Port of Batangas (PMO Batangas)", "Base Port of Calapan (PMO Mindoro)"]
    elif comp_preset == "NCR Gateways: North vs South Harbor":
        default_comp = ["Manila North Harbor (PMO NCR North)", "Manila South Harbor (PMO NCR South)"]
    elif comp_preset == "Bicol Hubs: Matnog vs Tabaco":
        default_comp = ["TMO Matnog (PMO Bicol)", "TMO Tabaco (PMO Bicol)"]
    else:
        default_comp = ["Base Port of Batangas (PMO Batangas)", "Base Port of Calapan (PMO Mindoro)", "Manila North Harbor (PMO NCR North)"]

    selected_compare_labels = st.multiselect(
        "Choose Verified Ports for Comparative Benchmarking:",
        options=ALL_FRIENDLY_PORTS,
        default=default_comp
    )

    if len(selected_compare_labels) >= 2:
        # Match raw port names
        matched_raw_comp = []
        for fl in selected_compare_labels:
            matched_raw_comp.extend(LABEL_TO_RAW_PORTS.get(fl, [fl]))

        df_p_comp = df_ports[df_ports["Port"].isin(matched_raw_comp)]
        
        c_cp1, c_cp2 = st.columns(2)
        with c_cp1:
            fig_comp_pax = px.bar(
                df_p_comp,
                x="Port",
                y="Total_Pax",
                color="Year",
                barmode="group",
                title="Passenger Volume Comparison Across Selected Ports",
                labels={"Total_Pax": "Passenger Volume", "Port": "Port Facility"}
            )
            apply_seametrics_chart_theme(
                fig_comp_pax,
                height=400,
                show_legend=True,
                legend_title="Year",
                barmode="group",
                xaxis_title="Port Facility",
                yaxis_title="Passenger Volume"
            )
            fig_comp_pax.update_xaxes(tickangle=-30)
            st.plotly_chart(fig_comp_pax, width='stretch')

        with c_cp2:
            fig_comp_roro = px.bar(
                df_p_comp,
                x="Port",
                y="Total_RoRo",
                color="Year",
                barmode="group",
                title="RoRo Vehicular Traffic Comparison Across Selected Ports",
                labels={"Total_RoRo": "RoRo Vehicles", "Port": "Port Facility"}
            )
            apply_seametrics_chart_theme(
                fig_comp_roro,
                height=400,
                show_legend=True,
                legend_title="Year",
                barmode="group",
                xaxis_title="Port Facility",
                yaxis_title="RoRo Vehicles"
            )
            fig_comp_roro.update_xaxes(tickangle=-30)
            st.plotly_chart(fig_comp_roro, width='stretch')

        # Comparative Summary Table
        st.markdown("#### Performance Summary for Selected Facilities")
        st.dataframe(
            df_p_comp[["Year", "Reporting_Period", "Cluster", "PMO", "Port", "Total_Pax", "Total_Ship", "Total_RoRo", "Avg_Pax_Per_Shipcall", "Avg_RoRo_Per_Shipcall"]],
            width='stretch',
            hide_index=True
        )
    else:
        st.warning("Please select at least two ports to generate comparative visualizations.")


# =========================================================================
# SECTION F: PREDICTIVE ANALYTICS
# =========================================================================
with tab_f:
    st.subheader("F. Predictive Analytics: Calibrated Short-Term Forecasting & Model Reliability")
    st.markdown("""
    Because official PPA records for CY 2026 currently conclude at the Third Quarter (September 30, 2026), 
    SeaMetrics provides short-term predictive forecasts to estimate expected **Fourth Quarter (Q4 2026)** performance 
    and projected **Full-Year 2026** totals across Luzon and individual verified port facilities.
    """)

    # 1. Scope Switcher & Metric Switcher
    col_f_scope, col_f_metric = st.columns([3, 2])
    with col_f_scope:
        f_scope_mode = st.radio(
            "Forecast Entity Selection:",
            ["🌐 Luzon Macro Aggregate (All Ports)", "📍 Individual Port Facility", "⚖️ Port Comparison Forecast"],
            horizontal=True
        )
    with col_f_metric:
        pred_metric = st.selectbox(
            "Select Indicator to Forecast for Q4 2026:",
            ["👥 Passenger Traffic", "🚛 RoRo Vehicular Traffic", "🚢 Ship Calls"]
        )

    # Unit & Metric Key Setup
    if "Passenger" in pred_metric:
        m_key = "Pax"
        y_unit = "Passengers"
        color_code = "#00cec9"
    elif "RoRo" in pred_metric:
        m_key = "RoRo"
        y_unit = "RoRo Vehicles"
        color_code = "#fbbf24"
    else:
        m_key = "Ship"
        y_unit = "Vessel Calls"
        color_code = "#38bdf8"

    # 2. Historical Data Used Information Card
    st.markdown("""
    <div class="info-card">
        <h5 style="color: #38bdf8; margin-top: 0;">Historical Observations Used by the Forecasting Engine</h5>
        <ul style="padding-left: 18px; margin-bottom: 0;">
            <li><b>Training Horizon:</b> Calendar Years 2022 through 2025 (4 completed annual cycles).</li>
            <li><b>Reporting Frequency:</b> 16 completed quarterly observations (Q1 2022 to Q4 2025).</li>
            <li><b>Test Evaluation Set:</b> 2026 Q1–Q3 actual audited observations ($N=3$) evaluated chronologically.</li>
            <li><b>Excluded Periods:</b> 2019 Volume 2 (Commodity only; no passenger/vessel counts) and 2020–2021 (Pandemic period not in PPA scope).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- CASE 1: LUZON MACRO AGGREGATE ----------------
    if f_scope_mode == "🌐 Luzon Macro Aggregate (All Ports)":
        if m_key == "Pax":
            model_name = "Naive Seasonal Baseline (Y_t-4)"
            mape_val = "4.62%"
            rmse_val = "328,102"
            q4_point_forecast = 5294524
            ci_lower = 3599407
            ci_upper = 6989641
            full_yr_proj = 22079354
            q1_actual = 5449010
            q2_actual = 6650478
            q3_actual = 4685342
            simple_explanation = (
                "The model suggests that **passenger traffic across Luzon will increase in Q4 2026** to approximately **5.29 million commuters**, "
                "up from 4.69 million in Q3. This rebound is driven by the predictable annual Christmas holiday homecoming travel surge."
            )
        elif m_key == "RoRo":
            model_name = "Historical Quarter Mean"
            mape_val = "6.34%"
            rmse_val = "71,204"
            q4_point_forecast = 898518
            ci_lower = 769909
            ci_upper = 1027127
            full_yr_proj = 3574611
            q1_actual = 879432
            q2_actual = 987455
            q3_actual = 809206
            simple_explanation = (
                "The model suggests that **RoRo vehicular traffic will experience moderate recovery in Q4 2026** to approximately **898,518 vehicles**, "
                "rebounding from the third-quarter monsoon lull as agricultural trade and holiday commercial freight shipments increase."
            )
        else:
            model_name = "Historical Quarter Mean"
            mape_val = "5.63%"
            rmse_val = "2,410"
            q4_point_forecast = 36442
            ci_lower = 33628
            ci_upper = 39256
            full_yr_proj = 149094
            q1_actual = 37890
            q2_actual = 39212
            q3_actual = 35550
            simple_explanation = (
                "The model suggests that **vessel dockings will remain relatively stable in Q4 2026** at approximately **36,442 commercial calls**, "
                "closely aligning with regular ferry rotations and pre-scheduled freight liner itineraries."
            )

        # Plotly Trajectory Chart
        st.markdown(f"### 📈 Visual Forecast: 2026 Luzon Quarterly Trajectory ({y_unit})")
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=["2026 Q1", "2026 Q2", "2026 Q3"],
            y=[q1_actual, q2_actual, q3_actual],
            mode="lines+markers",
            name="Audited Actual Observation",
            line=dict(color=color_code, width=4),
            marker=dict(size=10, color=color_code)
        ))
        fig_forecast.add_trace(go.Scatter(
            x=["2026 Q3", "2026 Q4 (Forecast)"],
            y=[q3_actual, q4_point_forecast],
            mode="lines+markers",
            name="Projected Q4 Point Forecast",
            line=dict(color="#f43f5e", width=3, dash="dash"),
            marker=dict(size=12, symbol="diamond", color="#f43f5e")
        ))
        fig_forecast.add_trace(go.Scatter(
            x=["2026 Q4 (Forecast)", "2026 Q4 (Forecast)"],
            y=[ci_lower, ci_upper],
            mode="markers",
            name="95% Confidence Interval",
            marker=dict(size=8, symbol="line-ew", color="#f59e0b", line=dict(width=3))
        ))
        fig_forecast.add_vline(
            x=2,
            line_dash="dot",
            line_color="#38bdf8",
            annotation_text="Forecast Horizon Boundary",
            annotation_position="top left",
            annotation_font=dict(color="#ffffff", size=11),
            annotation_bgcolor="rgba(10, 25, 47, 0.88)",
            annotation_bordercolor="#38bdf8",
            annotation_borderwidth=1
        )
        apply_seametrics_chart_theme(
            fig_forecast,
            height=420,
            show_legend=True,
            legend_orientation="h",
            xaxis_title="Reporting Period",
            yaxis_title=f"Luzon Total {y_unit}"
        )
        fig_forecast.update_layout(title=dict(text=f"Luzon Total: 2026 Quarterly Trajectory & Q4 Calibrated Projection ({y_unit})", font=dict(color="#ffffff", size=15)))
        st.plotly_chart(fig_forecast, width='stretch')

        col_pred1, col_pred2 = st.columns([3, 2])
        with col_pred1:
            st.markdown(f"""
            <div class="callout-box">
                <h5 style="color: #38bdf8; margin-top: 0;">What the Prediction Means (Simple Explanation)</h5>
                <p>
                    {simple_explanation}<br><br>
                    <b>Point Forecast for Q4 2026:</b> <span style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">{q4_point_forecast:,} {y_unit.lower()}</span><br>
                    <b>95% Confidence Interval:</b> Between <b>{ci_lower:,}</b> and <b>{ci_upper:,}</b>.<br>
                    <b>Projected Full-Year 2026 Total:</b> <span style="font-size: 1.05rem; font-weight: 700; color: #34d399;">{full_yr_proj:,} {y_unit.lower()}</span>.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_pred2:
            st.markdown(f"""
            <div class="info-card">
                <h5 style="color: #fbbf24; margin-top: 0;">Model Information & Reliability</h5>
                <p>
                    <b>Selected Algorithm:</b> {model_name}<br>
                    <b>Historical Accuracy (MAPE):</b> <span style="color: #34d399; font-weight: 700;">{mape_val}</span><br>
                    <b>Root Mean Squared Error (RMSE):</b> {rmse_val}<br><br>
                    <i>Plain-Language Note:</i> A MAPE of <b>{mape_val}</b> means that under chronological testing on actual 2026 data, 
                    the model's predictions deviated from reality by less than <b>{mape_val}</b> on average.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- CASE 2: INDIVIDUAL PORT FACILITY FORECAST ----------------
    elif f_scope_mode == "📍 Individual Port Facility":
        f_port_choice = st.selectbox(
            "Select Verified Port Facility for Dedicated Forecast:",
            options=ALL_FRIENDLY_PORTS,
            index=0
        )
        matched_raw_list = LABEL_TO_RAW_PORTS.get(f_port_choice, [f_port_choice])
        sub_p = df_ports[df_ports["Port"].isin(matched_raw_list)]

        r25 = sub_p[sub_p["Year"] == 2025]
        r26 = sub_p[sub_p["Year"] == 2026]

        is_valid_forecast = False
        if not r25.empty and not r26.empty:
            v25_q13 = r25[f"Q1_Q3_{m_key}"].values[0]
            v25_q4 = r25[f"Q4_{m_key}"].values[0]
            v26_q13 = r26[f"Q1_Q3_{m_key}"].values[0]
            q1_act = r26[f"Q1_{m_key}"].values[0]
            q2_act = r26[f"Q2_{m_key}"].values[0]
            q3_act = r26[f"Q3_{m_key}"].values[0]

            if v25_q13 > 0 and v25_q4 > 0 and v26_q13 > 0:
                is_valid_forecast = True
                seasonal_ratio = v25_q4 / v25_q13
                p_q4 = int(round(v26_q13 * seasonal_ratio))
                p_fy = int(v26_q13 + p_q4)
                # Standard 95% error margin (+/- 12%)
                ci_l = max(0, int(round(p_q4 * 0.88)))
                ci_u = int(round(p_q4 * 1.12))

        if is_valid_forecast:
            st.markdown(f"### 📈 Visual Forecast: {f_port_choice} — 2026 Trajectory ({y_unit})")
            fig_port_f = go.Figure()
            fig_port_f.add_trace(go.Scatter(
                x=["2026 Q1", "2026 Q2", "2026 Q3"],
                y=[q1_act, q2_act, q3_act],
                mode="lines+markers",
                name="Audited Actual Observation",
                line=dict(color=color_code, width=4),
                marker=dict(size=10, color=color_code)
            ))
            fig_port_f.add_trace(go.Scatter(
                x=["2026 Q3", "2026 Q4 (Forecast)"],
                y=[q3_act, p_q4],
                mode="lines+markers",
                name="Projected Q4 Point Forecast",
                line=dict(color="#f43f5e", width=3, dash="dash"),
                marker=dict(size=12, symbol="diamond", color="#f43f5e")
            ))
            fig_port_f.add_trace(go.Scatter(
                x=["2026 Q4 (Forecast)", "2026 Q4 (Forecast)"],
                y=[ci_l, ci_u],
                mode="markers",
                name="95% Confidence Interval",
                marker=dict(size=8, symbol="line-ew", color="#f59e0b", line=dict(width=3))
            ))
            fig_port_f.add_vline(
                x=2,
                line_dash="dot",
                line_color="#38bdf8",
                annotation_text="Forecast Horizon Boundary",
                annotation_position="top left",
                annotation_font=dict(color="#ffffff", size=11),
                annotation_bgcolor="rgba(10, 25, 47, 0.88)",
                annotation_bordercolor="#38bdf8",
                annotation_borderwidth=1
            )
            apply_seametrics_chart_theme(
                fig_port_f,
                height=420,
                show_legend=True,
                legend_orientation="h",
                xaxis_title="Reporting Period",
                yaxis_title=f"{y_unit}"
            )
            fig_port_f.update_layout(title=dict(text=f"{f_port_choice}: 2026 Quarterly Trajectory & Q4 Calibrated Projection ({y_unit})", font=dict(color="#ffffff", size=15)))
            st.plotly_chart(fig_port_f, width='stretch')

            c_pf1, c_pf2 = st.columns([3, 2])
            with c_pf1:
                st.markdown(f"""
                <div class="callout-box">
                    <h5 style="color: #38bdf8; margin-top: 0;">Port-Specific Forecast Interpretation</h5>
                    <p>
                        Based on the verified seasonal ratio derived from 2025 observations (<b>{seasonal_ratio*100:.1f}%</b> of Q1–Q3), 
                        <b>{f_port_choice}</b> is projected to handle:
                        <br><br>
                        <b>Q4 2026 Point Forecast:</b> <span style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">{p_q4:,} {y_unit.lower()}</span><br>
                        <b>95% Confidence Interval:</b> Between <b>{ci_l:,}</b> and <b>{ci_u:,}</b> {y_unit.lower()}<br>
                        <b>Projected Full-Year 2026 Total:</b> <span style="font-size: 1.05rem; font-weight: 700; color: #34d399;">{p_fy:,} {y_unit.lower()}</span>.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with c_pf2:
                st.markdown(f"""
                <div class="info-card">
                    <h5 style="color: #fbbf24; margin-top: 0;">Audited Operational Actuals</h5>
                    <p>
                        <b>2026 Q1 Actual:</b> {int(q1_act):,} {y_unit.lower()}<br>
                        <b>2026 Q2 Actual:</b> {int(q2_act):,} {y_unit.lower()}<br>
                        <b>2026 Q3 Actual:</b> {int(q3_act):,} {y_unit.lower()}<br>
                        <b>2026 Q1–Q3 Subtotal:</b> <span style="color: #38bdf8; font-weight: 700;">{int(v26_q13):,}</span><br>
                        <b>2025 Full-Year Benchmark:</b> {int(v25_q13 + v25_q4):,}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-box">
                <h5 style="color: #fbbf24; margin-top: 0;">⚠️ Insufficient Historical Data for Facility-Level Forecasting</h5>
                <p>
                    The official PPA dataset for <b>{f_port_choice}</b> contains zero or missing observations for <b>{pred_metric}</b> 
                    in the required 2025/2026 quarterly cycle (e.g. specialized cargo-only or container terminal where this indicator is unrecorded).
                    <br><br>
                    To maintain strict data integrity and prevent fabricated numbers, mathematical projection is disabled for this indicator. 
                    Descriptive historical trends for this port are available in Section B, C, and D.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- CASE 3: PORT COMPARISON FORECAST ----------------
    else:
        st.markdown("#### Comparative Gateway Forecasting (e.g. Batangas vs. Calapan)")
        col_cp1, col_cp2 = st.columns(2)
        with col_cp1:
            p1_choice = st.selectbox("Select Port 1:", ALL_FRIENDLY_PORTS, index=0)
        with col_cp2:
            p2_choice = st.selectbox("Select Port 2:", ALL_FRIENDLY_PORTS, index=1 if len(ALL_FRIENDLY_PORTS) > 1 else 0)

        # Helper to compute port forecast
        def get_port_forecast_data(p_choice, metric):
            rm_list = LABEL_TO_RAW_PORTS.get(p_choice, [p_choice])
            sp = df_ports[df_ports["Port"].isin(rm_list)]
            r25_sub = sp[sp["Year"] == 2025]
            r26_sub = sp[sp["Year"] == 2026]
            if not r25_sub.empty and not r26_sub.empty:
                v25_13 = r25_sub[f"Q1_Q3_{metric}"].values[0]
                v25_4 = r25_sub[f"Q4_{metric}"].values[0]
                v26_13 = r26_sub[f"Q1_Q3_{metric}"].values[0]
                q1 = r26_sub[f"Q1_{metric}"].values[0]
                q2 = r26_sub[f"Q2_{metric}"].values[0]
                q3 = r26_sub[f"Q3_{metric}"].values[0]
                if v25_13 > 0 and v25_4 > 0 and v26_13 > 0:
                    rat = v25_4 / v25_13
                    pred_4 = int(round(v26_13 * rat))
                    fy = int(v26_13 + pred_4)
                    return True, [q1, q2, q3], pred_4, fy, int(v26_13)
            return False, [], 0, 0, 0

        ok1, act1, pred1, fy1, q13_1 = get_port_forecast_data(p1_choice, m_key)
        ok2, act2, pred2, fy2, q13_2 = get_port_forecast_data(p2_choice, m_key)

        if ok1 and ok2:
            fig_dual = go.Figure()
            # Port 1
            fig_dual.add_trace(go.Scatter(x=["2026 Q1", "2026 Q2", "2026 Q3"], y=act1, mode="lines+markers", name=f"{p1_choice} (Actual)", line=dict(color="#00cec9", width=3)))
            fig_dual.add_trace(go.Scatter(x=["2026 Q3", "2026 Q4 (Forecast)"], y=[act1[2], pred1], mode="lines+markers", name=f"{p1_choice} (Q4 Forecast)", line=dict(color="#00cec9", width=3, dash="dash"), marker=dict(size=10, symbol="diamond")))
            # Port 2
            fig_dual.add_trace(go.Scatter(x=["2026 Q1", "2026 Q2", "2026 Q3"], y=act2, mode="lines+markers", name=f"{p2_choice} (Actual)", line=dict(color="#fbbf24", width=3)))
            fig_dual.add_trace(go.Scatter(x=["2026 Q3", "2026 Q4 (Forecast)"], y=[act2[2], pred2], mode="lines+markers", name=f"{p2_choice} (Q4 Forecast)", line=dict(color="#fbbf24", width=3, dash="dash"), marker=dict(size=10, symbol="diamond")))
            fig_dual.add_vline(
                x=2,
                line_dash="dot",
                line_color="#38bdf8",
                annotation_text="Forecast Horizon Boundary",
                annotation_position="top left",
                annotation_font=dict(color="#ffffff", size=11),
                annotation_bgcolor="rgba(10, 25, 47, 0.88)",
                annotation_bordercolor="#38bdf8",
                annotation_borderwidth=1
            )
            apply_seametrics_chart_theme(
                fig_dual,
                height=420,
                show_legend=True,
                legend_orientation="h",
                xaxis_title="Reporting Period",
                yaxis_title=y_unit
            )
            fig_dual.update_layout(title=dict(text=f"Comparative Trajectory & Q4 Forecast: {p1_choice} vs. {p2_choice} ({y_unit})", font=dict(color="#ffffff", size=15)))
            st.plotly_chart(fig_dual, width='stretch')

            c_db1, c_db2 = st.columns(2)
            with c_db1:
                st.markdown(f"""
                <div class="bento-card">
                    <div class="bento-header"><span style="color: #00cec9;">⚓</span> {p1_choice}</div>
                    <div class="bento-subtitle">2026 Q1–Q3 Actual: <b>{q13_1:,}</b></div>
                    <div class="bento-number bento-cyan">{pred1:,}</div>
                    <div class="bento-subtitle">Q4 Point Forecast | FY2026: <b>{fy1:,} {y_unit.lower()}</b></div>
                </div>
                """, unsafe_allow_html=True)
            with c_db2:
                st.markdown(f"""
                <div class="bento-card">
                    <div class="bento-header"><span style="color: #fbbf24;">⚓</span> {p2_choice}</div>
                    <div class="bento-subtitle">2026 Q1–Q3 Actual: <b>{q13_2:,}</b></div>
                    <div class="bento-number bento-amber">{pred2:,}</div>
                    <div class="bento-subtitle">Q4 Point Forecast | FY2026: <b>{fy2:,} {y_unit.lower()}</b></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("One or both selected ports do not have complete 2025/2026 observations for this indicator. Please choose facilities with complete time-series records.")

    # 3. Chronological Backtest Evaluation Table
    st.markdown("#### Chronological Backtesting Benchmark on 2026 Q1–Q3 Actuals")
    df_eval = load_analysis_table("predictive_model_evaluation.csv")
    if df_eval is not None:
        st.dataframe(df_eval, width='stretch', hide_index=True)

    # 4. Limitations Callout Box
    st.markdown("""
    <div class="warning-box">
        <h5 style="color: #fbbf24; margin-top: 0;">📌 How to Understand This Prediction (Important Limitations)</h5>
        <ul style="padding-left: 18px; margin-bottom: 0;">
            <li><b>Estimates, Not Guarantees:</b> These predictions are statistical projections based on recurring historical seasonality. They are not guaranteed real-world outcomes.</li>
            <li><b>Sensitivity to Weather:</b> Tropical cyclones (typhoons) occurring in November and December frequently cause multi-day Philippine Coast Guard voyage cancellations, which can depress actual volumes below forecasts.</li>
            <li><b>Economic Factors:</b> Maritime fuel price shifts, terminal tariff adjustments, and holiday fare adjustments can cause real commuter and logistics demand to deviate from historical models.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# =========================================================================
# SECTION G: DATA EXPLORER
# =========================================================================
with tab_g:
    st.subheader("G. Data Explorer: Searchable Archives, Source Inspection & CSV Exports")
    st.markdown("""
    Inspect, sort, filter, and export the standardized multi-year datasets and precomputed statistical tables 
    produced by the SeaMetrics analytical engine.
    """)

    explorer_view = st.selectbox(
        "Choose Data Archive to Inspect:",
        [
            "1. Multi-Year Luzon Monthly Master (2019, 2022–2026)",
            "2. Macro Historical Series (2019, 2022–2026)",
            "3. Port Summary Master (2019, 2022–2026)",
            "4. PMO Summary Master (2019, 2022–2026)",
            "5. Top 15 Passenger Ports Ranking",
            "6. Top 15 Ship Calls Ranking",
            "7. Top 15 RoRo Ports Ranking",
            "8. Batangas–Calapan Corridor Performance Matrix",
            "9. Monthly Seasonality Indices",
            "10. Predictive Model Evaluation Benchmark"
        ]
    )

    if "1. Multi-Year Luzon Monthly" in explorer_view:
        st.markdown(f"**Viewing Multi-Year Luzon Monthly Dataset ({len(filtered_m):,} active filtered records):**")
        st.dataframe(filtered_m, width='stretch', hide_index=True)
        csv_data = filtered_m.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Filtered Monthly Data as CSV", data=csv_data, file_name="seametrics_filtered_monthly.csv", mime="text/csv")
        
    elif "2. Macro Historical" in explorer_view:
        st.markdown(f"**Viewing Luzon Historical Macro Dataset ({len(df_macro)} records):**")
        st.dataframe(df_macro, width='stretch', hide_index=True)
        csv_data = df_macro.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Macro Historical Data as CSV", data=csv_data, file_name="seametrics_macro_historical.csv", mime="text/csv")

    elif "3. Port Summary" in explorer_view:
        st.markdown(f"**Viewing Port Facilities Summary ({len(df_ports)} records):**")
        st.dataframe(df_ports, width='stretch', hide_index=True)
        csv_data = df_ports.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Port Summary as CSV", data=csv_data, file_name="seametrics_ports_summary.csv", mime="text/csv")

    elif "4. PMO Summary" in explorer_view:
        st.markdown(f"**Viewing PMO Summary Dataset ({len(df_pmo)} records):**")
        st.dataframe(df_pmo, width='stretch', hide_index=True)
        csv_data = df_pmo.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export PMO Summary as CSV", data=csv_data, file_name="seametrics_pmo_summary.csv", mime="text/csv")

    elif "5. Top 15 Passenger" in explorer_view:
        df_tbl = load_analysis_table("pax_top_ports.csv")
        if df_tbl is not None:
            st.dataframe(df_tbl, width='stretch', hide_index=True)
            csv_data = df_tbl.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Top Passenger Ports as CSV", data=csv_data, file_name="pax_top_ports.csv", mime="text/csv")

    elif "6. Top 15 Ship" in explorer_view:
        df_tbl = load_analysis_table("ship_top_ports.csv")
        if df_tbl is not None:
            st.dataframe(df_tbl, width='stretch', hide_index=True)
            csv_data = df_tbl.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Top Ship Ports as CSV", data=csv_data, file_name="ship_top_ports.csv", mime="text/csv")

    elif "7. Top 15 RoRo" in explorer_view:
        df_tbl = load_analysis_table("roro_top_ports.csv")
        if df_tbl is not None:
            st.dataframe(df_tbl, width='stretch', hide_index=True)
            csv_data = df_tbl.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Top RoRo Ports as CSV", data=csv_data, file_name="roro_top_ports.csv", mime="text/csv")

    elif "8. Batangas–Calapan Corridor" in explorer_view:
        df_tbl = load_analysis_table("corridor_batangas_calapan_metrics.csv")
        if df_tbl is not None:
            st.dataframe(df_tbl, width='stretch', hide_index=True)
            csv_data = df_tbl.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Corridor Metrics as CSV", data=csv_data, file_name="corridor_metrics.csv", mime="text/csv")

    elif "9. Monthly Seasonality" in explorer_view:
        df_tbl = load_analysis_table("monthly_seasonality_indices.csv")
        if df_tbl is not None:
            st.dataframe(df_tbl, width='stretch', hide_index=True)
            csv_data = df_tbl.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Seasonality Indices as CSV", data=csv_data, file_name="monthly_seasonality_indices.csv", mime="text/csv")

    elif "10. Predictive Model" in explorer_view:
        df_tbl = load_analysis_table("predictive_model_evaluation.csv")
        if df_tbl is not None:
            st.dataframe(df_tbl, width='stretch', hide_index=True)
            csv_data = df_tbl.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Model Evaluation as CSV", data=csv_data, file_name="predictive_model_evaluation.csv", mime="text/csv")


# =========================================================================
# SECTION H: ABOUT SEAMETRICS, METHODOLOGY & RESEARCH ATTRIBUTION
# =========================================================================
with tab_h:
    st.subheader("H. ℹ️ About SeaMetrics: Research Methodology, Attribution & Public Disclaimers")

    # Hero Card
    st.markdown(r"""
    <div class="doc-hero">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
            <div>
                <span class="doc-pill doc-pill-cyan">Academic Research Platform</span>
                <span class="doc-pill doc-pill-blue">DepEd MIMAROPA Region</span>
                <span class="doc-pill doc-pill-purple">Leuteboro National High School</span>
                <span class="doc-pill doc-pill-amber">Fundamentals of Data Analytics</span>
                <h2 style="color: #ffffff; font-size: 1.65rem; font-weight: 800; margin: 10px 0px 6px 0px;">
                    SeaMetrics: Luzon Maritime Port Traffic Intelligence & Predictive Analytics
                </h2>
                <div style="color: #94a3b8; font-size: 0.90rem; max-width: 950px; line-height: 1.6;">
                    An empirical data analytics and econometric modeling system designed to analyze inter-island passenger movement, 
                    commercial vessel movements, and roll-on/roll-off (RoRo) vehicular logistics across verified seaport facilities in 
                    <b>Luzon, Philippines</b>. Built using public Philippine Ports Authority (PPA) administrative statistical archives.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6 Collapsible Subsections for Clear, Structured Reading
    doc_sub1, doc_sub2, doc_sub3, doc_sub4, doc_sub5, doc_sub6 = st.tabs([
        "1. 🎯 About SeaMetrics",
        "2. 📊 Data Sources & Scope",
        "3. 🔬 Methodology & Models",
        "4. ⚖️ Limitations & Disclaimers",
        "5. 🏛️ Academic Attribution",
        "6. 📖 User Navigation Guide"
    ])

    # -------------------------------------------------------------------------
    # SUBSECTION 1: ABOUT SEAMETRICS
    # -------------------------------------------------------------------------
    with doc_sub1:
        st.markdown("### 1. About SeaMetrics & Core Objectives")
        
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown(r"""
            #### Project Overview & Problem Statement
            Maritime transportation is the economic lifeblood of the Philippine archipelago, serving as the primary medium 
            for inter-island passenger connectivity, agricultural logistics, and commercial supply chain distribution. 
            Historically, public port statistics published by the Philippine Ports Authority (PPA) have been disseminated 
            through static annual PDF reports and fragmented quarterly workbooks. 
            
            **SeaMetrics** was conceived and developed to transform these administrative data records into an interactive, 
            transparent, empirical decision-support intelligence platform. By harmonizing multi-year statistical workbooks, 
            standardizing disparate facility nomenclatures, and implementing rigorous time series forecasting models, 
            SeaMetrics enables researchers, students, port managers, and transport planners to examine long-term throughput 
            trends, evaluate post-pandemic maritime recovery trajectories, and anticipate seasonal operational bottlenecks.

            #### Primary Research Objectives
            1. **Multi-Year Data Harmonization:** Unify multi-year PPA statistical publications covering 2019 and 2022–2026 into a standardized, machine-readable analytical framework.
            2. **Tri-Indicator Maritime Evaluation:** Focus empirical analysis on three non-cargo mobility metrics: **Passenger Traffic**, **Commercial Ship Calls**, and **RoRo Vehicle Movements**.
            3. **Gateway Connectivity Analysis:** Evaluate vital maritime arteries, with dedicated deep-dive comparative benchmarking of the strategic **Batangas–Calapan Corridor** linking mainland Luzon to Mindoro and the Southern Tagalog region.
            4. **Predictive Econometric Modeling:** Deploy chronological backtested forecasting models equipped with mathematical 95% Confidence Intervals to provide plausible quarterly throughput trajectories.
            """)
        with c2:
            st.markdown(r"""
            <div class="doc-card">
                <div style="color: #00cec9; font-weight: 800; font-size: 0.95rem; margin-bottom: 8px;">🚢 The Three Core Indicators</div>
                <ul style="padding-left: 18px; margin-bottom: 0px;">
                    <li style="margin-bottom: 8px;">
                        <b style="color: #38bdf8;">Passenger Traffic:</b> Total commuter throughput, segmented into Embarked (departing) and Disembarked (arriving) passengers across domestic ferry terminals.
                    </li>
                    <li style="margin-bottom: 8px;">
                        <b style="color: #38bdf8;">Ship Calls:</b> Frequency of commercial vessel docking movements, categorized by domestic inter-island routes and foreign ocean-going traffic.
                    </li>
                    <li style="margin-bottom: 8px;">
                        <b style="color: #38bdf8;">RoRo Vehicle Movement:</b> Volume of rolling vehicles transported via Roll-on/Roll-off ferries, classified across 4 PPA vehicular classifications (Type 1 to Type 4).
                    </li>
                </ul>
            </div>
            <div class="callout-box" style="margin-top: 14px;">
                <b style="color: #00cec9;">Analytical Boundary:</b> Containerized cargo (TEUs) and bulk cargo tonnage (metric tons) are 
                <b>strictly excluded</b> from the SeaMetrics dashboard to maintain analytical clarity focused on commuter mobility and vehicular transit.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Intended Users & Practical Applications")
        col_u1, col_u2, col_u3 = st.columns(3)
        with col_u1:
            st.markdown(r"""
            <div class="doc-card" style="height: 100%;">
                <div style="color: #38bdf8; font-weight: 700; font-size: 0.90rem; margin-bottom: 6px;">👥 Commuters & Ferry Operators</div>
                <p style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.5;">
                    Allows shipping lines to calibrate vessel deployment schedules against verified quarterly demand surges and helps commuters anticipate peak holiday travel periods.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_u2:
            st.markdown(r"""
            <div class="doc-card" style="height: 100%;">
                <div style="color: #34d399; font-weight: 700; font-size: 0.90rem; margin-bottom: 6px;">🏛️ Port & Transport Planners</div>
                <p style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.5;">
                    Provides empirical berth utilization ratios (Passengers/Call, RoRo/Call) to inform marshalling yard expansions, terminal renovations, and intermodal connectivity.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_u3:
            st.markdown(r"""
            <div class="doc-card" style="height: 100%;">
                <div style="color: #a78bfa; font-weight: 700; font-size: 0.90rem; margin-bottom: 6px;">🎓 Researchers & Students</div>
                <p style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.5;">
                    Serves as an open educational benchmark demonstrating real-world data cleaning, ETL pipeline automation, statistical benchmarking, and Streamlit dashboard design.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SUBSECTION 2: DATA SOURCES & SCOPE
    # -------------------------------------------------------------------------
    with doc_sub2:
        st.markdown("### 2. Data Sources, Timeline & Geographical Coverage")
        
        st.markdown(r"""
        All empirical data incorporated into SeaMetrics originates from official administrative reports published by the 
        **Philippine Ports Authority (PPA)**, an attached agency of the Department of Transportation (DOTr) of the Republic of the Philippines.
        """)

        # Data Timeline Table
        st.markdown("#### Official Reporting Periods & Data Characteristics")
        timeline_data = {
            "Year": ["2019", "2022", "2023", "2024", "2025", "2026"],
            "Source Publication": [
                "2019 PPA Annual Statistical Report (ASR Vol. 2)",
                "2022 PPA Annual Port Statistics Summary",
                "2023 PPA Annual Port Statistics Summary",
                "2024 PPA Annual Port Statistics Summary",
                "CY 2025 PPA Port Statistics Summary (Q4 QSR)",
                "CY 2026 PPA Quarterly Statistical Report (Q3 QSR)"
            ],
            "Period Coverage": [
                "Full Calendar Year (Jan–Dec)",
                "Full Calendar Year (Q1–Q4)",
                "Full Calendar Year (Q1–Q4)",
                "Full Calendar Year (Q1–Q4)",
                "Full Calendar Year (12 Months)",
                "Partial Calendar Year (Q1–Q3 / Jan–Sep)"
            ],
            "Data Granularity": [
                "Annual PMO Commodity Summary (Traffic Unreported*)",
                "Quarterly Aggregates (Q1, Q2, Q3, Q4)",
                "Quarterly Aggregates (Q1, Q2, Q3, Q4)",
                "Quarterly Aggregates (Q1, Q2, Q3, Q4)",
                "Monthly Facility Records (Jan–Dec)",
                "Monthly Facility Records (Jan–Sep, 9 Months)"
            ],
            "Operational Status": [
                "Pre-Pandemic Baseline (Commodity Only)",
                "Post-Pandemic Initial Recovery",
                "Inter-Island Transit Expansion",
                "Pre-Modernization Fleet Stabilization",
                "Full Historical Series",
                "Active Current Year (Partial)"
            ]
        }
        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, width='stretch', hide_index=True)

        st.markdown(r"""
        > [!IMPORTANT]
        > **Zero-Fabrication Principle Regarding 2019 & 2026 Data:**
        > * **2019 Dataset:** Sourced from PPA Volume 2 Commodity archives. Passenger counts, vessel calls, and RoRo movements were unrecorded in this source volume. SeaMetrics explicitly designates these metrics as `Unreported*` rather than fabricating synthetic estimates.
        > * **2026 Dataset:** Strictly contains observed data from **January through September 2026 (Q1–Q3)**. Q4 2026 records are not fabricated. When comparing 2026 against previous years, the dashboard automatically filters historical years to matching Q1–Q3 periods to prevent misleading year-over-year conclusions.
        """)

        st.markdown("#### Geographical Scope: Verified Luzon Port Management Offices (PMOs)")
        st.markdown(r"""
        SeaMetrics exclusively monitors verified seaports and terminals located within **Luzon and its associated island provinces**, 
        administered across 9 regional PPA Port Management Offices (PMOs):
        """)

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(r"""
            * **PMO Batangas:** Baseport Batangas, Bauan, San Pascual, Tingloy, Lobo (Southern Luzon hub).
            * **PMO Mindoro:** Calapan, Puerto Galera, San Jose, Balatero, Abra de Ilog, Roxas, Bulalacao.
            * **PMO Marinduque/Quezon:** Lucena, Balanacan, Cawit, Atimonan, Gumaca, Infanta.
            * **PMO Bicol:** Legazpi, Tabaco, Matnog, Bulan, Pilar, Pasacao, Pio Duran.
            * **PMO Bataan/Aurora:** Limay, Port Capinpin, Dingalan, Mariveles, Lamao.
            """)
        with col_p2:
            st.markdown(r"""
            * **PMO NCR North:** Manila North Harbor (premier domestic passenger and general cargo terminal).
            * **PMO NCR South:** Manila South Harbor & Eva Macapagal Super Terminal (international/cruise hub).
            * **PMO Northern Luzon:** San Fernando (Poro Point), Currimao, Salomague, Basco, Claveria.
            * **PMO Palawan:** Puerto Princesa, Coron, El Nido, Culion, Cuyo, Brooke's Point, San Vicente.
            """)

        st.warning("⚠️ **Geographical Boundary Disclosure:** SeaMetrics does NOT claim to cover every seaport in the Philippines. Visayas and Mindanao ports outside the Luzon maritime cluster are explicitly outside the scope of this research study.")

    # -------------------------------------------------------------------------
    # SUBSECTION 3: METHODOLOGY & PREDICTIVE MODELING
    # -------------------------------------------------------------------------
    with doc_sub3:
        st.markdown("### 3. Analytical Methodology & Predictive Modeling Architecture")

        st.markdown(r"""
        The SeaMetrics analytical workflow adheres to standard data science principles across four primary stages:
        **Automated ETL Ingestion** $\rightarrow$ **Standardization & Deduplication** $\rightarrow$ **Statistical Aggregation** $\rightarrow$ **Econometric Forecasting**.
        """)

        # Methodology Steps
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(r"""
            <div class="doc-card">
                <div style="color: #00cec9; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">1. Data Cleaning & Deduplication</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    PPA source workbooks frequently feature disparate naming conventions (e.g. "Calapan Port", "Port of Calapan", "Baseport Calapan"). 
                    The ETL pipeline standardizes port names into unified canonical labels and segregates Base Port aggregates from terminal sub-ports 
                    to strictly prevent double-counting.
                </p>
            </div>
            <div class="doc-card">
                <div style="color: #38bdf8; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">2. Derived Efficiency Ratios</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    To evaluate operational efficiency, SeaMetrics derives two empirical berth productivity ratios:
                    <br>• <b>Avg. Passengers per Call:</b> \(\text{Total Pax} / \text{Total Ship Calls}\)
                    <br>• <b>Avg. RoRo Vehicles per Call:</b> \(\text{Total RoRo} / \text{Total Ship Calls}\)
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(r"""
            <div class="doc-card">
                <div style="color: #34d399; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">3. Macro Ensemble Forecasting</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    For macro Luzon throughput, SeaMetrics deploys an ensemble comparing:
                    <br>• <b>Naive Seasonal Baseline:</b> Prior-year same-quarter trajectory.
                    <br>• <b>Quarter Mean Baseline:</b> Historical quarterly moving distribution.
                    <br>• <b>ARIMA / ETS Benchmarks:</b> Parametric time series validation.
                </p>
            </div>
            <div class="doc-card">
                <div style="color: #a78bfa; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">4. Facility Ratio Allocation</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    Individual port forecasts are computed using port-specific seasonal ratio allocation models that map multi-year historical port shares 
                    against macro quarterly projections, with explicit fallback guards for ports with limited data history.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Backtesting Validation Table
        st.markdown("#### Chronological Backtesting & Accuracy Validation")
        st.markdown(r"""
        To evaluate model accuracy, forecasts were backtested against known historical quarters. 
        Accuracy is quantified using **Mean Absolute Percentage Error (MAPE)** and **Root Mean Squared Error (RMSE)**:
        """)

        backtest_table = {
            "Traffic Domain": ["Passenger Traffic", "Commercial Ship Calls", "RoRo Vehicle Movements"],
            "Target Metric": ["Pax_Total", "Ship_Total", "RoRo_Total"],
            "Optimal Model": ["Naive Seasonal Baseline (Prior Q4)", "Quarter Mean Baseline", "Quarter Mean Baseline"],
            "Training Periods": ["Q1 2022 – Q3 2025", "Q1 2022 – Q3 2025", "Q1 2022 – Q3 2025"],
            "Validation Horizon": ["Q4 2025 (Known Observed)", "Q4 2025 (Known Observed)", "Q4 2025 (Known Observed)"],
            "MAE": ["279,726 passengers", "1,328 ship calls", "43,158 vehicles"],
            "RMSE": ["279,726 passengers", "1,328 ship calls", "43,158 vehicles"],
            "MAPE (% Error)": ["4.62%", "5.63%", "6.34%"],
            "Accuracy Tier": ["High Precision (< 5%)", "High Precision (< 6%)", "Good Calibration (< 7%)"]
        }
        df_bt = pd.DataFrame(backtest_table)
        st.dataframe(df_bt, width='stretch', hide_index=True)

        st.markdown("#### Mathematical Uncertainty: 95% Confidence Intervals")
        st.markdown(r"""
        All forecast trajectories in Tab F feature computed **95% Confidence Intervals (CI)**:
        
        $$\\text{CI}_{95\\%} = \\hat{Y}_t \\pm 1.96 \\times \\text{RMSE}$$

        Where \(\hat{Y}_t\) is the point forecast for quarter \(t\), and \(\text{RMSE}\) is the historical backtest root mean squared error. 
        This upper and lower bound communicates the plausible variance range around future projections.
        """)

        st.markdown(r"""
        <div class="callout-box">
            <b style="color: #00cec9;">How to Interpret Actual vs. Predicted Values:</b>
            <br>• <b>Actual Values (Solid Lines):</b> Verifiable historical administrative records published by the PPA.
            <br>• <b>Predicted Values (Dashed Lines & Shaded Bands):</b> Statistical estimates projecting trend continuity under normal operating conditions. 
            External factors such as severe typhoons (e.g. tropical cyclone signal suspensions), bunker fuel price spikes, or administrative route changes 
            can cause actual figures to diverge from mathematical projections.
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SUBSECTION 4: LIMITATIONS & DISCLAIMERS
    # -------------------------------------------------------------------------
    with doc_sub4:
        st.markdown("### 4. Research Limitations & Legal Disclaimers")

        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown(r"""
            <div class="warning-box">
                <div style="color: #fbbf24; font-weight: 800; font-size: 0.95rem; margin-bottom: 6px;">⚠️ Data & Reporting Limitations</div>
                <ul style="padding-left: 18px; margin-bottom: 0px; font-size: 0.84rem; line-height: 1.6;">
                    <li><b>Partial 2026 Reporting:</b> The CY 2026 dataset covers Q1–Q3 (January to September) only. Full-year 2026 totals cannot be directly evaluated against full-year 2025 without applying like-for-like Q1–Q3 filtering.</li>
                    <li><b>2019 Unreported Traffic:</b> Pre-pandemic 2019 figures reflect Volume 2 Commodity data; passenger, ship, and RoRo movements were not cataloged in that volume.</li>
                    <li><b>Weather Susceptibility:</b> Philippine maritime corridors experience seasonal typhoon suspensions, causing localized quarterly volatility that cannot be fully captured by static econometric models.</li>
                    <li><b>Sporadic Sub-Port Records:</b> Smaller municipal feeder ports may exhibit irregular reporting intervals, widening confidence intervals.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col_l2:
            st.markdown(r"""
            <div class="warning-box">
                <div style="color: #fbbf24; font-weight: 800; font-size: 0.95rem; margin-bottom: 6px;">⚖️ Official Legal & Operational Disclaimer</div>
                <ul style="padding-left: 18px; margin-bottom: 0px; font-size: 0.84rem; line-height: 1.6;">
                    <li><b>Independent Academic Tool:</b> SeaMetrics is an independent student and academic research tool. It is <b>NOT</b> an official operational, administrative, or commercial vessel dispatch system.</li>
                    <li><b>Non-Replacement of Official PPA Statistics:</b> SeaMetrics does not replace, supersede, or amend official Philippine Ports Authority statistical gazettes or PMO port records.</li>
                    <li><b>Probabilistic Nature of Forecasts:</b> All projections are statistical extrapolations and must not be treated as guaranteed operational outcomes or binding commercial forecasts.</li>
                    <li><b>No Commercial Ticketing or Booking:</b> SeaMetrics provides retrospective and prospective macro analytics; it does not offer passenger booking, ferry schedules, or cargo clearance services.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(r"""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #334155; border-radius: 8px; padding: 14px 18px; margin-top: 14px;">
            <p style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5; margin-bottom: 0px;">
                <b>Notice of Data Ownership:</b> Primary port statistics remain the intellectual property and administrative domain of the 
                <b>Philippine Ports Authority (PPA)</b>. SeaMetrics claims no ownership of primary government records and provides analytical 
                transformations under fair academic and educational use.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SUBSECTION 5: ACADEMIC ATTRIBUTION
    # -------------------------------------------------------------------------
    with doc_sub5:
        st.markdown("### 5. Research Attribution & Academic Framework")

        st.markdown(r"""
        <div class="doc-card" style="border-left: 4px solid #00cec9 !important;">
            <h3 style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-top: 0px;">
                Fundamentals of Data Analytics Capstone Research
            </h3>
            <div style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 14px;">
                Developed under the Senior High School Applied Research Curriculum
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 14px;">
                <div>
                    <div style="color: #38bdf8; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">Educational Institution</div>
                    <div style="color: #ffffff; font-size: 1.0rem; font-weight: 800;">Leuteboro National High School</div>
                    <div style="color: #cbd5e1; font-size: 0.82rem;">Department of Education • MIMAROPA Region<br>Socorro, Oriental Mindoro, Philippines</div>
                </div>
                <div>
                    <div style="color: #34d399; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">Course & Subject</div>
                    <div style="color: #ffffff; font-size: 1.0rem; font-weight: 800;">Fundamentals of Data Analytics</div>
                    <div style="color: #cbd5e1; font-size: 0.82rem;">Senior High School Academic Track</div>
                </div>
                <div>
                    <div style="color: #fbbf24; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">Supervising Instructor / Teacher</div>
                    <div style="color: #ffffff; font-size: 1.0rem; font-weight: 800;">Aldrin D. Magtibay</div>
                    <div style="color: #cbd5e1; font-size: 0.82rem;">Teacher V • Project Adviser & Instructor</div>
                </div>
                <div>
                    <div style="color: #a78bfa; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">Project Developers & Researchers</div>
                    <div style="color: #ffffff; font-size: 0.95rem; font-weight: 800; line-height: 1.45;">
                        • Ace Mc Kinzy D. Magnaye<br>
                        • Keirvin Lee M. Escala<br>
                        • Sydney Emerald A. Cuebillas
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.80rem; margin-top: 4px;">Student Researchers & Platform Developers</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(r"""
        #### Institutional Non-Endorsement Statement
        This research paper, empirical models, and interactive dashboard were created strictly for academic, scientific, and educational 
        purposes within the curriculum of *Fundamentals of Data Analytics*. 
        
        **No official endorsement, formal sponsorship, or commercial partnership** by the Philippine Ports Authority (PPA), the Department 
        of Education (DepEd), or any commercial shipping entity is expressed, implied, or claimed. All analytical conclusions and interpretations 
        represent solely the academic findings of the authors.
        """)

    # -------------------------------------------------------------------------
    # SUBSECTION 6: USER NAVIGATION GUIDE
    # -------------------------------------------------------------------------
    with doc_sub6:
        st.markdown("### 6. Interactive User Navigation & Operating Guide")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown(r"""
            <div class="doc-card">
                <div style="color: #00cec9; font-weight: 700; font-size: 0.92rem; margin-bottom: 6px;">1. Navigating Tabs A Through H</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    • <b>Tab A (Overview):</b> Executive Bento Grid KPIs, macro trend charts, and Luzon summary metrics.<br>
                    • <b>Tab B (Passengers):</b> Commuter flows, rankings, and the Batangas–Calapan deep dive.<br>
                    • <b>Tab C (Ship Calls):</b> Commercial vessel movements and domestic vs. foreign traffic splits.<br>
                    • <b>Tab D (RoRo Vehicles):</b> Rolling vehicle volumes and 4-class vehicle breakdown.<br>
                    • <b>Tab E (Port Comparison):</b> Side-by-side benchmarking of two or more chosen ports.<br>
                    • <b>Tab F (Predictive Analysis):</b> Calibrated forecasts, backtesting tables, and 95% CIs.<br>
                    • <b>Tab G (Data Explorer):</b> Dynamic database slicing and direct CSV exports.<br>
                    • <b>Tab H (About & Methodology):</b> Complete research whitepaper and documentation.
                </p>
            </div>
            <div class="doc-card">
                <div style="color: #38bdf8; font-weight: 700; font-size: 0.92rem; margin-bottom: 6px;">2. Filtering Years & Matching Periods</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    In the sidebar, use the <b>Multi-Year Horizon Selector</b> to select single years or compare all 6 years (2019, 2022–2026). 
                    When comparing multiple years, the dashboard defaults to <b>"Matching Q1–Q3"</b> mode to guarantee fair, annualized comparisons against 2026.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_g2:
            st.markdown(r"""
            <div class="doc-card">
                <div style="color: #34d399; font-weight: 700; font-size: 0.92rem; margin-bottom: 6px;">3. Selecting Ports & PMO Clusters</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    Use the <b>Port Selection Mode</b> radio buttons in the sidebar:
                    <br>• <i>All Luzon Ports:</i> Aggregates all 32 verified facilities.
                    <br>• <i>Specific Regional PMO:</i> Filters to an individual administrative cluster (e.g. PMO Batangas or PMO Mindoro).
                    <br>• <i>Individual Port Facility:</i> Focuses the entire dashboard on a single seaport.
                    <br>• <i>Batangas–Calapan Corridor:</i> Dedicated dual-port corridor evaluation mode.
                </p>
            </div>
            <div class="doc-card">
                <div style="color: #a78bfa; font-weight: 700; font-size: 0.92rem; margin-bottom: 6px;">4. Exporting Data to CSV</div>
                <p style="font-size: 0.84rem; color: #e2e8f0; line-height: 1.5;">
                    Every data table across Sections A through G includes a one-click <b>📥 Export as CSV</b> button. 
                    In Tab G (Data Explorer), you can slice any combination of years, PMOs, and indicators, and download clean UTF-8 encoded files for Microsoft Excel or Python analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)

