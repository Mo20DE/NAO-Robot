import speech_recognition as sr
from constants import MICROPHONE_NAME, MICROPHONE_ID

with sr.Microphone(device_index=MICROPHONE_ID) as source:
    print(source.list_working_microphones())
    print("===============================")
    print(source.list_microphone_names())
    print("===============================")
    print(source.list_microphone_names().index(MICROPHONE_NAME))
