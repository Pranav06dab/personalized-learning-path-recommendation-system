import streamlit as st
import plotly.express as px

from logic.processor import process_data
from logic.diagnosis import run_diagnosis
from logic.learning_style import get_learning_style
from logic.recommender import generate_recommendations
from logic.scheduler import generate_schedule
from logic.data_handler import save_data, load_data
from logic.auth import login, signup

# ---- session state ----
if "user" not in st.session_state:
    st.session_state.user = None

# ---- LOGIN PAGE ----
if st.session_state.user is None:

    st.title("🔐 Login / Signup")

    choice = st.radio("Choose Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if signup(username, password):
                st.success("Account created successfully. Please login.")
            else:
                st.error("User already exists")

    else:
        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ---- MAIN APP ----
st.set_page_config(page_title="Learning Advisor", layout="wide")

st.title("📊 Personalized Learning Advisor")
st.markdown(f"### 🚀 Welcome, {st.session_state.user}")
st.write("Analyze your learning behavior and get a personalized study plan.")

# ---- logout button ----
if st.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ---- input section ----
st.subheader("⏱️ Daily Availability")

daily_time = st.number_input(
    "Available study time (minutes per day)",
    30, 600, 120, 10
)

st.subheader("📚 Subject Inputs")

num_subjects = st.slider("Number of subjects", 1, 6, 2)

subjects = []

for i in range(num_subjects):
    st.markdown(f"### Subject {i+1}")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Subject Name", key=f"name_{i}")
        topic = st.text_input("Topic", key=f"topic_{i}")

    with col2:
        score = st.number_input("Score (%)", 0, 100, key=f"s_{i}")
        time = st.number_input("Study Time (min)", 0, 300, key=f"t_{i}")

    col3, col4 = st.columns(2)

    with col3:
        attempts = st.number_input("Attempts", 0, 20, key=f"a_{i}")

    with col4:
        understanding = st.selectbox(
            "Understanding Level",
            ["Low", "Medium", "High"],
            key=f"u_{i}"
        )

    subjects.append({
        "subject": name,
        "topic": topic,
        "score": score,
        "time": time,
        "attempts": attempts,
        "understanding": understanding
    })

# ---- analyze button ----
analyze = st.button("🔍 Analyze Learning Pattern")

# ================= OUTPUT =================
if analyze:

    processed = process_data(subjects)
    diagnosis = run_diagnosis(processed)

    # ---- save per user ----
    save_data(diagnosis, st.session_state.user)

    style = get_learning_style(processed)
    recs = generate_recommendations(diagnosis)
    schedule = generate_schedule(diagnosis, daily_time)

    st.subheader("🧬 Learning Style")
    st.success(style)

    # ---- KPI ----
    col1, col2, col3 = st.columns(3)

    avg_score = sum([d["score"] for d in diagnosis]) / len(diagnosis)
    avg_eff = sum([d["efficiency"] for d in diagnosis]) / len(diagnosis)
    weak_count = len([d for d in diagnosis if d["status"] == "Weak"])

    col1.metric("Average Score", f"{round(avg_score,1)}%")
    col2.metric("Efficiency", f"{round(avg_eff,2)}")
    col3.metric("Weak Subjects", weak_count)

    st.divider()

    # ---- diagnosis ----
    st.subheader("🧠 Subject-wise Diagnosis")

    for d in diagnosis:
        if d["subject"].strip() == "":
            continue

        st.markdown(f"### 📘 {d['subject']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{d['score']}%")
        c2.metric("Effort", d["effort_level"])

        if d["status"] == "Weak":
            c3.error("Weak 🔴")
        elif d["status"] == "Moderate":
            c3.warning("Moderate 🟡")
        else:
            c3.success("Strong 🟢")

        st.write(f"Issue: {d['issue']}")

    st.divider()

    # ---- schedule ----
    st.subheader("📅 Daily Study Plan")

    for s in schedule:
        st.write(f"{s['subject']} → {s['time']} min")

    st.divider()

    # ---- charts ----
    st.subheader("📊 Analytics")

    names = [d["subject"] for d in diagnosis if d["subject"]]
    scores = [d["score"] for d in diagnosis if d["subject"]]

    fig = px.bar(x=names, y=scores, color=scores)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---- progress ----
    st.subheader("📈 Progress Tracking")

    history = load_data(st.session_state.user)

    if history:
        subject_data = {}

        for entry in history:
            subject_data.setdefault(entry["subject"], []).append(entry["score"])

        for sub, scores in subject_data.items():
            if len(scores) < 2:
                continue

            diff = scores[-1] - scores[-2]

            if diff > 0:
                st.success(f"{sub}: +{diff}")
            else:
                st.error(f"{sub}: {diff}")

            fig = px.line(y=scores, markers=True, title=sub)
            st.plotly_chart(fig, use_container_width=True)