import streamlit as st
import streamlit.components.v1 as components
import pickle
import numpy as np
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Dropout Intelligence",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f) 

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Appearance")
theme = st.sidebar.radio("Theme Mode", ["Dark", "Light"])

# ---------------- THEME SETTINGS ----------------
if theme == "Dark":
    background = "linear-gradient(135deg, #1f2937, #111827)"
    card_bg = "rgba(255,255,255,0.05)"
    text_color = "white"
    accent = "#6366f1"
    input_bg = "#1f2937"
    ring_bg = "#374151"
else:
    background = "linear-gradient(135deg, #f9fafb, #e5e7eb)"
    card_bg = "white"
    text_color = "black"
    accent = "#4f46e5"
    input_bg = "white"
    ring_bg = "#d1d5db"

# ---------------- CUSTOM CSS ----------------
st.markdown(f"""
<style>
.stApp {{
    background: {background};
}}

.card {{
    background: {card_bg};
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}}

.header {{
    font-size: 28px;
    font-weight: 700;
    color: {text_color};
    margin-bottom: 25px;
}}

.section-title {{
    font-size: 20px;
    font-weight: 600;
    color: {text_color};
    padding-bottom: 6px;
    border-bottom: 2px solid {accent};
    margin-bottom: 15px;
}}

label {{
    color: {text_color} !important;
    font-weight: 500;
}}

p, span, div, li {{
    color: {text_color} !important;
}}

input, textarea {{
    background-color: {input_bg} !important;
    color: {text_color} !important;
}}

div[data-baseweb="select"] > div {{
    background-color: {input_bg} !important;
    color: {text_color} !important;
}}

div[data-baseweb="select"] span {{
    color: {text_color} !important;
}}
/* Sidebar Styling */
section[data-testid="stSidebar"] {{ 
    background-color: #111827 !important;
}}

section[data-testid="stSidebar"] * {{ 
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header'>🎓 AI Dropout Risk Intelligence System</div>", unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["🧠 Individual Analysis", "📊 Batch Monitoring"])

# =========================================================
# 🧠 INDIVIDUAL ANALYSIS TAB
# =========================================================

with tab1:
    left, right = st.columns([1, 1])

    # LEFT PANEL
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>👤 Student Profile</div>", unsafe_allow_html=True)

        colp1, colp2 = st.columns(2)
        with colp1:
            student_name = st.text_input("Name")
            roll_no = st.text_input("Roll No")
        with colp2:
            department = st.selectbox("Dept", ["CSE", "ECE", "ME", "CE", "BCA"])
            semester = st.selectbox("Sem", ["1","2","3","4","5","6","7","8"])

        st.markdown("<div class='section-title'>📊 Academic Indicators</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            attendance = st.number_input("Attendance", 0, 100, 75)
            marks = st.number_input("Marks", 0, 100, 65)
            participation = st.number_input("Participation", 1, 10, 5)
        with col2:
            assignments = st.number_input("Assignments", 0, 100, 70)
            study_hours = st.number_input("Study Hrs", 0, 40, 10)

        st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT PANEL
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>📈 Risk Intelligence</div>", unsafe_allow_html=True)

        input_data = np.array([[attendance, assignments, marks, study_hours, participation]])
        probability = model.predict_proba(input_data)[0][1]
        percentage = round(probability * 100, 2)

        if probability > 0.6:
            color = "#ef4444"
            label = "HIGH RISK"
        elif probability > 0.3:
            color = "#f59e0b"
            label = "MEDIUM RISK"
        else:
            color = "#22c55e"
            label = "LOW RISK"

        radius = 65
        circumference = 2 * 3.1416 * radius
        offset = circumference - (percentage / 100) * circumference

        gauge_html = f"""
        <div style="display:flex; justify-content:center;">
            <svg width="200" height="200">
                <circle cx="100" cy="100" r="{radius}"
                    stroke="{ring_bg}" stroke-width="15" fill="none"/>
                <circle cx="100" cy="100" r="{radius}"
                    stroke="{color}" stroke-width="15"
                    fill="none"
                    stroke-dasharray="{circumference}"
                    stroke-dashoffset="{offset}"
                    stroke-linecap="round"
                    transform="rotate(-90 100 100)"
                />
                <text x="50%" y="50%"
                    dominant-baseline="middle"
                    text-anchor="middle"
                    font-size="26"
                    font-weight="bold"
                    fill="{color}">
                    {percentage}%
                </text>
            </svg>
        </div>
        <div style="text-align:center; font-size:18px; font-weight:600; color:{color}; margin-top:5px;">
            {label}
        </div>
        """

        components.html(gauge_html, height=240)

        # AI ANALYSIS ENGINE
        st.markdown("<div class='section-title'>🧠 AI Risk Analysis Engine</div>", unsafe_allow_html=True)

        indicators = {
            "Attendance": attendance,
            "Assignments": assignments,
            "Marks": marks,
            "Study Hours": study_hours * 3,
            "Participation": participation * 10
        }

        sorted_indicators = sorted(indicators.items(), key=lambda x: x[1])
        primary_driver = sorted_indicators[0]
        secondary_driver = sorted_indicators[1]

        def severity_color(value):
            if value < 40:
                return "#ef4444", "CRITICAL"
            elif value < 60:
                return "#f59e0b", "MODERATE"
            else:
                return "#22c55e", "STABLE"

        p_color, p_level = severity_color(primary_driver[1])
        s_color, s_level = severity_color(secondary_driver[1])

        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.25); padding:12px; border-radius:10px; margin-bottom:10px;">
            <b>Primary Risk Driver:</b><br>
            <span style="color:{p_color}; font-weight:600;">
            {primary_driver[0]} — {p_level}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.25); padding:12px; border-radius:10px; margin-bottom:15px;">
            <b>Secondary Risk Driver:</b><br>
            <span style="color:{s_color}; font-weight:600;">
            {secondary_driver[0]} — {s_level}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🚀 Intervention Protocol</div>", unsafe_allow_html=True)

        if probability > 0.6:
            st.write("• Immediate faculty counseling")
            st.write("• Assign dedicated mentor")
            st.write("• Weekly academic review")
            st.write("• Structured recovery plan")
        elif probability > 0.3:
            st.write("• Bi-weekly mentoring")
            st.write("• Monitor assignment consistency")
            st.write("• Engagement reinforcement strategy")
        else:
            st.write("• Maintain academic stability")
            st.write("• Encourage skill development")
                    # ---------------- MODEL EXPLAINABILITY ----------------
        st.markdown("<div class='section-title'>🔍 Model Explainability</div>", unsafe_allow_html=True)

        try:
            if hasattr(model, "coef_"):
                importance = model.coef_[0]
            elif hasattr(model, "feature_importances_"):
                importance = model.feature_importances_
            else:
                importance = None

            if importance is not None:
                feature_names = [
                    "Attendance",
                    "Assignments",
                    "Marks",
                    "Study Hours",
                    "Participation"
                ]

                importance_df = pd.DataFrame({
                    "Feature": feature_names,
                    "Importance": np.abs(importance)
                })

                importance_df = importance_df.sort_values(by="Importance", ascending=False)

                st.bar_chart(importance_df.set_index("Feature"))

            else:
                st.write("Model does not support feature importance visualization.")

        except:
            st.write("Explainability module unavailable for this model.")


        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 📊 BATCH MONITORING TAB
# =========================================================
with tab2:
    st.markdown("<div class='section-title'>📊 Institutional Risk Dashboard</div>", unsafe_allow_html=True)

    np.random.seed(42)
    num_students = 20

    # MUST MATCH TRAINING FEATURE NAMES EXACTLY
    data = pd.DataFrame({
        "student_id": [f"S{100+i}" for i in range(num_students)],
        "attendance": np.random.randint(30, 100, num_students),
        "assignments": np.random.randint(30, 100, num_students),
        "marks": np.random.randint(30, 100, num_students),
        "study_hours": np.random.randint(1, 30, num_students),
        "participation": np.random.randint(1, 10, num_students)
    })

    # Use exact same order as training
    features = data[[
        "attendance",
        "assignments",
        "marks",
        "study_hours",
        "participation"
    ]]

    probabilities = model.predict_proba(features)[:, 1]
    data["Risk %"] = (probabilities * 100).round(2)

    def classify(r):
        if r > 60:
            return "CRITICAL"
        elif r > 30:
            return "MODERATE"
        else:
            return "LOW"

    data["Risk Level"] = data["Risk %"].apply(classify)
    data = data.sort_values(by="Risk %", ascending=False)

    st.markdown("### 🚨 High Priority Cases")
    st.dataframe(data[data["Risk Level"] == "CRITICAL"], use_container_width=True)
        # ---------------- REAL-TIME ALERT SIMULATION ----------------
    st.markdown("<div class='section-title'>🚨 Real-Time Alert System</div>", unsafe_allow_html=True)

    critical_students = data[data["Risk Level"] == "CRITICAL"]

    if not critical_students.empty:
        alert_count = len(critical_students)

        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #ef4444, #b91c1c);
            padding: 15px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 0 15px rgba(239,68,68,0.6);
            animation: pulse 1.5s infinite;
        ">
        🔴 ALERT: {alert_count} Student(s) Entered Critical Risk Zone<br>
        Immediate Academic Intervention Required
        </div>
        """, unsafe_allow_html=True)

        for sid in critical_students["student_id"].head(3):
            st.write(f"• Notification sent to Academic Advisor for {sid}")

    else:
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, #22c55e, #15803d);
            padding: 12px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
        ">
        ✅ All Students Within Safe Monitoring Threshold
        </div>
        """, unsafe_allow_html=True)


    st.markdown("### 📋 Full Risk Ranking")
    st.dataframe(data, use_container_width=True)



