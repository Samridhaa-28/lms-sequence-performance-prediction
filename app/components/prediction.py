import streamlit as st


def show_prediction():
    st.header("🤖 Performance Prediction")

    st.markdown("Input student behavior features to predict performance")

    clicks = st.slider("Total Clicks", 0, 1000, 100)
    quiz_attempts = st.slider("Quiz Attempts", 0, 50, 5)

    if st.button("Predict"):
        st.success("Prediction: PASS (demo placeholder)")