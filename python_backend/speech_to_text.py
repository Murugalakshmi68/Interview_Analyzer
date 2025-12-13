import speech_recognition as sr

def listen_and_convert():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎙 Listening...")
        audio_data = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except:
            return ""
