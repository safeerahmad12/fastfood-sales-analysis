import sys, os

# --- PATH FIX (DON'T TOUCH) ---
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from dashboard.utils import load_data, style_fig

# --- LOAD DATA ---
df = load_data()

# ===========================
# HEADER
# ===========================
st.markdown(
    """
    <h2>📊 Overview</h2>
    <p class="subtitle-text">
        Simple view of how the restaurant is doing: money, orders, and busy times.
    </p>
    """,
    unsafe_allow_html=True,
)

# ===========================
# TOP KPI CARDS
# ===========================
total_revenue = float(df["total_price"].sum())
total_orders = int(df["order_id"].nunique())
total_items = int(df["quantity"].sum())

order_level = (
    df.groupby("order_id")
    .agg(
        revenue=("total_price", "sum"),
        items=("quantity", "sum"),
    )
    .reset_index()
)
avg_order_value = float(order_level["revenue"].mean())
avg_items_per_order = float(order_level["items"].mean())

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"€{total_revenue:,.2f}")
col2.metric("🛒 Total Orders", f"{total_orders:,}")
col3.metric("🍟 Items Sold", f"{total_items:,}")
col4.metric("📦 Avg. Order Value", f"€{avg_order_value:,.2f}")

# Small explanation row
st.caption(
    "These cards answer: *How much money did we make? How many orders? "
    "How big is a typical order?*"
)

st.markdown("---")

# ===========================
# BUSIEST DAY / HOUR / CATEGORY SUMMARY
# ===========================
day_revenue = (
    df.groupby("day_name")["total_price"].sum().sort_values(ascending=False)
)
busiest_day = day_revenue.idxmax()

hour_revenue = (
    df.groupby("hour")["total_price"].sum().sort_values(ascending=False)
)
busiest_hour = int(hour_revenue.idxmax())

cat_revenue = (
    df.groupby("category")["total_price"].sum().sort_values(ascending=False)
)
top_category = cat_revenue.idxmax()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f"""
        <div class="glass-card">
            <h4>📅 Busiest Day</h4>
            <p style="font-size:1.4rem;margin:0;"><b>{busiest_day}</b></p>
            <p style="opacity:0.7;margin-top:0.2rem;">Highest total revenue.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="glass-card">
            <h4>⏰ Peak Hour</h4>
            <p style="font-size:1.4rem;margin:0;"><b>{busiest_hour}:00</b></p>
            <p style="opacity:0.7;margin-top:0.2rem;">Most money earned per hour.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="glass-card">
            <h4>🍔 Top Category</h4>
            <p style="font-size:1.4rem;margin:0;"><b>{top_category}</b></p>
            <p style="opacity:0.7;margin-top:0.2rem;">Category with highest revenue.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ===========================
# ROW 1: SALES BY HOUR + SALES BY DAY (BAR)
# ===========================
left, right = st.columns((1.3, 1))

# --- Revenue by hour of day ---
with left:
    st.markdown(
        '<div class="section-title">⏰ Revenue by hour of day</div>',
        unsafe_allow_html=True,
    )

    hourly = (
        df.groupby("hour")["total_price"]
        .sum()
        .reset_index()
        .sort_values("hour")
    )

    fig_hour = px.line(
        hourly,
        x="hour",
        y="total_price",
        markers=True,
        labels={"hour": "Hour", "total_price": "Revenue (€)"},
    )
    fig_hour = style_fig(fig_hour, "Daily revenue curve")
    st.plotly_chart(fig_hour, use_container_width=True)

    st.caption("This shows when the restaurant is most active during a normal day.")

# --- Revenue by day of week (bar) ---
with right:
    st.markdown(
        '<div class="section-title">📅 Revenue by day of week</div>',
        unsafe_allow_html=True,
    )

    day_order = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday",
    ]
    day_sales = (
        df.groupby("day_name")["total_price"]
        .sum()
        .reindex(day_order)
        .reset_index()
    )

    fig_day = px.bar(
        day_sales,
        x="day_name",
        y="total_price",
        labels={"day_name": "Day", "total_price": "Revenue (€)"},
    )
    fig_day = style_fig(fig_day, "Revenue by weekday")
    st.plotly_chart(fig_day, use_container_width=True)

    st.caption("Easy way to compare weekdays: which days are slow, which are strong.")

st.markdown("---")

# ===========================
# ROW 2: CATEGORY SHARE + SIMPLE ANIMATED VIEW
# ===========================
c_left, c_right = st.columns((1.1, 1.1))

# --- Category share donut ---
with c_left:
    st.markdown(
        '<div class="section-title">🍽️ Category revenue share</div>',
        unsafe_allow_html=True,
    )

    cat_revenue_df = (
        df.groupby("category")["total_price"]
        .sum()
        .reset_index()
        .sort_values("total_price", ascending=False)
    )

    fig_cat = px.pie(
        cat_revenue_df,
        names="category",
        values="total_price",
        hole=0.45,
    )
    fig_cat = style_fig(fig_cat, "Revenue share by category")
    st.plotly_chart(fig_cat, use_container_width=True)

    st.caption("Each slice shows how much money each category brings in.")

# --- SIMPLE ANIMATION: hour-by-hour growth of revenue ---
with c_right:
    st.markdown(
        '<div class="section-title">▶️ Animated: revenue building up over the day</div>',
        unsafe_allow_html=True,
    )

    # Use cumulative revenue so it feels like a "growing" line
    hourly_anim = hourly.copy()
    hourly_anim["cum_revenue"] = hourly_anim["total_price"].cumsum()

    fig_anim = px.bar(
        hourly_anim,
        x="hour",
        y="cum_revenue",
        animation_frame="hour",  # this gives us the play button
        range_y=[0, hourly_anim["cum_revenue"].max() * 1.1],
        labels={"hour": "Hour", "cum_revenue": "Cumulative revenue (€)"},
    )
    fig_anim = style_fig(fig_anim, "Cumulative revenue over the day")
    st.plotly_chart(fig_anim, use_container_width=True)

    st.caption("Press play ▶️ to watch how money adds up hour by hour.")

st.markdown("---")

# ===========================
# TEXT INSIGHTS (AUTO-GENERATED)
# ===========================
st.markdown(
    """
    <h4>🧠 Simple automatic insights</h4>
    """,
    unsafe_allow_html=True,
)

# Basic narrative in simple language
st.write(
    f"- **Most money** is earned on **{busiest_day}**, especially around **{busiest_hour}:00**."
)
st.write(
    f"- People usually buy about **{avg_items_per_order:.1f} items per order**."
)
st.write(
    f"- The category that brings the most revenue is **{top_category}**."
)
st.write(
    "- You can use this information to plan staff shifts, promotions and prep times."
)