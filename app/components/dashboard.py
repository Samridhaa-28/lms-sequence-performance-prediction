import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ─── COLOUR PALETTE ───────────────────────────────────────────────────────────
PASS_COLOR = "#22d3ee"
FAIL_COLOR = "#f87171"
DIST_COLOR = "#a78bfa"
WITH_COLOR = "#94a3b8"

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'Space Grotesk', sans-serif", color="#cbd5e1"),
    margin=dict(l=20, r=20, t=45, b=20),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)"),
)


# ─── CSS ──────────────────────────────────────────────────────────────────────
def _inject_css():
    st.markdown(
        """
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
.stApp { background: #020617; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
h1 {
    font-size: 2rem !important; font-weight: 700 !important;
    background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
}
[data-testid="stSidebar"] .stRadio > div > label {
    color: #cbd5e1 !important; font-size: 0.88rem !important;
    padding: 7px 12px !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(99,102,241,0.15) !important; color: #e2e8f0 !important;
}
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,41,59,0.7)) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 14px !important; padding: 18px !important;
    transition: border-color 0.2s, transform 0.2s;
}
div[data-testid="metric-container"]:hover {
    border-color: rgba(99,102,241,0.5) !important;
    transform: translateY(-2px);
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.65rem !important; font-weight: 600 !important;
    color: #475569 !important; text-transform: uppercase; letter-spacing: 1.8px;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.9rem !important; font-weight: 700 !important;
    color: #e2e8f0 !important; font-family: 'JetBrains Mono', monospace !important;
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.35), transparent);
    margin: 2rem 0;
}
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1.1rem; padding-bottom: 10px;
    border-bottom: 1px solid rgba(99,102,241,0.12);
}
.section-icon {
    width: 34px; height: 34px; border-radius: 9px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    display: flex; align-items: center; justify-content: center; font-size: 0.9rem;
}
.section-title { font-size: 1rem; font-weight: 600; color: #e2e8f0; margin: 0; }
.info-badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.6px;
    text-transform: uppercase; margin-right: 5px;
}
.badge-pass      { background: rgba(34,211,238,0.12);  color: #22d3ee; border: 1px solid rgba(34,211,238,0.28); }
.badge-fail      { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.28); }
.badge-dist      { background: rgba(167,139,250,0.12); color: #a78bfa; border: 1px solid rgba(167,139,250,0.28); }
.badge-withdrawn { background: rgba(148,163,184,0.12); color: #94a3b8; border: 1px solid rgba(148,163,184,0.28); }
.stat-pill {
    background: rgba(30,41,59,0.6); border: 1px solid rgba(99,102,241,0.13);
    border-radius: 11px; padding: 12px 16px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #64748b;
}
.stat-pill span { color: #e2e8f0; font-weight: 600; font-size: 0.98rem; display: block; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""",
        unsafe_allow_html=True,
    )


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def _section(icon: str, title: str):
    st.markdown(
        f"""<div class="section-header">
               <div class="section-icon">{icon}</div>
               <p class="section-title">{title}</p>
             </div>""",
        unsafe_allow_html=True,
    )


def _divider():
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def show_dashboard():
    _inject_css()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """<div style="padding:6px 0 22px 0">
               <h1>📡 LMS Analytics Dashboard</h1>
               <p style="color:#475569;font-size:0.82rem;margin-top:-4px">
                   Open University Learning Analytics · OULAD Dataset
               </p>
           </div>""",
        unsafe_allow_html=True,
    )

    try:
        # ── Load ──────────────────────────────────────────────────────────────
        with st.spinner("Loading datasets…"):
            student_vle        = pd.read_csv("data/raw/studentVle.csv", nrows=200_000)
            student_info       = pd.read_csv("data/raw/studentInfo.csv")
            vle                = pd.read_csv("data/raw/vle.csv")
            student_assessment = pd.read_csv("data/raw/studentAssessment.csv")
            assessments        = pd.read_csv("data/raw/assessments.csv")

        # ── KPI row ───────────────────────────────────────────────────────────
        _section("📊", "Key Metrics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Students",     f"{student_info['id_student'].nunique():,}")
        c2.metric("Learning Resources", f"{vle['id_site'].nunique():,}")
        c3.metric("VLE Interactions",   f"{len(student_vle):,}+")
        c4.metric("Assessments",        f"{len(assessments):,}")

        _divider()

        # ── Performance ───────────────────────────────────────────────────────
        _section("🎯", "Student Performance Distribution")

        result_counts = student_info["final_result"].value_counts().reset_index()
        result_counts.columns = ["Result", "Count"]
        color_map = {
            "Pass": PASS_COLOR, "Fail": FAIL_COLOR,
            "Distinction": DIST_COLOR, "Withdrawn": WITH_COLOR,
        }

        col_l, col_r = st.columns([3, 2])

        with col_l:
            fig_bar = px.bar(
                result_counts, x="Result", y="Count",
                color="Result", color_discrete_map=color_map, text="Count",
            )
            fig_bar.update_traces(
                texttemplate="%{text:,}", textposition="outside",
                marker_line_width=0, width=0.55,
            )
            fig_bar.update_layout(
                **CHART_THEME, title="Count by Outcome",
                showlegend=False, yaxis_title="", xaxis_title="",
            )
            fig_bar.update_yaxes(showticklabels=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_r:
            fig_pie = px.pie(
                result_counts, names="Result", values="Count",
                color="Result", color_discrete_map=color_map, hole=0.55,
            )
            fig_pie.update_traces(
                textinfo="percent+label", textfont_size=11,
                pull=[0.03] * len(result_counts),
                marker=dict(line=dict(color="#020617", width=2)),
            )
            fig_pie.update_layout(
                **CHART_THEME, title="Share by Outcome", showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # badges
        rc    = dict(zip(result_counts["Result"], result_counts["Count"]))
        total = result_counts["Count"].sum()
        badges = [
            ("badge-pass",      "Pass",        rc.get("Pass", 0)),
            ("badge-dist",      "Distinction", rc.get("Distinction", 0)),
            ("badge-fail",      "Fail",        rc.get("Fail", 0)),
            ("badge-withdrawn", "Withdrawn",   rc.get("Withdrawn", 0)),
        ]
        badge_html = "".join(
            f'<span class="info-badge {cls}">{lbl}&nbsp;{cnt:,} ({cnt/total*100:.1f}%)</span>'
            for cls, lbl, cnt in badges
        )
        st.markdown(
            f'<div style="margin-top:-8px;margin-bottom:6px">{badge_html}</div>',
            unsafe_allow_html=True,
        )

        _divider()

        # ── Activity types ────────────────────────────────────────────────────
        _section("📚", "Learning Resource Types")
        activity_counts = vle["activity_type"].value_counts().reset_index()
        activity_counts.columns = ["Activity", "Count"]

        fig_act = px.bar(
            activity_counts.sort_values("Count"),
            x="Count", y="Activity", orientation="h",
            color="Count",
            color_continuous_scale=[[0, "#1e3a5f"], [0.5, "#4f46e5"], [1, "#22d3ee"]],
            text="Count",
        )
        fig_act.update_traces(
            texttemplate="%{text:,}", textposition="outside", marker_line_width=0
        )
        fig_act.update_coloraxes(showscale=False)
        fig_act.update_layout(
            **CHART_THEME,
            title="Number of Resources per Activity Type",
            xaxis_title="", yaxis_title="", height=420,
        )
        fig_act.update_xaxes(showticklabels=False)
        st.plotly_chart(fig_act, use_container_width=True)

        _divider()

        # ── Timeline ──────────────────────────────────────────────────────────
        _section("⏳", "Student Activity Timeline")
        timeline = student_vle["date"].value_counts().sort_index().reset_index()
        timeline.columns = ["Day", "Interactions"]

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=timeline["Day"], y=timeline["Interactions"],
            mode="lines",
            line=dict(color="#22d3ee", width=2),
            fill="tozeroy", fillcolor="rgba(34,211,238,0.07)",
        ))
        fig_line.add_vline(
            x=0, line_dash="dash", line_color="rgba(248,113,113,0.55)",
            annotation_text="Course Start", annotation_font_color="#f87171",
        )
        fig_line.update_layout(
            **CHART_THEME,
            title="Daily Interaction Volume (sample: 200 k rows)",
            xaxis_title="Day Relative to Course Start",
            yaxis_title="Interactions",
            showlegend=False, height=300,
        )
        st.plotly_chart(fig_line, use_container_width=True)

        _divider()

        # ── Click stats ───────────────────────────────────────────────────────
        _section("🖱️", "Click Behaviour Statistics")
        desc  = student_vle["sum_click"].describe()
        stats = [
            ("Min",    f'{desc["min"]:.0f}'),
            ("25 %",   f'{desc["25%"]:.0f}'),
            ("Median", f'{desc["50%"]:.0f}'),
            ("Mean",   f'{desc["mean"]:.1f}'),
            ("75 %",   f'{desc["75%"]:.0f}'),
            ("Max",    f'{desc["max"]:.0f}'),
        ]
        cols = st.columns(len(stats))
        for col, (label, val) in zip(cols, stats):
            col.markdown(
                f'<div class="stat-pill">{label}<span>{val}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        fig_hc = px.histogram(
            student_vle[student_vle["sum_click"] < 50],
            x="sum_click", nbins=49,
            color_discrete_sequence=["#6366f1"],
        )
        fig_hc.update_layout(
            **CHART_THEME,
            title="Distribution of Clicks per Interaction (clipped at 50)",
            xaxis_title="Clicks", yaxis_title="Frequency", bargap=0.05,
        )
        st.plotly_chart(fig_hc, use_container_width=True)

        _divider()

        # ── Activity vs Performance ───────────────────────────────────────────
        _section("🔍", "Activity Type vs Student Outcome")
        logs = student_vle.merge(vle, on="id_site", how="left")
        logs = logs.merge(student_info[["id_student", "final_result"]], on="id_student")

        activity_result = (
            logs.groupby(["activity_type", "final_result"])
            .size()
            .reset_index(name="Count")
        )
        fig_grp = px.bar(
            activity_result,
            x="activity_type", y="Count",
            color="final_result", barmode="group",
            color_discrete_map=color_map,
        )
        fig_grp.update_traces(marker_line_width=0)
        fig_grp.update_layout(
            **CHART_THEME,
            title="Interaction Counts by Activity Type and Outcome",
            xaxis_title="Activity Type", yaxis_title="Interactions",
            legend_title_text="Outcome", height=420,
        )
        st.plotly_chart(fig_grp, use_container_width=True)

        _divider()

        # ── Assessment scores ─────────────────────────────────────────────────
        _section("📝", "Assessment Score Distribution")
        col_s1, col_s2 = st.columns([2, 1])

        with col_s1:
            fig_sc = px.histogram(
                student_assessment.dropna(subset=["score"]),
                x="score", nbins=50,
                color_discrete_sequence=["#a78bfa"],
            )
            fig_sc.update_layout(
                **CHART_THEME,
                title="Score Frequency Across All Assessments",
                xaxis_title="Score (0–100)", yaxis_title="Count", bargap=0.04,
            )
            st.plotly_chart(fig_sc, use_container_width=True)

        with col_s2:
            st.markdown(
                '<p style="font-size:.75rem;font-weight:600;color:#64748b;'
                'text-transform:uppercase;letter-spacing:1.4px;margin-bottom:8px">'
                'Score Summary</p>',
                unsafe_allow_html=True,
            )
            st.dataframe(
                student_assessment["score"]
                .describe()
                .round(2)
                .to_frame()
                .rename(columns={"score": "Value"}),
                use_container_width=True,
            )

        _divider()

        # ── Missing values ────────────────────────────────────────────────────
        _section("🧹", "Data Quality — Missing Values")
        datasets = {
            "studentVle":        student_vle,
            "studentInfo":       student_info,
            "vle":               vle,
            "studentAssessment": student_assessment,
            "assessments":       assessments,
        }
        missing_data = {n: int(df.isnull().sum().sum()) for n, df in datasets.items()}

        fig_mv = px.bar(
            x=list(missing_data.keys()),
            y=list(missing_data.values()),
            color=list(missing_data.values()),
            color_continuous_scale=[[0, "#1e3a5f"], [1, "#f87171"]],
            text=list(missing_data.values()),
        )
        fig_mv.update_traces(textposition="outside", marker_line_width=0)
        fig_mv.update_coloraxes(showscale=False)
        fig_mv.update_layout(
            **CHART_THEME,
            title="Total Missing Values per Dataset",
            xaxis_title="", yaxis_title="Missing Cells", height=320,
        )
        st.plotly_chart(fig_mv, use_container_width=True)

        _divider()

        # ── Sample data ───────────────────────────────────────────────────────
        _section("🔎", "Sample VLE Interactions")
        st.dataframe(student_vle.head(10), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error("⚠️  Could not load datasets. Make sure the OULAD CSVs are in `data/raw/`.")
        st.exception(e)