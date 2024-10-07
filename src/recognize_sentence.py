import speech_recognition as sr
from constants import MICROPHONE_ID

recognizer = sr.Recognizer()
with sr.Microphone(device_index=1) as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
    #audio = recognizer.record(source, duration=3)
    try:
        text = recognizer.recognize_google(audio)
        print(text)
    except sr.UnknownValueError:
        print("[Not understood]")
    except sr.RequestError as e:
        print("[Request error]".format(e))
            