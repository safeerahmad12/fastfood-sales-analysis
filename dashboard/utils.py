import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/fast_food_dataset_cleaned.csv")

    df.columns = df.columns.str.strip()

    # Map your real dataset columns to the names used in dashboard pages
    if "day_name" not in df.columns and "weekday" in df.columns:
        df["day_name"] = df["weekday"]

    if "category" not in df.columns and "menu_category" in df.columns:
        df["category"] = df["menu_category"]

    if "item_name" not in df.columns and "menu_item" in df.columns:
        df["item_name"] = df["menu_item"]

    if "product_name" not in df.columns and "menu_item" in df.columns:
        df["product_name"] = df["menu_item"]

    return df


def style_fig(fig, title=""):
    fig.update_layout(
        title=title,
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        title_x=0.02
    )
    return fig