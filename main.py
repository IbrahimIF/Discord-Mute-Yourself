import os
import speech_recognition as sr

def takeCommand():
    print("Begin")
    burger = sr.AudioFile('handsome.wav')
    r = sr.Recognizer()
    with burger as source:
        print("Listening....")
        audio = r.listen(source)
    try:
        print("Listening deeper....")
        said = r.recognize_google(audio)
        print(said)
    
    except Exception as e:
        print(e)
        print("Google didn't Understand.")
        return "None"
    return said
takeCommand()

