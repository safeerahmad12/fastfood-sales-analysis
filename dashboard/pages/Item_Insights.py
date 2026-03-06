import sys, os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils import load_data, style_fig

df = load_data()

st.markdown(
    """
    <h2>🍔 Item Insights</h2>
    <p class="subtitle-text">
        Deep dive into bestselling items, pricing and revenue contribution.
    </p>
    """,
    unsafe_allow_html=True,
)

# Top N selector
top_n_items = st.slider("Show top N items by revenue", 5, 30, 15)

item_group = (
    df.groupby(["product_name", "category"])
    .agg(
        revenue=("total_price", "sum"),
        qty=("quantity", "sum"),
        avg_price=("price", "mean"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

top_items = item_group.head(top_n_items)

col1, col2 = st.columns((1.4, 1.1))

with col1:
    st.markdown(
        '<div class="section-title">Top items by revenue</div>',
        unsafe_allow_html=True,
    )
    fig_item_rev = px.bar(
        top_items,
        x="revenue",
        y="product_name",
        orientation="h",
        color="category",
        labels={
            "revenue": "Revenue (€)",
            "product_name": "Item",
            "category": "Category",
        },
    )
    fig_item_rev = style_fig(fig_item_rev, f"Top {top_n_items} items")
    st.plotly_chart(fig_item_rev, use_container_width=True)

with col2:
    st.markdown(
        '<div class="section-title">Price vs volume</div>',
        unsafe_allow_html=True,
    )
    fig_price_qty = px.scatter(
        top_items,
        x="avg_price",
        y="qty",
        size="revenue",
        color="category",
        hover_name="product_name",
        labels={
            "avg_price": "Average Item Price (€)",
            "qty": "Units sold",
        },
    )
    fig_price_qty = style_fig(fig_price_qty, "Price vs Volume (top items)")
    st.plotly_chart(fig_price_qty, use_container_width=True)

st.markdown("---")

# Optional: small detailed table
with st.expander("🔍 Show detailed item table"):
    st.dataframe(
        top_items.sort_values("revenue", ascending=False),
        use_container_width=True,
        hide_index=True,
    )