import time
from modes.human_behavior import HumanBehavior
from modes.police_behavior import PoliceBehavior
from interface.speaker import Speaker
from vision.camera import RobotCamera
import config
from movement.motors import mou_cap

class Agent:
    def __init__(self, camera:RobotCamera= None, speaker:Speaker= None):
        self.mode = config.DEFAULT_MODE
        self.submode = "default"
        self.speaker = speaker
        self.camera = camera

        self.human = HumanBehavior(self.speaker)
        self.police = PoliceBehavior(self.speaker, self.camera)

        self.running = True
        self.last_action_time = 0

    def set_mode(self, mode):
        if mode in ["human", "police"]:
            print(f"Mode ➜ {mode}")
            self.mode = mode
            self.submode = "default"
        else:
            print(f"Mode desconegut: {mode}")

    def set_submode(self, submode):
        print(f"Submode ➜ {submode}")
        self.submode = submode

    def run(self):
        print("Agent en execució...")
        while self.running:
            now = time.time()

            # Limita la freqüència d'acció (ex: cada 5s)
            if now - self.last_action_time >= 5:
                self._execute_mode()
                self.last_action_time = now

            time.sleep(0.1)  # Redueix ús de CPU

    def stop(self):
        print("Aturant Agent")
        self.running = False

    def _execute_mode(self):
        print(f"Executant: mode={self.mode}, submode={self.submode}")
        if self.mode == "human":
            self.human.express_emotion(self.submode)
        elif self.mode == "police":
            if self.submode == "default":
                self.police.detect_license_plate()
            else:
                print(f"Submode policial desconegut: {self.submode}")

    def handle_gemini_response(self, text: str):
        text = text.lower()

        # ✅ Exemple de mapping
        if "emocionat" in text or "content" in text:
            self.set_mode("human")
            self.set_submode("happy")
        elif "trist" in text:
            self.set_mode("human")
            self.set_submode("sad")
        elif "enfadat" in text:
            self.set_mode("human")
            self.set_submode("angry")
        elif "patrulla" in text:
            self.set_mode("human")
            self.set_submode("patrol")
        elif "matrícula" in text or "detectar" in text:
            self.set_mode("police")
            self.set_submode("detect")
        else:
            print(f"❓ No s’ha reconegut cap acció clara a partir del text: {text}")
            if self.speaker:
                self.speaker.say_text("Ho pots repetir? No sé què vols que faci.")
