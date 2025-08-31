# import pyaudio
# import wave
# import pyttsx3
# import speech_recognition as sr


# class Audio():
#     def __init__(self):
#         self.tts = pyttsx3.init()
#         self.recognizer = sr.Recognizer()
#         self.mic = sr.Microphone()

#     def listen(self):
#         data=''
#         while True:
#             cmd = input("\n👉 Press ENTER to record (or type 'exit'): ")
#             if cmd.strip().lower() == "exit":
#                 print("📴 Call ended.")
#                 break
#             with self.mic as source:
#                 self.recognizer.adjust_for_ambient_noise(source)
#                 print("🎙️ Listening...")
#                 audio = self.recognizer.listen(source, timeout=5)
#                 try:
#                     user_text = self.recognizer.recognize_google(audio)
#                 except sr.UnknownValueError:
#                     user_text = ''
#                 except sr.RequestError:
#                     print("⚠️ STT service unavailable")
#                 if user_text.lower()=='end call':
#                     break
#             data+=f'.{user_text}'
#         return data
    
#     def speak(self):
#         pass 

import threading
import queue
import speech_recognition as sr
import pyttsx3
from AI_agents import AI

# agent = AI()
tts = pyttsx3.init()
q = queue.Queue()

def listen_loop():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            print('i')
            audio = recognizer.listen(source, phrase_time_limit=5)
            try:
                text = recognizer.recognize_google(audio)
                q.put(text)
                print(text)
            except:
                pass

def talk_loop():
    while True:
        query = q.get()
        # response = agent.rn(query)
        # response = 'hi am here'
        tts.say(query)
        tts.runAndWait()

threading.Thread(target=listen_loop).start()
threading.Thread(target=talk_loop).start()
