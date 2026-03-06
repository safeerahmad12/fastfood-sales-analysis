import sys, os
import os
import streamlit as st
st.success("THIS IS THE CORRECT APP.PY ✔️")

st.write("Loaded file:", os.path.abspath(__file__))
# Make sure Python can see the dashboard folder
CURRENT_DIR = os.path.dirname(__file__)
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

import streamlit as st
from utils import load_data 

# ==========================================================
# 🔥 GLOBAL PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Fast Food AI Dashboard",
    page_icon="🍔",
    layout="wide"
)

# ==========================================================
# 🔥 GLOBAL NEON GLASS THEME
# ==========================================================
st.markdown("""
<style>

:root {
    --bg1: #0b0e16;
    --bg2: #131826;
    --card-bg: rgba(255,255,255,0.10);
    --border: rgba(255,255,255,0.20);
    --text: #e7e7e7;
    --accent: #77f6ff;
}

/* APP BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #1b2238, #0b0e16 60%);
    color: var(--text);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: rgba(22,22,22,0.55);
    backdrop-filter: blur(18px);
    border-right: 1px solid var(--border);
}

/* TITLE */
.page-title {
    font-size: 50px;
    font-weight: 900;
    padding-top: 0.3rem;
    color: var(--accent);
    text-shadow: 0px 0px 15px rgba(119, 246, 255, 0.8);
    margin-bottom: 0.5rem;
}

/* SUBTITLE */
.subtitle {
    font-size: 19px;
    opacity: 0.88;
    max-width: 900px;
    line-height: 1.45;
}

/* GLASS CARD */
.info-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 26px;
    margin-top: 22px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.45);
}

/* CARD TITLE */
.card-title {
    font-size: 28px;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 15px;
    text-shadow: 0 0 12px rgba(119, 246, 255, 0.5);
}

/* LIST TEXT */
li {
    font-size: 17px;
    margin-bottom: 6px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# 🔥 LOAD DATA
# ==========================================================
df = load_data()

# ==========================================================
# 🔥 HEADER SECTION
# ==========================================================
st.markdown("<div class='page-title'>Fast Food AI Sales Dashboard</div>", unsafe_allow_html=True)

st.markdown("""
<p class='subtitle'>
A visually enhanced Bachelor-level project dashboard built using a synthetic fast-food POS dataset.
Explore KPIs, category insights, employee performance, bestselling items, weather impact analysis,
and advanced ML-driven predictions — all inside a modern neon-glass interface.
</p>
""", unsafe_allow_html=True)

# ==========================================================
# 🔥 PROJECT SCOPE + TECH STACK
# ==========================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>📘 Project Scope</div>", unsafe_allow_html=True)
    st.markdown("""
- Data cleaning + feature engineering  
- Multi-page interactive dashboard  
- Trend exploration (time, category, item, employee)  
- Predictive modelling (RandomForest, KMeans)  
- Context analysis: weather & time-of-day  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🧠 Tech Stack</div>", unsafe_allow_html=True)
    st.markdown("""
- **Python** · pandas · numpy  
- **Plotly** interactive visuals  
- **Streamlit multipage app**  
- **scikit-learn** ML (RandomForest, KMeans)  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# 🔥 HOW TO USE THE APP
# ==========================================================
st.markdown("<div class='info-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>✅ How to Use This App</div>", unsafe_allow_html=True)

st.markdown("""
1. **Overview** – high-level KPIs & time trends  
2. **Category Analysis** – revenue by category  
3. **Employee Performance** – staff revenue distribution  
4. **Item Insights** – bestseller & pricing patterns  
5. **Predictive Analytics** – ML revenue prediction & segmentation  
6. **Time & Weather** – how external conditions influence revenue  
""")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# 🔥 KPI CARDS
# ==========================================================
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("### 💰 Total Revenue")
    st.subheader(f"€{df['total_price'].sum():,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with k2:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("### 🧾 Total Orders")
    st.subheader(f"{df['order_id'].nunique():,}")
    st.markdown("</div>", unsafe_allow_html=True)

with k3:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("### 🍟 Items Sold")
    st.subheader(f"{df['quantity'].sum():,}")
    st.markdown("</div>", unsafe_allow_html=True)