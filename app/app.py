import streamlit as st

# ── MUST be the very first Streamlit call ─────────────────────────────────────
st.set_page_config(
    page_title="LMS Performance Prediction",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.dashboard import show_dashboard
from components.patterns import show_patterns
from components.prediction import show_prediction

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding:10px 0 24px 0">
    <div style="font-size:1.15rem;font-weight:700;color:#e2e8f0;display:flex;align-items:center;gap:8px">
        <span>📡</span> LMS Analytics
    </div>
    <div style="font-size:0.7rem;color:#475569;margin-top:3px;letter-spacing:.5px">
        OULAD · Performance Prediction
    </div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "🔍 Patterns", "🤖 Prediction"],
    label_visibility="collapsed",
)

# ── Route ─────────────────────────────────────────────────────────────────────
if menu == "📊 Dashboard":
    show_dashboard()
elif menu == "🔍 Patterns":
    show_patterns()
elif menu == "🤖 Prediction":
    show_prediction()