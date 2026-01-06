import cv2
import time
import json
from pathlib import Path

from voice_engine import speak
from speech_to_text import listen_and_convert

ROOT = Path(__file__).parent.resolve()
QUESTIONS_FILE = ROOT / "selected_questions.json"


def load_questions():
    if not QUESTIONS_FILE.exists():
        print("❌ No questions file found. Please run the Streamlit UI first.")
        return []

    payload = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    return payload.get("questions", [])


def start_interview(questions):
    cam = cv2.VideoCapture(0)
    answers = []

    if not cam.isOpened():
        print("❌ Webcam not accessible")
        return

    print("📽 Webcam started. Close webcam window or press 'q' to stop interview.")
    time.sleep(1)

    speak(
        "Your interview is starting now. "
        "Please listen carefully to each question and answer clearly."
    )

    q_index = 0
    asking_question = False   # controls repeat speaking

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Error reading from webcam.")
            break

        cv2.imshow("Real-Time Interview (press 'q' to quit)", frame)

        # ---------------- ASK QUESTION ONCE ----------------
        if q_index < len(questions) and not asking_question:
            asking_question = True

            question = questions[q_index]
            print(f"\n❓ QUESTION {q_index + 1}: {question}")

            speak(f"Question {q_index + 1}. {question}")
            time.sleep(0.5)  # allow TTS to start

            print("🎙 Listening for answer...")
            answer = listen_and_convert()

            answers.append({
                "question": question,
                "answer": answer,
                "timestamp": time.time()
            })

            print("➡ Saved Answer:", answer)

            q_index += 1
            asking_question = False
            time.sleep(1)

        # ---------------- INTERVIEW COMPLETED ----------------
        if q_index >= len(questions):
            cv2.putText(
                frame,
                "Interview completed. Press 'q' or close window.",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        # ---------------- EXIT CONDITIONS ----------------
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("❌ Interview ended by user (pressed q).")
            break

        if cv2.getWindowProperty(
            "Real-Time Interview (press 'q' to quit)",
            cv2.WND_PROP_VISIBLE
        ) < 1:
            print("❌ Webcam window closed by user.")
            break

    speak("Your interview is completed. Thank you.")

    cam.release()
    cv2.destroyAllWindows()
    out_file = ROOT / "interview_answers.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2)

    print(f"✅ Interview finished. Answers saved to {out_file}")


if __name__ == "__main__":
    questions = load_questions()
    if not questions:
        print("⚠ No questions available. Exiting.")
    else:
        start_interview(questions)
