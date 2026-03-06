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
    <h2>🍟 Category Analysis</h2>
    <p class="subtitle-text">
        Understand which menu categories drive revenue, volume and average order value.
    </p>
    """,
    unsafe_allow_html=True,
)

# Filter by order type (optional)
order_types = ["All"] + sorted(df["order_type"].unique().tolist())
selected_order_type = st.selectbox("Filter by order type", order_types)

df_cat = df.copy()
if selected_order_type != "All":
    df_cat = df_cat[df_cat["order_type"] == selected_order_type]

# Aggregations per category
cat_group = (
    df_cat
    .groupby("category")
    .agg(
        revenue=("total_price", "sum"),
        qty=("quantity", "sum"),
        avg_item_price=("price", "mean"),
        avg_order_revenue=("total_price", "mean"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

col1, col2 = st.columns((1.4, 1))

with col1:
    st.markdown(
        '<div class="section-title">Revenue by category</div>',
        unsafe_allow_html=True,
    )
    fig_cat_rev = px.bar(
        cat_group,
        x="category",
        y="revenue",
        labels={"category": "Category", "revenue": "Revenue (€)"},
    )
    fig_cat_rev = style_fig(fig_cat_rev, "Total Revenue by Category")
    st.plotly_chart(fig_cat_rev, use_container_width=True)

    st.markdown(
        '<div class="section-title">Item volume by category</div>',
        unsafe_allow_html=True,
    )
    fig_cat_qty = px.bar(
        cat_group,
        x="category",
        y="qty",
        labels={"category": "Category", "qty": "Items Sold"},
    )
    fig_cat_qty = style_fig(fig_cat_qty, "Items Sold by Category")
    st.plotly_chart(fig_cat_qty, use_container_width=True)

with col2:
    st.markdown(
        '<div class="section-title">Price vs demand</div>',
        unsafe_allow_html=True,
    )

    fig_scatter = px.scatter(
        cat_group,
        x="avg_item_price",
        y="revenue",
        size="qty",
        color="category",
        hover_data=["avg_order_revenue"],
        labels={
            "avg_item_price": "Average Item Price (€)",
            "revenue": "Revenue (€)",
        },
    )
    fig_scatter = style_fig(fig_scatter, "Category positioning: price vs revenue")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown(
        """
        <p class="subtitle-text">
            Bubble size = units sold. Categories in the top-right are both
            <strong>high price</strong> and <strong>high revenue</strong>.
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

st.markdown(
    """
    <div class="neon-card">
      <h3>📝 Interpretation tips</h3>
      <ul class="subtitle-text">
        <li><strong>High revenue + high volume</strong>: core categories to protect.</li>
        <li><strong>High revenue + low volume</strong>: premium categories where price matters.</li>
        <li><strong>Low revenue + high volume</strong>: candidates for upselling or price review.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)