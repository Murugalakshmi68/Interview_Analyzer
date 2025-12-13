# real_time_interview_from_ui.py
import cv2
import time
import json
from pathlib import Path
from speech_to_text import listen_and_convert  # assumes this file exists

ROOT = Path(__file__).parent.resolve()
QUESTIONS_FILE = ROOT / "selected_questions.json"

def load_questions():
    if not QUESTIONS_FILE.exists():
        print("No questions file found. Please run the Streamlit UI first.")
        return []
    payload = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    return payload.get("questions", [])

def start_interview(questions):
    cam = cv2.VideoCapture(0)
    q_index = 0
    answers = []

    print("📽 Webcam started. Close webcam window to stop interview.")
    time.sleep(1)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error reading from webcam.")
            break

        cv2.imshow("Real-Time Interview (press 'q' to quit)", frame)

        # if we still have questions to ask
        if q_index < len(questions):
            question = questions[q_index]
            print(f"\n❓ QUESTION {q_index+1}: {question}")
            # small delay so user can see webcam frame
            time.sleep(0.5)

            # listen for the user's answer (this will block until user finishes speaking or
            # times out inside listen_and_convert)
            answer = listen_and_convert()
            answers.append({"question": question, "answer": answer, "timestamp": time.time()})
            print("➡ Saved Answer:", answer)
            q_index += 1
            # small pause before next question
            time.sleep(0.5)
        else:
            # all questions asked; keep showing webcam but wait for user to close
            print("\n✔ All questions have been asked. Close the webcam window or press 'q' to finish.")
            time.sleep(2)

        # allow user to quit by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("❌ Interview ended by user (pressed q).")
            break

        # also break if the window was closed (visibility check)
        if cv2.getWindowProperty("Real-Time Interview (press 'q' to quit)", cv2.WND_PROP_VISIBLE) < 1:
            print("❌ Webcam window closed by user.")
            break

    cam.release()
    cv2.destroyAllWindows()

    # Save answers to a local file
    out_file = ROOT / "interview_answers.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2)
    print(f"✅ Interview finished. Answers saved to {out_file}")

if __name__ == "__main__":
    qs = load_questions()
    if not qs:
        print("No questions available. Exiting.")
    else:
        start_interview(qs)
