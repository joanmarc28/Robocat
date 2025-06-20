import speech_recognition as sr
import requests
import time
from modes.agent import Agent
from movement.motors import mou_cap
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["ALSA_CARD"] = "default"
os.environ["SDL_AUDIODRIVER"] = "dsp"

class Micro:
    def __init__(self, agent:Agent=None, wake_word="Hola", language="ca-ES", device_index=None):
        self.agent = agent
        self.wake_word = wake_word.lower()
        self.language = language
        self.device_index = device_index
        self.recognizer = sr.Recognizer()
        self._running = True

    def stop(self):
        self._running = False

    def say(self, text):
        if self.agent and hasattr(self.agent, "speaker"):
            """self.agent.speaker.say_text(text)"""
        else:
            print(f"🔊 {text}")

    def send_to_gemini(self, text):
        url = "https://your-google-cloud-endpoint.com/chat"  # <-- el teu endpoint
        try:
            response = requests.post(url, json={"text": text})
            return response.json().get("response", None)
        except Exception as e:
            return f"[Error amb Gemini: {str(e)}]"

    def listen_once(self, timeout=5, phrase_time_limit=5):
        with sr.Microphone(device_index=self.device_index) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                return self.recognizer.recognize_google(audio, language=self.language).lower()
            except:
                return None

    def run(self):
        while self._running:
            print("👂 Escoltant wake word...")
            text = self.listen_once(timeout=5, phrase_time_limit=3)
            if text and self.wake_word in text:
                print("✅ Wake word detectada!")
                """self.say("Et sento. Digues què vols que faci.")"""
                mou_cap()
                self.agent.speaker.say_emotion("surprised")

                command = self.listen_once(timeout=5, phrase_time_limit=6)
                if not command:
                    self.say("No t'he entès bé. Pots repetir?")
                    continue

                """response = self.send_to_gemini(command)
                print("🤖 Gemini:", response)
                self.say(response or "No he pogut obtenir resposta.")

                if self.agent:
                    self.agent.handle_gemini_response(response or "")"""
            time.sleep(0.5)
