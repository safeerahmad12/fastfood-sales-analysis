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
    <h2>👥 Employee Performance</h2>
    <p class="subtitle-text">
        Compare employees by revenue, number of orders and average order value.
    </p>
    """,
    unsafe_allow_html=True,
)

# Aggregate per employee
emp_group = (
    df.groupby(["employee_id", "employee_name"])
    .agg(
        revenue=("total_price", "sum"),
        orders=("order_id", "nunique"),
        items=("quantity", "sum"),
        avg_order_value=("total_price", "mean"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

top_n = st.slider("Show top N employees by revenue", 3, 20, 10)
emp_top = emp_group.head(top_n)

col1, col2 = st.columns((1.5, 1))

with col1:
    st.markdown(
        '<div class="section-title">Revenue by employee</div>',
        unsafe_allow_html=True,
    )
    fig_emp_rev = px.bar(
        emp_top,
        x="employee_name",
        y="revenue",
        hover_data=["orders", "items", "avg_order_value"],
        labels={"employee_name": "Employee", "revenue": "Revenue (€)"},
    )
    fig_emp_rev = style_fig(fig_emp_rev, f"Top {top_n} employees by revenue")
    st.plotly_chart(fig_emp_rev, use_container_width=True)

with col2:
    st.markdown(
        '<div class="section-title">Efficiency view</div>',
        unsafe_allow_html=True,
    )
    fig_emp_eff = px.scatter(
        emp_top,
        x="orders",
        y="avg_order_value",
        size="revenue",
        color="employee_name",
        labels={
            "orders": "Orders handled",
            "avg_order_value": "Avg. order value (€)",
        },
    )
    fig_emp_eff = style_fig(fig_emp_eff, "Orders vs Avg Order Value")
    st.plotly_chart(fig_emp_eff, use_container_width=True)

st.markdown("---")

st.markdown(
    """
    <div class="neon-card">
      <h3>🔍 How to read this</h3>
      <ul class="subtitle-text">
        <li>Bar chart: who contributes most to total revenue.</li>
        <li>Bubble chart: right side = many orders, top = higher order value.</li>
        <li>Large bubble = employee who combines volume and value.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)