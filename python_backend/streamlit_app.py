# streamlit_app.py
import streamlit as st
import json
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AI Interview Analyzer", layout="centered")

ROOT = Path(__file__).parent.resolve()
QUESTIONS_FILE = ROOT / "selected_questions.json"

# --------------------------------------------------
# QUESTION BANK
# --------------------------------------------------
QUESTION_BANK = {
    "Python": {
        "low": [
            "What is a list in Python?",
            "How do you create a function in Python?",
            "What is the difference between a list and a tuple?",
            "How do you install a package using pip?",
            "What does if __name__ == '__main__' do?"
        ],
        "intermediate": [
            "Explain list comprehensions.",
            "How does exception handling work?",
            "What are generators?",
            "Explain decorators.",
            "How do virtual environments work?"
        ],
        "high": [
            "Explain Python GIL.",
            "How do you optimize Python code?",
            "Explain async and await.",
            "How do you design scalable Python apps?",
            "How do you profile memory usage?"
        ]
    }
}

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("🎤 AI Interview Analyzer")

st.markdown("Fill the details below to start a **real-time mock interview**.")

with st.form("interview_form"):
    name = st.text_input("Candidate Name")
    email = st.text_input("Email ID")

    domain = st.selectbox("Select Domain", list(QUESTION_BANK.keys()))
    level = st.selectbox("Interview Level", ["low", "intermediate", "high"])
    role = st.text_input("Job Role / Field", value="Software Developer")

    n_questions = st.slider("Number of Questions", 1, 7, 5)

    start_btn = st.form_submit_button("🚀 Start Interview")

# --------------------------------------------------
# LOGIC
# --------------------------------------------------
if start_btn:
    if not name or not email:
        st.error("❌ Please enter Name and Email")
    else:
        bank = QUESTION_BANK[domain][level]

        # rotate if fewer questions
        selected_questions = [
            bank[i % len(bank)] for i in range(n_questions)
        ]

        payload = {
            "candidate_name": name,
            "email": email,
            "domain": domain,
            "level": level,
            "role": role,
            "questions": selected_questions
        }

        # save for interview runner
        with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        st.success("✅ Questions generated successfully!")

        st.subheader("📋 Interview Questions (for record)")
        for i, q in enumerate(selected_questions, 1):
            st.write(f"{i}. {q}")

        st.info(
            "🎥 Interview will start now.\n\n"
            "• Webcam window will open\n"
            "• Questions will be spoken\n"
            "• Answer by voice\n"
            "• Close webcam or press **Q** to finish"
        )

        # --------------------------------------------------
        # START INTERVIEW SCRIPT
        # --------------------------------------------------
        python_exe = sys.executable
        runner_script = ROOT / "real_time_interview_from_ui.py"

        try:
            subprocess.Popen(
                [python_exe, str(runner_script)],
                cwd=str(ROOT)
            )
            st.success("🎬 Interview started successfully!")
        except Exception as e:
            st.error(f"❌ Failed to start interview: {e}")
