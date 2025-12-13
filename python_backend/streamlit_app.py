# streamlit_app.py
import streamlit as st
import json
import subprocess
import sys
from pathlib import Path

QUESTION_BANK = {
    "Python": {
        "low": [
            "What is a list in Python?",
            "How do you create a function in Python?",
            "What is the difference between a list and a tuple?",
            "How do you install a package using pip?",
            "What does 'if __name__ == \"__main__\"' do?"
        ],
        "intermediate": [
            "Explain list comprehensions with an example.",
            "How does exception handling work in Python?",
            "What are generators and when to use them?",
            "Explain decorators with a simple use case.",
            "How do you manage virtual environments?"
        ],
        "high": [
            "Explain Python's GIL and its impact on multithreading.",
            "How would you optimize a slow Python program?",
            "Describe how you would design a Python package for reuse.",
            "Explain async/await in Python with an example.",
            "How do you profile memory usage in Python?"
        ]
    },
    "Data Science / ML": {
        "low": [
            "What is the difference between supervised and unsupervised learning?",
            "What is a dataset split and why is it important?",
            "Explain what a feature is in ML.",
            "What is overfitting in simple terms?",
            "Name a few evaluation metrics for classification."
        ],
        "intermediate": [
            "Explain bias-variance tradeoff.",
            "How does cross-validation work?",
            "What is regularization and why is it used?",
            "Describe how a decision tree decides splits.",
            "How would you handle class imbalance?"
        ],
        "high": [
            "Explain gradient descent variants and their differences.",
            "How do you deploy an ML model to production?",
            "Discuss techniques for explainability in ML.",
            "How do you approach feature engineering for complex data?",
            "Describe how you would tune a large model efficiently."
        ]
    },
    "Web Development": {
        "low": [
            "What is HTML and why is it used?",
            "What is CSS used for?",
            "How does a browser request a web page?",
            "What is JavaScript used for?",
            "What does HTTP stand for?"
        ],
        "intermediate": [
            "Explain RESTful APIs.",
            "What is CORS and why might you see it?",
            "How do you maintain state in a web app?",
            "Explain difference between client-side and server-side rendering.",
            "How would you secure an API endpoint?"
        ],
        "high": [
            "How do you scale a web application?",
            "Explain web sockets and when to use them.",
            "Describe microservices architecture pros and cons.",
            "How would you design a highly available backend?",
            "What strategies do you use for performance optimization?"
        ]
    }
}

DEFAULT_DOMAIN = "Python"
DEFAULT_LEVEL = "low"
DEFAULT_ROLE = "Software Developer"

ROOT = Path(__file__).parent.resolve()
QUESTIONS_FILE = ROOT / "selected_questions.json"

st.set_page_config(page_title="AI Interview — Start", layout="centered")

st.title("AI Interview — Setup")

with st.form("setup_form"):
    domain = st.selectbox("Select Domain", options=list(QUESTION_BANK.keys()), index=0)
    level = st.selectbox("Select Interview Level", options=["low", "intermediate", "high"], index=0)
    role = st.text_input("Job Role / Field", value=DEFAULT_ROLE)
    n_questions = st.slider("Number of questions", min_value=1, max_value=7, value=5)
    start_button = st.form_submit_button("Generate Questions & Start Interview")

if start_button:
    # pick questions
    bank = QUESTION_BANK.get(domain, QUESTION_BANK[DEFAULT_DOMAIN])
    choices = bank.get(level, bank[DEFAULT_LEVEL])
    # if fewer than needed, cycle
    selected = []
    for i in range(n_questions):
        selected.append(choices[i % len(choices)])

    payload = {
        "domain": domain,
        "level": level,
        "role": role,
        "questions": selected
    }

    # save to file read by the interview runner
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    st.success(f"Saved {len(selected)} questions for domain={domain}, level={level}, role={role}")
    st.write("Questions:")
    for i, q in enumerate(selected, start=1):
        st.write(f"{i}. {q}")

    st.info("Starting interview script (it will open a webcam window). Close the webcam window when finished or press 'q' inside the webcam window.")

    # Launch the interviewer as a separate process
    # Use the same python executable that runs Streamlit
    python_exe = sys.executable
    runner = ROOT / "real_time_interview_from_ui.py"
    try:
        # start the interview runner as a new process (non-blocking)
        subprocess.Popen([python_exe, str(runner)], cwd=str(ROOT))
        st.success("Interview started in a separate window.")
    except Exception as e:
        st.error(f"Failed to start interview: {e}")
