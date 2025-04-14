import os
import speech_recognition as sr
import pyaudiowpatch as pyaudio
import pyautogui
import wave
import sys
import time

def record_headphones_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100
    RECORD_SECONDS = 5
    OUTPUT_FILENAME = 'output.wav'

    with pyaudio.PyAudio() as p:
        try:
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

            if not default_speakers["isLoopbackDevice"]:
                for loopback in p.get_loopback_device_info_generator():
                    if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        break
                else:
                    print("No loopback device found for your headphones!")
                    return False

            print(f"Recording from: {default_speakers['name']}")

            with wave.open(OUTPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(default_speakers["maxInputChannels"])
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(int(default_speakers["defaultSampleRate"]))

                stream = p.open(
                    format=FORMAT,
                    channels=default_speakers["maxInputChannels"],
                    rate=int(default_speakers["defaultSampleRate"]),
                    input=True,
                    input_device_index=default_speakers["index"],
                    frames_per_buffer=CHUNK
                )

                print(f'Recording for {RECORD_SECONDS} seconds...')
                for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    wf.writeframes(stream.read(CHUNK))
                
                stream.close()
                print('Done recording')
                return True

        except Exception as e:
            print(f"Recording error: {e}")
            return False

def take_command():
    """Process the recorded audio"""
    print("Processing audio...")
    try:
        with sr.AudioFile('output.wav') as source:
            r = sr.Recognizer()
            r.energy_threshold = 5000
            r.pause_threshold = 2.0
                
            print("Listening...")
            audio = r.listen(source)
                
            print("Processing audio...")
            
            said = r.recognize_google(audio)
            print("Full transcript:", said)
            return said.lower()
    
    except Exception as e:
        print(e)
        print("Google didn't understand.")
        return "none"

if __name__ == "__main__":
    if record_headphones_audio():
        command = take_command()
        if "mute" in command:
            pyautogui.hotkey('ctrl', 'shift', 'm')