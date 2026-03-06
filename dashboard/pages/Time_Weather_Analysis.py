import sys, os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from dashboard.utils import load_data, style_fig

df = load_data()

st.markdown(
    """
    <h2>⏱️ Time & Weather Analysis</h2>
    <p class="subtitle-text">
        Explore how time-of-day and weather conditions influence revenue.
    </p>
    """,
    unsafe_allow_html=True,
)

# Weather filter
weather_options = ["All"] + sorted(df["weather"].unique().tolist())
selected_weather = st.selectbox("Filter by weather type", weather_options)

df_tw = df.copy()
if selected_weather != "All":
    df_tw = df_tw[df_tw["weather"] == selected_weather]

col1, col2 = st.columns((1.4, 1.2))

# Revenue by hour (for chosen weather)
with col1:
    st.markdown(
        '<div class="section-title">Revenue by hour</div>',
        unsafe_allow_html=True,
    )

    hourly = (
        df_tw.groupby("hour")["total_price"]
        .sum()
        .reset_index()
        .sort_values("hour")
    )
    fig_hour = px.line(
        hourly,
        x="hour",
        y="total_price",
        markers=True,
        labels={"hour": "Hour of Day", "total_price": "Revenue (€)"},
    )
    title_suffix = (
        f" ({selected_weather})" if selected_weather != "All" else " (all weather)"
    )
    fig_hour = style_fig(fig_hour, f"Revenue by Hour{title_suffix}")
    st.plotly_chart(fig_hour, use_container_width=True)

# Temperature vs revenue (scatter + manual regression line)
with col2:
    st.markdown(
        '<div class="section-title">Temperature vs average order revenue</div>',
        unsafe_allow_html=True,
    )

    order_level = (
        df_tw.groupby("order_id")
        .agg(
            revenue=("total_price", "sum"),
            temp=("temperature_c", "median"),
        )
        .reset_index()
        .dropna()
    )

    fig_temp = px.scatter(
        order_level,
        x="temp",
        y="revenue",
        labels={
            "temp": "Temperature (°C)",
            "revenue": "Order revenue (€)",
        },
    )

    # Manual linear regression line
    if len(order_level) > 5:
        x_vals = order_level["temp"].values
        y_vals = order_level["revenue"].values
        coef = np.polyfit(x_vals, y_vals, 1)
        x_line = np.linspace(x_vals.min(), x_vals.max(), 50)
        y_line = coef[0] * x_line + coef[1]
        fig_temp.add_traces(
            px.line(
                x=x_line,
                y=y_line,
            ).data
        )

    fig_temp = style_fig(fig_temp, "Effect of temperature on order revenue")
    st.plotly_chart(fig_temp, use_container_width=True)

st.markdown("---")

# Heatmap: day vs hour
st.markdown(
    '<div class="section-title">Heatmap: Day-of-week × Hour</div>',
    unsafe_allow_html=True,
)

pivot = (
    df_tw.pivot_table(
        index="day_name",
        columns="hour",
        values="total_price",
        aggfunc="sum",
    )
)

day_order = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]
pivot = pivot.reindex(day_order)

fig_heat = px.imshow(
    pivot,
    aspect="auto",
    labels={"x": "Hour of Day", "y": "Day of Week", "color": "Revenue (€)"},
)
fig_heat = style_fig(fig_heat, "Revenue heatmap (Day × Hour)")
st.plotly_chart(fig_heat, use_container_width=True)