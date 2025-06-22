import speech_recognition as sr
import requests
import time
import difflib
import logging
from modes.agent import Agent
from movement.motors import mou_cap
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["ALSA_CARD"] = "default"
os.environ["SDL_AUDIODRIVER"] = "dsp"

class Micro:
    def __init__(self, agent: Agent = None, wake_word="hola", language="ca-ES",
                 device_index=None, debug=True, log_file="micro.log"):
        self.agent = agent
        self.wake_word = wake_word.lower()
        self.language = language
        self.device_index = device_index
        self.recognizer = sr.Recognizer()
        self._running = True
        self.debug = debug

        # Logger setup
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self._setup_micro()

    def _setup_micro(self):
        # Ajustar soroll ambiental una sola vegada
        try:
            with sr.Microphone(device_index=self.device_index) as source:
                if self.debug:
                    print("🎙️ Ajustant al soroll ambiental...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Improve recognition sensitivity
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.dynamic_energy_adjustment_ratio = 1.5
        except Exception as e:
            if self.debug:
                print(f"[ERROR MICRÒFON] {e}")

    def stop(self):
        self._running = False
        self.logger.info("Microphone stopped")

    def say(self, text):
        if self.agent and hasattr(self.agent, "speaker"):
            self.agent.speaker.say_text(text)
        elif self.debug:
            print(f"[SAY] {text}")
        self.logger.info(f"SAY: {text}")

    def send_to_gemini(self, text):
        url = "https://your-google-cloud-endpoint.com/chat"
        try:
            response = requests.post(url, json={"text": text})
            reply = response.json().get("response", None)
            self.logger.info(f"Gemini response: {reply}")
            return reply
        except Exception as e:
            if self.debug:
                print(f"[Gemini Error] {e}")
            return None

    def listen_once(self, timeout=6, phrase_time_limit=5):
        try:
            with sr.Microphone(device_index=self.device_index) as source:
                if self.debug:
                    print("🎧 Escoltant...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                # Retorna la millor transcripció i registra totes les opcions
                result = self.recognizer.recognize_google(audio, language=self.language, show_all=True)
                if isinstance(result, dict) and "alternative" in result:
                    text = result["alternative"][0].get("transcript", "").lower()
                    self.logger.info(f"Escoltat: {text}")
                    if self.debug:
                        print(f"[Escoltat] {text}")
                        for alt in result["alternative"]:
                            if "transcript" in alt:
                                print(f" - Possible: {alt['transcript']}")
                    return text
                return None
        except Exception as e:
            if self.debug:
                print(f"[Listen Error] {e}")
            return None

    def match_wake_word(self, text):
        ratio = difflib.SequenceMatcher(None, text, self.wake_word).ratio()
        if self.debug:
            print(f"[Similitud wake word] {ratio:.2f}")
        return ratio > 0.7  # Posa-ho més alt si vols més exigència

    def run(self):
        while self._running:
            if self.debug:
                print("👂 Listening for wake word...")
            self.logger.info("Listening for wake word")
            text = self.listen_once(timeout=6, phrase_time_limit=5)

            if text and self.match_wake_word(text):
                if self.debug:
                    print("✅ Wake word detectada!")
                self.logger.info("Wake word detected")

                mou_cap()
                if self.agent:
                    self.agent.speaker.say_emotion("surprised")

                # Aquí pots activar Gemini si vols
                # command = self.listen_once(timeout=7, phrase_time_limit=6)
                # if command:
                #     response = self.send_to_gemini(command)
                #     self.say(response or "Sorry, I didn't understand.")
                #     if self.agent:
                #         self.agent.handle_gemini_response(response or "")
                # else:
                #     self.say("Can you repeat, please?")

            time.sleep(0.3)
