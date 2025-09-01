import threading
import queue
import speech_recognition as sr
import pyttsx3
from AI_agents import AI
import streamlit as st

class Call:
    def __init__(self):
        self.agent = AI()
        self.tts = pyttsx3.init()
        self.q = queue.Queue()
        self.running = True
            
    # def listen_loop(self):
    #     recognizer = sr.Recognizer()
    #     with sr.Microphone() as mic:
    #         recognizer.adjust_for_ambient_noise(mic)
    #         while self.running:
    #             print("🎙️ Start speaking...")
    #             try:
    #                 audio = recognizer.listen(mic, phrase_time_limit=5)
    #                 text = recognizer.recognize_google(audio)
    #                 print(f"👤 You: {text}")
                    
    #                 # Stop call if user says "end call"
    #                 if text.strip().lower() in ["end call", "bye", "exit"]:
    #                     self.running = False
    #                     break
                    
    #                 self.q.put(text)
    #             except sr.UnknownValueError:
    #                 print("⚠️ Didn't catch that.")
    #             except sr.RequestError:
    #                 print("⚠️ Speech service unavailable.")
    #             except Exception as e:
    #                 print(f"⚠️ Error: {e}")
    #             if text:
    #                 try:
    #                     response = self.agent.rn(query=text)
    #                     print(f"🤖 Agent: {response}")
    #                     self.tts.say(response)
    #                     self.tts.runAndWait()
    #                 except queue.Empty:
    #                     continue



    # def run(self):
    #     t1 = threading.Thread(target=self.listen_loop, daemon=True)
    #     # t2 = threading.Thread(target=self.talk_loop, daemon=True)
    #     t1.start()
    #     # t2.start()

    #     # keep main thread alive until call ends
    #     try:
    #         while self.running:
    #             pass
    #     except KeyboardInterrupt:
    #         self.running = False
    #         print("\n📴 Call ended.")

    def listen(self,audio):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(audio) as source:
                audio_data = recognizer.record(source) 
                text = recognizer.recognize_google(audio_data)
                print(text)
                return text
        except sr.UnknownValueError:
            print("⚠️ Didn't catch that.")
        except sr.RequestError:
            print("⚠️ Speech service unavailable.")
        except Exception as e:
            print(f"⚠️ Error: {e}")
    
    
    def speak(self,response):
        try:
            self.tts.say(response)
            self.tts.runAndWait()
        except Exception as e:
            pass

    
if __name__ == "__main__":
    obj = Call()
    obj.run()
