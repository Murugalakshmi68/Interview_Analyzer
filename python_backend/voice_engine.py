import pyttsx3
import threading
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()
# voice_engine.py
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

_engine = None

def speak(text):
    global _engine
    if pyttsx3 is None:
        print("🔇 TTS not available:", text)
        return

    if _engine is None:
        _engine = pyttsx3.init()

    _engine.say(text)
    _engine.runAndWait()


def speak(text):
    def _speak():
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    threading.Thread(target=_speak, daemon=True).start()
