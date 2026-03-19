import streamlit as st

from components.dashboard import show_dashboard
from components.patterns import show_patterns
from components.prediction import show_prediction

st.markdown("""
<style>
    .main {
        background-color: #0f172a;
    }
    h1, h2, h3 {
        color: #e2e8f0;
    }
    .stMetric {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 15px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="LMS Performance Prediction",
    layout="wide"
)

# Sidebar
st.sidebar.title("📊 Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Patterns", "Prediction"]
)

# Header
st.title("🎓 LMS Student Performance Analysis")
st.markdown("Analyze student behavior and predict performance using LMS interaction data")

# Routing
if menu == "Dashboard":
    show_dashboard()

elif menu == "Patterns":
    show_patterns()

elif menu == "Prediction":
    show_prediction()