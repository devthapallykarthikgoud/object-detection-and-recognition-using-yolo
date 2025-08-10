import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass