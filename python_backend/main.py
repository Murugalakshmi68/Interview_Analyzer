import cv2
import threading
from speech_to_text import listen_and_convert

running = True  # Global flag

def audio_loop():
    global running
    print("🎙 Audio thread started. Keep speaking...")

    while running:
        text = listen_and_convert()  # Listen once
        if text:
            print("📝 You said:", text)
        else:
            print("⚠ No clear audio detected.")

def video_loop():
    global running
    cap = cv2.VideoCapture(0)
    print("📷 Webcam started. Close the window to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Interview Camera", frame)

        # If webcam window is closed → exit
        if cv2.getWindowProperty("Interview Camera", cv2.WND_PROP_VISIBLE) < 1:
            running = False
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

    cap.release()
    cv2.destroyAllWindows()
    print("📷 Webcam stopped.")

# -----------------------
# MAIN START
# -----------------------
print("Program started!")

# Start threads
t1 = threading.Thread(target=audio_loop)
t2 = threading.Thread(target=video_loop)

t1.start()
t2.start()

t1.join()
t2.join()

print("Program finished.")
