import streamlit as st
import pandas as pd
import plotly.express as px


def show_dashboard():
    st.header("📊 Dataset Overview")

    try:
        # Load data (limit rows for performance)
        student_vle = pd.read_csv("data/raw/studentVle.csv", nrows=200000)
        student_info = pd.read_csv("data/raw/studentInfo.csv")
        vle = pd.read_csv("data/raw/vle.csv")
        student_assessment = pd.read_csv("data/raw/studentAssessment.csv")
        assessments = pd.read_csv("data/raw/assessments.csv")

        # -------------------------------
        # 🎯 TOP METRICS (CARDS STYLE)
        # -------------------------------
        st.markdown("### 🔑 Key Metrics")

        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Students", f"{student_vle['id_student'].nunique():,}")
        col2.metric("📚 Resources", f"{vle['id_site'].nunique():,}")
        col3.metric("🖱️ Interactions", f"{len(student_vle):,}")

        st.markdown("---")

        # -------------------------------
        # 📦 DATASET SIZES
        # -------------------------------
        st.subheader("📦 Dataset Sizes")

        col1, col2, col3 = st.columns(3)
        col1.metric("Student VLE", f"{student_vle.shape[0]:,}")
        col2.metric("Student Info", f"{student_info.shape[0]:,}")
        col3.metric("VLE", f"{vle.shape[0]:,}")

        col4, col5 = st.columns(2)
        col4.metric("Student Assessment", f"{student_assessment.shape[0]:,}")
        col5.metric("Assessments", f"{assessments.shape[0]:,}")

        st.markdown("---")

        # -------------------------------
        # 🧹 MISSING VALUES
        # -------------------------------
        st.subheader("🧹 Missing Values")

        datasets = {
            "student_vle": student_vle,
            "student_info": student_info,
            "vle": vle,
            "student_assessment": student_assessment,
            "assessments": assessments
        }

        missing_data = {
            name: df.isnull().sum().sum()
            for name, df in datasets.items()
        }

        fig = px.bar(
            x=list(missing_data.keys()),
            y=list(missing_data.values()),
            color=list(missing_data.values()),
            color_continuous_scale="tealgrn",
            title="Missing Values Across Datasets"
        )
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -------------------------------
        # 📚 ACTIVITY DISTRIBUTION
        # -------------------------------
        st.subheader("📚 Activity Type Distribution")

        activity_counts = vle["activity_type"].value_counts()

        fig = px.bar(
            activity_counts,
            x=activity_counts.index,
            y=activity_counts.values,
            color=activity_counts.values,
            color_continuous_scale="viridis"
        )
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------
        # 🎯 PERFORMANCE DISTRIBUTION
        # -------------------------------
        st.subheader("🎯 Student Performance")

        fig = px.pie(
            student_info,
            names="final_result",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -------------------------------
        # 🖱️ CLICK DISTRIBUTION
        # -------------------------------
        st.subheader("🖱️ Click Statistics")

        st.dataframe(student_vle["sum_click"].describe().to_frame())

        # -------------------------------
        # ⏳ TIMELINE
        # -------------------------------
        st.subheader("⏳ Interaction Timeline")

        timeline = student_vle["date"].value_counts().sort_index()

        fig = px.line(
            x=timeline.index,
            y=timeline.values,
            title="Student Activity Over Time"
        )
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -------------------------------
        # 🔍 ACTIVITY vs PERFORMANCE
        # -------------------------------
        st.subheader("🔍 Activity vs Performance")

        logs = student_vle.merge(vle, on="id_site", how="left")
        logs = logs.merge(student_info[["id_student", "final_result"]], on="id_student")

        activity_result = (
            logs.groupby(["activity_type", "final_result"])
            .size()
            .reset_index(name="count")
        )

        fig = px.bar(
            activity_result,
            x="activity_type",
            y="count",
            color="final_result",
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -------------------------------
        # 📝 ASSESSMENT SCORES
        # -------------------------------
        st.subheader("📝 Assessment Scores")

        st.dataframe(student_assessment["score"].describe().to_frame())

        fig = px.histogram(
            student_assessment,
            x="score",
            nbins=50,
            color_discrete_sequence=["#6366f1"]
        )
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -------------------------------
        # 🔎 SAMPLE DATA
        # -------------------------------
        st.subheader("🔎 Sample Data")

        st.dataframe(student_vle.head())

    except Exception as e:
        st.error("⚠️ Error loading data. Make sure dataset is present.")
        st.write(e)