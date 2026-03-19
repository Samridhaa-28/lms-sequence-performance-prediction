import streamlit as st
import pandas as pd


def show_patterns():
    st.header("🔍 Sequential Patterns")

    try:
        patterns = pd.read_csv("../results/patterns.csv")

        st.subheader("Top Patterns")
        st.dataframe(patterns.head(20))

    except:
        st.info("Patterns will be available after pattern mining (Day 6)")