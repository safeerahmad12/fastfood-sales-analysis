import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# DATA LOADER
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/fast_food_dataset_cleaned.csv")

    # order_time is already a full datetime string
    df["timestamp"] = pd.to_datetime(df["order_time"])

    # Derived features
    df["hour"] = df["timestamp"].dt.hour
    df["day_name"] = df["timestamp"].dt.day_name()
    df["weekday"] = df["timestamp"].dt.weekday

    # Rename for dashboard consistency
    df.rename(
        columns={
            "menu_category": "category",
            "menu_item": "product_name",
        },
        inplace=True,
    )

    return df


# -------------------------------------------------
# GLOBAL NEON CYBER THEME (CSS)
# -------------------------------------------------
def inject_neon_theme():
    st.markdown(
        """
        <style>
        /* MAIN BACKGROUND */
        .stApp {
            background: radial-gradient(circle at top left, #0f172a 0, #020617 45%, #000000 100%);
            color: #e5e7eb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
        }

        /* Center the main container a bit */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15,23,42,0.95), rgba(8,47,73,0.9));
            border-right: 1px solid rgba(148,163,184,0.3);
        }

        section[data-testid="stSidebar"] .stMarkdown p {
            font-size: 0.9rem;
            color: #cbd5f5;
        }

        /* HEADERS */
        h1, h2, h3, h4 {
            font-weight: 700;
            letter-spacing: 0.03em;
        }

        /* Subtle text */
        .subtitle-text {
            font-size: 0.9rem;
            color: #9ca3af;
        }

        /* METRIC CARDS */
        div[data-testid="metric-container"] {
            background: radial-gradient(circle at top left, rgba(56,189,248,0.15), rgba(15,23,42,0.95));
            border-radius: 14px;
            border: 1px solid rgba(56,189,248,0.35);
            padding: 0.75rem 1rem;
            box-shadow:
                0 0 25px rgba(56,189,248,0.18),
                0 18px 35px rgba(15,23,42,0.95);
        }
        div[data-testid="metric-container"] > label {
            color: #e5e7eb !important;
            font-size: 0.85rem;
        }
        div[data-testid="metric-container"] > div {
            color: #f9fafb !important;
            font-weight: 600;
        }

        /* "Cards" for plots */
        .neon-card {
            background: radial-gradient(circle at top left, rgba(168,85,247,0.12), rgba(15,23,42,0.96));
            border-radius: 18px;
            border: 1px solid rgba(129,140,248,0.4);
            padding: 1.1rem 1.2rem 1.3rem 1.2rem;
            margin-bottom: 1.3rem;
            box-shadow:
                0 0 22px rgba(129,140,248,0.25),
                0 18px 45px rgba(15,23,42,1);
        }

        .neon-card h3 {
            margin-bottom: 0.5rem;
        }

        /* Plotly charts: remove white background */
        .stPlotlyChart {
            background-color: transparent;
        }

        /* Buttons / sliders */
        .stSlider > div > div > div {
            color: #e5e7eb !important;
        }

        .stButton>button {
            border-radius: 999px;
            border: 1px solid rgba(94,234,212,0.6);
            background: radial-gradient(circle at top left, rgba(34,211,238,0.25), rgba(15,23,42,1));
            color: #e5e7eb;
            padding: 0.5rem 1.2rem;
            font-weight: 500;
        }
        .stButton>button:hover {
            border-color: rgba(94,234,212,0.9);
            box-shadow: 0 0 18px rgba(34,211,238,0.45);
        }

        /* Select boxes */
        .stSelectbox label {
            font-size: 0.85rem;
            color: #e5e7eb;
        }

        /* Section title small bar */
        .section-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #f9fafb;
            margin-bottom: 0.4rem;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }
        .section-title::before {
            content: "";
            display: inline-block;
            width: 7px;
            height: 18px;
            border-radius: 999px;
            background: linear-gradient(180deg, #22d3ee, #a855f7);
        }

        /* Make tables slightly glassy */
        .stDataFrame, .stTable {
            background: rgba(15,23,42,0.9);
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Plotly default style
    px.defaults.template = "plotly_dark"
    px.defaults.color_discrete_sequence = [
        "#22d3ee", "#a855f7", "#f97316", "#4ade80", "#eab308"
    ]


# -------------------------------------------------
# PLOT HELPERS
# -------------------------------------------------
def style_fig(fig, title: str | None = None):
    fig.update_layout(
        paper_bgcolor="rgba(15,23,42,0)",
        plot_bgcolor="rgba(15,23,42,0.8)",
        font=dict(family="Inter, system-ui, sans-serif", color="#e5e7eb"),
        margin=dict(t=60 if title else 30, r=30, b=40, l=55),
        hoverlabel=dict(
            bgcolor="rgba(15,23,42,0.95)",
            bordercolor="#22d3ee",
            font=dict(color="#e5e7eb"),
        ),
    )
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                x=0.02,
                xanchor="left",
                font=dict(size=18, color="#f9fafb"),
            )
        )
    return fig