import sys, os

# --- PATH FIX ---
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error

from dashboard.utils import load_data, style_fig

# ----------------------------------------
# LOAD DATA
# ----------------------------------------
df = load_data()

st.markdown(
    """
    <h2>🔮 Predictive Analytics & Intelligence</h2>
    <p class="subtitle-text">
        Here we use machine learning to predict order revenue and discover simple customer groups.
        Everything is explained in easy language.
    </p>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------
# PREPARE ORDER-LEVEL DATA
# ----------------------------------------
order_level = (
    df.groupby("order_id")
    .agg(
        revenue=("total_price", "sum"),
        items=("quantity", "sum"),
        avg_item_price=("total_price", lambda x: x.sum() / max(x.count(), 1)),
        hour=("hour", "median"),
        temp=("temperature_c", "median"),
        order_type=("order_type", lambda x: x.iloc[0]),
        payment_method=("payment_method", lambda x: x.iloc[0]),
        day_name=("day_name", lambda x: x.iloc[0]),
    )
    .reset_index()
)

# Small safety check
order_level = order_level.dropna(subset=["revenue", "items", "hour", "temp"])

# Extra features
order_level["items_per_order"] = order_level["items"]
order_level["order_type_code"] = order_level["order_type"].astype("category").cat.codes

# ----------------------------------------
# 1. REVENUE PREDICTION MODEL
# ----------------------------------------
@st.cache_data
def train_revenue_model(order_df: pd.DataFrame):
    feature_cols = [
        "hour",
        "temp",
        "items_per_order",
        "avg_item_price",
        "order_type_code",
    ]

    X = order_df[feature_cols].copy()
    y = order_df["revenue"].copy()

    # Safety: drop any NaNs
    mask = X.notna().all(axis=1) & y.notna()
    X = X[mask]
    y = y[mask]

    model = RandomForestRegressor(
        n_estimators=120,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X, y)

    # Evaluate on the same data (for simplicity here)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    mape = mean_absolute_percentage_error(y, y_pred) * 100

    return model, feature_cols, {"r2": r2, "mae": mae, "mape": mape}


revenue_model, feature_cols, metrics = train_revenue_model(order_level)

# ----------------------------------------
# 2. CLUSTERING MODEL (KMeans)
# ----------------------------------------
@st.cache_data
def train_kmeans(order_df: pd.DataFrame, n_clusters: int = 3):
    cluster_features = ["revenue", "items_per_order", "temp", "hour"]

    X = order_df[cluster_features].copy().dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    result = order_df.loc[X.index].copy()
    result["cluster"] = labels

    return kmeans, scaler, result


# UI: choose number of clusters
st.markdown("### 💰 1) Revenue prediction (RandomForest)")
st.caption(
    "We train a model that tries to guess the total revenue of one order, "
    "using hour, temperature, number of items and order type."
)

# KPIs for model quality
c1, c2, c3 = st.columns(3)
c1.metric("📈 R² score", f"{metrics['r2']:.2f}")
c2.metric("📉 MAE (€, avg error)", f"{metrics['mae']:.2f}")
c3.metric("📊 MAPE (% error)", f"{metrics['mape']:.1f}%")

st.caption(
    "R² close to 1.0 means a very good model. MAE/MAPE show how far the model is off on average."
)

st.markdown("---")

# ----------------------------------------
# WHAT-IF PLAYGROUND FOR PREDICTION
# ----------------------------------------
st.markdown("#### 🧪 Try your own scenario")

col_left, col_right = st.columns(2)

with col_left:
    hour_input = st.slider("Hour of day", min_value=0, max_value=23, value=12)
    temp_input = st.slider("Outside temperature (°C)", min_value=-5, max_value=40, value=20)
    items_input = st.slider("Number of items in order", min_value=1, max_value=10, value=3)
    avg_price_input = st.slider("Average price per item (€)", min_value=1.0, max_value=15.0, value=5.0, step=0.5)

with col_right:
    order_type_options = sorted(order_level["order_type"].unique().tolist())
    payment_options = sorted(order_level["payment_method"].unique().tolist())
    day_options = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]

    order_type_input = st.selectbox("Order type", order_type_options)
    payment_input = st.selectbox("Payment method", payment_options)
    day_input = st.selectbox("Day of week", day_options)

# Convert order_type to the same numeric code system
order_type_cat = order_level["order_type"].astype("category")
order_type_mapping = dict(enumerate(order_type_cat.cat.categories))
reverse_mapping = {v: k for k, v in order_type_mapping.items()}
order_type_code_input = reverse_mapping.get(order_type_input, 0)

# Build single-row input
input_df = pd.DataFrame(
    {
        "hour": [hour_input],
        "temp": [temp_input],
        "items_per_order": [items_input],
        "avg_item_price": [avg_price_input],
        "order_type_code": [order_type_code_input],
    }
)

pred_revenue = float(revenue_model.predict(input_df)[0])

# Display result in a glass card
st.markdown(
    f"""
    <div class="glass-card" style="margin-top:0.5rem;">
        <h4>🔮 Predicted order revenue</h4>
        <p style="font-size:2rem;margin:0;"><b>€{pred_revenue:,.2f}</b></p>
        <p style="opacity:0.8;margin-top:0.3rem;">
            Example: On a <b>{day_input}</b> at <b>{hour_input}:00</b>,
            with <b>{items_input}</b> items (~€{avg_price_input:.2f} each),
            the model expects the order to be about <b>€{pred_revenue:,.2f}</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ----------------------------------------
# REAL vs PREDICTED PLOT
# ----------------------------------------
st.markdown("#### 📉 Real vs predicted revenue (sample of orders)")

sample = order_level.sample(n=min(700, len(order_level)), random_state=42).copy()
X_sample = sample[feature_cols]
y_sample = sample["revenue"]
y_pred_sample = revenue_model.predict(X_sample)

scatter_df = pd.DataFrame(
    {
        "Real revenue": y_sample,
        "Predicted revenue": y_pred_sample,
    }
)

fig_scatter = px.scatter(
    scatter_df,
    x="Real revenue",
    y="Predicted revenue",
    labels={"Real revenue": "Real revenue (€)", "Predicted revenue": "Predicted revenue (€)"},
)
fig_scatter.add_shape(
    type="line",
    x0=scatter_df["Real revenue"].min(),
    y0=scatter_df["Real revenue"].min(),
    x1=scatter_df["Real revenue"].max(),
    y1=scatter_df["Real revenue"].max(),
    line=dict(dash="dash")
)
fig_scatter = style_fig(fig_scatter, "How well does the model follow the diagonal line?")
st.plotly_chart(fig_scatter, use_container_width=True)

st.caption("If points are close to the dashed line, the model is doing a good job.")

st.markdown("---")

# ----------------------------------------
# 2) CLUSTERING – SIMPLE CUSTOMER GROUPS
# ----------------------------------------
st.markdown("### 🧩 2) Order & customer segmentation (KMeans)")

n_clusters = st.slider("Number of groups (clusters)", min_value=2, max_value=6, value=3)
kmeans, scaler, clustered_orders = train_kmeans(order_level, n_clusters)

# Short summary table
cluster_summary = (
    clustered_orders.groupby("cluster")
    .agg(
        avg_revenue=("revenue", "mean"),
        avg_items=("items_per_order", "mean"),
        avg_hour=("hour", "mean"),
    )
    .reset_index()
    .sort_values("avg_revenue", ascending=False)
)

st.write("**Cluster summary (simple stats):**")
st.dataframe(
    cluster_summary.style.format(
        {
            "avg_revenue": "€{:.2f}",
            "avg_items": "{:.1f}",
            "avg_hour": "{:.1f}",
        }
    ),
    use_container_width=True,
)

# Simple text interpretation for each cluster
st.markdown("#### 🗣️ How to read these groups (in easy words)")

for _, row in cluster_summary.iterrows():
    cid = int(row["cluster"])
    rev = row["avg_revenue"]
    items_c = row["avg_items"]
    hour_c = row["avg_hour"]

    if rev >= cluster_summary["avg_revenue"].max() * 0.8:
        kind = "💎 High spenders"
    elif rev <= cluster_summary["avg_revenue"].min() * 1.2:
        kind = "🧊 Low spend snackers"
    else:
        kind = "😊 Normal customers"

    st.write(
        f"- **Cluster {cid}** → {kind}: on average **€{rev:.2f} per order**, "
        f"~**{items_c:.1f} items**, around **{hour_c:.0f}:00**."
    )

st.markdown("---")

# ----------------------------------------
# CLUSTER VISUALIZATION
# ----------------------------------------
st.markdown("#### 🎨 Visualizing clusters")

viz_choice = st.radio(
    "What do you want to see?",
    ["Items vs revenue", "Hour vs revenue"],
    horizontal=True,
)

if viz_choice == "Items vs revenue":
    fig_clusters = px.scatter(
        clustered_orders,
        x="items_per_order",
        y="revenue",
        color="cluster",
        labels={"items_per_order": "Items per order", "revenue": "Revenue (€)"},
    )
    fig_clusters = style_fig(fig_clusters, "Clusters by items and revenue")
else:
    fig_clusters = px.scatter(
        clustered_orders,
        x="hour",
        y="revenue",
        color="cluster",
        labels={"hour": "Hour of day", "revenue": "Revenue (€)"},
    )
    fig_clusters = style_fig(fig_clusters, "Clusters by hour and revenue")

st.plotly_chart(fig_clusters, use_container_width=True)

st.caption(
    "Each color is one group (cluster). This helps the manager see which types of orders exist."
)