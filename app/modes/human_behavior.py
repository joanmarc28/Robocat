import os
import time
import threading
import base64
import json
import cv2
import requests

from interface.display import clear_displays, displays_show_frames
from interface.speaker import Speaker
from vision.camera import RobotCamera
import config
from utils.helpers import normalize_emocions

class HumanBehavior:
    def __init__(self, speaker: Speaker = None, camera: RobotCamera = None, motors=None):
        self.speaker = speaker
        self.camera = camera
        self.motors = motors
        
        
    def express_emotion(self, emotion, duration=3):
        if emotion not in config.STATES:
            print(f"[HUMAN] Emoció desconeguda: {emotion}")
            return
        if not self.speaker:
            print("[HUMAN] Altaveu no disponible")
            return

        t_inici = time.time()
        while time.time() - t_inici < duration:
            displays_show_frames(emotion)

        #clear_displays()

    def process_emocions(self, emocions: list[str]):
        """Executa una acció en funció de la primera emoció detectada."""
        if not emocions:
            return

        emocio = emocions[0]

        match emocio:
            case "happy":
                self.express_emotion("happy")
            case "sad":
                self.express_emotion("sad")
                if self.motors:
                    self.motors.body_downward()
            case "angry":
                self.express_emotion("angry")
            case "surprised":
                self.express_emotion("surprised")
            case "scared":
                self.express_emotion("scared")
            case "disgusted":
                self.express_emotion("disgusted")
            case "sleepy":
                self.express_emotion("sleepy")
                if self.motors:
                    self.motors.sit_hind_legs()
            case "neutral":
                self.express_emotion("default")
            case _:
                print(f"[HUMAN] Emoció sense acció: {emocio}")

    def analitza_emocions(self):
        """Captura un frame i l'envia al servidor per analitzar emocions amb Gemini."""
        frame = self.camera.capture()
        _, jpeg = cv2.imencode(".jpg", frame)
        image_base64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")

        try:
            res = requests.post(
                f"https://{config.SERVER_IP}/api/deteccio-frame2",
                json={
                    "imatge": f"data:image/jpeg;base64,{image_base64}",
                    "mode": "emocions"
                }
                #cookies={"session": config.SESSION_TOKEN}
            )
            if res.ok:
                data = res.json()
                emocions = normalize_emocions(data.get('emocions', []))
                print(f"[HUMAN] Emocions detectades: {emocions}")
                print(f"[HUMAN] Anàlisi: {data.get('analisi', 'Cap')}")
                self.process_emocions(emocions)
                return {"emocions": emocions, "analisi": data.get('analisi', 'Cap')}
            else:
                print(f"[ERROR] No s'ha pogut fer l'anàlisi d’emocions: {res.status_code} - {res.text}")
                return {"emocions": [], "analisi": "Error"}
        except Exception as e:
            print(f"[ERROR] Fallo durant l'anàlisi d'emocions: {e}")
            return {"emocions": [], "analisi": "Error"}


def analitza_emocions(self):
        """
        Captura un frame i l'envia al servidor (mode únic deteccio-frames2).
        El servidor retorna percepció: llista de 'faces' amb emotion_human, attention, etc.
        Aquí triem la cara principal i apliquem process_emocions(emocions).
        """
        if not self.camera:
            print("[ERROR] Camera no disponible")
            return {"emocions": [], "analisi": "Error"}

        # 1) Captura i codifica
        frame = self.camera.capture()
        _, jpeg = cv2.imencode(".jpg", frame)
        image_base64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")

        # 2) Llista d’emocions permeses (del teu sistema STATES o custom)
        #    Si vols controlar l’ordre de preferència, ordena aquí.
        emotions_allowed = list(config.STATES.keys())
        # Aconsellat: limitar a les que detectes habitualment
        # emotions_allowed = ["happy","sad","angry","surprised","scared","disgusted","neutral","sleepy"]

        emotions_csv = ",".join(emotions_allowed)

        try:
            res = requests.post(
                f"https://{config.SERVER_IP}/api/deteccio-frames2",
                json={
                    "imatge": f"data:image/jpeg;base64,{image_base64}",
                    "emotions": emotions_csv
                },
                #timeout=8
                # cookies={"session": config.SESSION_TOKEN},
            )

            if not res.ok:
                print(f"[ERROR] Analisi HTTP {res.status_code}: {res.text}")
                return {"emocions": [], "analisi": "Error"}

            data = res.json()
            faces = data.get("faces", []) or []
            summary = data.get("summary", "Cap")

            # 3) Si el servidor ja ordena per focus_score, agafa la primera.
            #    Per robustesa, reordeno per focus_score si existeix; si no, ho deixo tal qual.
            if faces and "focus_score" in faces[0]:
                faces.sort(key=lambda f: f.get("focus_score", 0.0), reverse=True)

            # 4) Tria la cara objectiu
            target = faces[0] if faces else None

            if not target:
                # cap cara: emoció neutral per no fer res agressiu
                emocions = normalize_emocions(["neutral"])
                print(f"[HUMAN] Cap persona clara. Emocions: {emocions}")
                self.process_emocions(emocions)
                return {"emocions": emocions, "analisi": summary}

            # 5) Extreu emoció humana i normalitza
            human_emotion = target.get("emotion_human", "neutral")
            emocions = normalize_emocions([human_emotion])

            # (OPCIONALS per a futures accions locals del robot)
            attention = bool(target.get("attention", False))
            eye_contact = bool(target.get("eye_contact", False))
            distance_m = target.get("distance_m", None)
            gesture = target.get("hand_gesture", "unknown")
            aggression = bool(target.get("aggression_signals", False))
            engagement = float(target.get("engagement", 0.0) or 0.0)
            gaze_dir = target.get("gaze_dir", "unknown")
            head_pose = target.get("head_pose", {"yaw": 0.0, "pitch": 0.0, "roll": 0.0})

            print(f"[HUMAN] Face target → emotion: {human_emotion}, "
                  f"attention={attention}, eye={eye_contact}, dist={distance_m}, "
                  f"gesture={gesture}, aggression={aggression}, engagement={engagement}, "
                  f"gaze={gaze_dir}, head={head_pose}")

            # Aquí mantens tota la lògica d'accions al teu gust.
            # Exemple: pots fer servir distance_m per mantenir espai personal, etc.
            # if self.motors and isinstance(distance_m, (int, float)):
            #     if distance_m < 0.6: self.motors.backoff(0.2)
            #     elif distance_m > 2.5 and attention: self.motors.approach(0.5)

            # 6) Executa emoció (visual/sons) segons el teu mapeig actual
            self.process_emocions(emocions)
            return {"emocions": emocions, "analisi": summary}

        except Exception as e:
            print(f"[ERROR] Fallo durant l'anàlisi d'emocions: {e}")
            return {"emocions": [], "analisi": "Error"}