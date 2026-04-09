import streamlit as st
import matplotlib.pyplot as plt

from logic.processor import process_data
from logic.diagnosis import run_diagnosis
from logic.learning_style import get_learning_style
from logic.recommender import generate_recommendations
from logic.scheduler import generate_schedule

# ---- page config ----
st.set_page_config(page_title="Learning Advisor", layout="wide")

# ---- title ----
st.title("📊 Personalized Learning Advisor")
st.write("Analyze your learning behavior and get a personalized study plan.")

# ---- input section ----
st.subheader("⏱️ Daily Availability")

daily_time = st.number_input(
    "Available study time (minutes per day)",
    min_value=30,
    max_value=600,
    value=120,
    step=10
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
    style = get_learning_style(processed)
    recs = generate_recommendations(diagnosis)
    schedule = generate_schedule(diagnosis, daily_time)

    # ---- learning style ----
    st.subheader("🧬 Learning Style")
    st.success(style)

    # ---- explainability (NEW) ----
    st.subheader("🧠 Why This Plan?")

    for d in diagnosis:
        if d["subject"].strip() == "":
            continue

        st.write(
            f"📘 {d['subject']}: Score = {d['score']}%, Time = {d['time']} min → {d['issue']}"
        )

    # ---- diagnosis section ----
    st.subheader("🧠 Subject-wise Diagnosis")

    for d in diagnosis:

        if d["subject"].strip() == "":
            continue

        st.markdown(f"### 📘 {d['subject']} ({d['topic']})")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Score", f"{d['score']}%")

        with c2:
            st.metric("Effort", d["effort_level"])

        with c3:
            # ---- colored status (UPDATED) ----
            if d["status"] == "Weak":
                st.error("Weak 🔴")
            elif d["status"] == "Moderate":
                st.warning("Moderate 🟡")
            else:
                st.success("Strong 🟢")

        st.write(f"**Issue Identified:** {d['issue']}")
        st.write("---")

    # ---- recommendations ----
    st.subheader("📌 Personalized Recommendations")

    for r in recs:
        st.markdown(f"### 📘 {r['subject']}")
        st.info(r["message"])

    # ---- daily schedule ----
    st.subheader("📅 Daily Study Plan")

    for s in schedule:
        st.write(
            f"📘 {s['subject']} → {s['time']} min "
            f"({s['sessions']} sessions) [{s['status']}]"
        )

    st.subheader("🔁 Revision Strategy")
    st.write("• Weak subjects → daily")
    st.write("• Moderate → every 2 days")
    st.write("• Strong → twice a week")

    # ================= WEEKLY PLAN =================
    st.subheader("🗓️ Weekly Study Plan")

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekly_plan = {day: [] for day in days}

    for s in schedule:

        subject = s["subject"]
        base_time = s["time"]
        status = s["status"]

        if status == "Weak":
            for i, day in enumerate(days):
                if i % 2 == 0:
                    time = int(base_time * 1.2)
                else:
                    time = int(base_time * 0.8)
                weekly_plan[day].append((subject, time))

        elif status == "Moderate":
            for i, day in enumerate(days):
                if i % 2 == 0:
                    weekly_plan[day].append((subject, int(base_time * 0.7)))

        else:
            weekly_plan["Wed"].append((subject, int(base_time * 0.5)))
            weekly_plan["Sun"].append((subject, int(base_time * 0.6)))

    cols = st.columns(4)

    for i, day in enumerate(days):
        with cols[i % 4]:
            st.markdown(f"**{day}**")

            if not weekly_plan[day]:
                st.info("Rest / Light revision")
            else:
                for sub, time in weekly_plan[day]:
                    st.write(f"{sub} → {time} min")

    # ---- graphs ----
    st.subheader("📊 Performance Overview")

    names = [d["subject"] for d in diagnosis if d["subject"].strip() != ""]
    scores = [d["score"] for d in diagnosis if d["subject"].strip() != ""]
    times = [d["time"] for d in diagnosis if d["subject"].strip() != ""]
    efficiency = [d["efficiency"] for d in diagnosis if d["subject"].strip() != ""]

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        colors = ["green" if s >= 75 else "orange" if s >= 50 else "red" for s in scores]
        ax1.bar(names, scores, color=colors)
        ax1.set_title("Performance (%)")

        for i, v in enumerate(scores):
            ax1.text(i, v + 2, str(v), ha='center', fontsize=8)

        plt.tight_layout()
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.bar(names, times)
        ax2.set_title("Study Time")

        for i, v in enumerate(times):
            ax2.text(i, v + 2, str(v), ha='center', fontsize=8)

        plt.tight_layout()
        st.pyplot(fig2)

    fig3, ax3 = plt.subplots(figsize=(6, 3))
    eff_colors = ["green" if e >= 1 else "orange" if e >= 0.5 else "red" for e in efficiency]

    ax3.bar(names, efficiency, color=eff_colors)
    ax3.set_title("Efficiency (Score / Time)")

    for i, v in enumerate(efficiency):
        ax3.text(i, v + 0.05, str(round(v, 2)), ha='center', fontsize=8)

    plt.tight_layout()
    st.pyplot(fig3)