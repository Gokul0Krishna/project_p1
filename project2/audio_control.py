import pyaudio
import wave
import pyttsx3
import speech_recognition as sr


class Audio():
    def __init__(self):
        self.tts = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen(self):
        data=''
        while True:
            cmd = input("\n👉 Press ENTER to record (or type 'exit'): ")
            if cmd.strip().lower() == "exit":
                print("📴 Call ended.")
                break
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("🎙️ Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                try:
                    user_text = self.recognizer.recognize_google(audio)
                except sr.UnknownValueError:
                    user_text = ''
                except sr.RequestError:
                    print("⚠️ STT service unavailable")
                if user_text.lower()=='end call':
                    break
            data+=f'.{user_text}'
        return data
    
    def speak(self):
        pass 