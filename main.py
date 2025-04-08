import os
import speech_recognition as sr
import pyaudio

import wave
import sys


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 24100
RECORD_SECONDS = 5

with wave.open('output.wav', 'wb') as wf:
    p = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

    print('Recording...')
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        wf.writeframes(stream.read(CHUNK))
    print('Done')

    stream.close()
    p.terminate()


def takeCommand():
    print("Begin")
    burger = sr.AudioFile('output.wav')
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

