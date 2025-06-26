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

class HumanBehavior:
    def __init__(self, speaker: Speaker = None, camera: RobotCamera = None):
        self.speaker = speaker
        self.camera = camera

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

    def analitza_emocions(self):
        """Captura un frame i l'envia al servidor per analitzar emocions amb Gemini."""
        frame = self.camera.capture()
        _, jpeg = cv2.imencode(".jpg", frame)
        image_base64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")

        try:
            res = requests.post(
                f"https://{config.SERVER_IP}/api/deteccio-frame",
                json={
                    "imatge": f"data:image/jpeg;base64,{image_base64}",
                    "mode": "emocions"
                }
                #cookies={"session": config.SESSION_TOKEN}
            )
            if res.ok:
                data = res.json()
                print(f"[HUMAN] Emocions detectades: {data.get('emocions', [])}")
                print(f"[HUMAN] Anàlisi: {data.get('analisi', 'Cap')}")
                return data
            else:
                print(f"[ERROR] No s'ha pogut fer l'anàlisi d’emocions: {res.status_code} - {res.text}")
                return {"emocions": [], "analisi": "Error"}
        except Exception as e:
            print(f"[ERROR] Fallo durant l'anàlisi d'emocions: {e}")
            return {"emocions": [], "analisi": "Error"}
