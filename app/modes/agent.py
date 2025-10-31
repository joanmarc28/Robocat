import time
from modes.human_behavior import HumanBehavior
from modes.police_behavior import PoliceBehavior
from modes.city_behavior import CityBehavior
from interface.speaker import Speaker
from vision.camera import RobotCamera
import config
from movement.motors import mou_cap
import threading

class Agent:
    def __init__(self, camera:RobotCamera= None, speaker:Speaker= None, time=0.1,frenquencia=5):
        self.mode = config.DEFAULT_MODE
        self.submode = "default"
        self.speaker = speaker
        self.camera = camera
        self.time = time
        self.frequencia = frenquencia
        self.human = HumanBehavior(self.speaker, self.camera)
        self.police = PoliceBehavior(self.speaker, self.camera)
        self.city = CityBehavior(self.speaker, self.camera)

        self.running = True
        self.last_action_time = 0

    def set_mode(self, mode):
        if mode in ["human", "police", "city"]:
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
            if now - self.last_action_time >= self.frequencia:

                self.last_action_time = now

                new_submode = self._execute_mode()

                if new_submode:
                    if new_submode != self.submode:
                        self.set_submode(new_submode)
                
                if self.speaker:
                    def speak(emotion=self.submode):
                        self.speaker.say_emotion(emotion)

                    t_speak = threading.Thread(target=speak)
                    t_speak.start()
                    t_speak.join()
         
            if self.mode == "human":
                self.time = 0.1  # Més ràpid per a interaccions humanes
                self.frequencia = 5  # Accions humanes més freqüents
            elif self.mode == "police":
                self.time = 0.1  # Més lent per a accions policials
                self.frequencia = 10  # Accions policials menys freqüents
            elif self.mode == "city":
                self.time = 0.1 
                self.frequencia = 5

            time.sleep(self.time)  # Redueix ús de CPU

    def stop(self):
        print("Aturant Agent")
        self.running = False

    def _execute_mode(self):
        print(f"Executant: mode={self.mode}, submode={self.submode}")
        if self.mode == "human":
            resultat = self.human.analitza_emocions()
            if isinstance(resultat, dict):
                nova_reaccio = resultat.get("reaccio")
                if isinstance(nova_reaccio, str) and nova_reaccio:
                    return nova_reaccio
            return None
        if self.mode == "cat":
            resultat = self.human.direct_react(self.submode)
            if isinstance(resultat, dict):
                nova_reaccio = resultat.get("reaccio")
                if isinstance(nova_reaccio, str) and nova_reaccio:
                    return nova_reaccio
            return None
        elif self.mode == "police":
            if self.submode == "default":
                self.police.detect_license_plate()
            else:
                print(f"Submode policial desconegut: {self.submode}")
        ##NOU -> containers
        elif self.mode == "city":
            if self.submode == "default":
                self.city.detect_container()
            else:
                print(f"Submode City desconegut: {self.submode}")
        return None
