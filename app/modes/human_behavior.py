import os
import time
import threading
import base64
import json
import cv2
import requests
import time
from typing import Any, Dict, List, Tuple, TypedDict

from movement.motors import EstructuraPotes
from interface.display import clear_displays, displays_show_frames
from interface.speaker import Speaker
from vision.camera import RobotCamera
import config
from utils.helpers import normalize_emocions
from movement.simulation_data import *

class HumanBehavior:
    def __init__(self, speaker: Speaker = None, camera: RobotCamera = None, motors:EstructuraPotes=None):
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

    def determine_reaction(self, human_emotion: str, context: Dict) -> Tuple[str, List[Any]]:
        """Decideix l'emoció i les accions del gat segons l'estat humà."""
        human_emotion = human_emotion or "default"
        context = context or {}
        aggression = bool(context.get("aggression", False))
        attention = bool(context.get("attention", False))
        eye_contact = bool(context.get("eye_contact", False))
        engagement = float(context.get("engagement", 0.0) or 0.0)
        gesture = (context.get("gesture") or "unknown").lower()
        distance = context.get("distance_m")

        actions: List[Any] = []

        # Situacions de tensió o agressió
        if aggression:
            #if distance is None or distance < 0.8:
                #    actions.append(deepcopy(SEQUENCE_LIBRARY["step_back"]))
            return "scared", actions

        if isinstance(distance, (int, float)) and distance < 0.4:
            #actions.append(deepcopy(SEQUENCE_LIBRARY["step_back"]))
            return "surprised", actions

        if human_emotion == "angry":
            actions.append("body_downward")
            return "surprised", actions

        if human_emotion == "disgusted":
            return "angry", actions

        if human_emotion == "scared":
            return "surprised", actions

        # Gestos o actituds amigables
        friendly_gestures = {"wave", "thumbs_up", "ok", "open_hand", "peace"}
        if gesture in friendly_gestures or (human_emotion in {"happy", "surprised"} and attention and engagement > 0.6):
            self.motors.follow_sequance(maneta_states, cycles=6, t=0.8)
            return "happy", actions

        if human_emotion == "sad":
            actions.append("body_upward")
            return "happy", actions

        head_pose = context.get("head_pose") or {}
        pitch = float(head_pose.get("pitch", 0.0) or 0.0)
        yaw = float(head_pose.get("yaw", 0.0) or 0.0)

        if attention and eye_contact:
            if abs(pitch) > 20 or abs(yaw) > 25:
                # Persona inclinada a prop → el gat es prepara per interactuar
                #actions.append(deepcopy(SEQUENCE_LIBRARY["sit_soft"]))
                self.motors.set_position("sit")
                return "surprised", actions
            return "surprised", actions

        return "default", actions

    def react_to_context(self, human_emotion: str, context: Dict | None = None) -> str:
        """Calcula i executa la resposta del gat a partir del context humà."""
        cat_emotion, actions = self.determine_reaction(human_emotion, context or {})
        self.express_emotion(cat_emotion)
        self.perform_actions(actions)
        return cat_emotion

    # ------------------------------------------------------------------
    # Compatibilitat amb lògica antiga basada en emocions simples
    # ------------------------------------------------------------------
    def process_emocions(self, emocions: List[str]) -> str | None:
        """Manté compatibilitat amb el flux antic que només passava emocions."""
        if not emocions:
            return None

        human_emotion = emocions[0]
        return self.react_to_context(human_emotion, {})

    # ------------------------------------------------------------------
    # Obtenció i anàlisi de dades del servidor
    # ------------------------------------------------------------------
    def analitza_emocions(self) -> Dict:
        """
        Captura un frame i l'envia al servidor (mode únic deteccio-frames2).
        El servidor retorna percepció: llista de 'faces' amb emotion_human, attention, etc.
        Aquí triem la cara principal i apliquem process_emocions(emocions).
        """
        if not self.camera:
            print("[ERROR] Càmera no disponible")
            return {"emocions": [], "analisi": "Error", "reaccio": "default", "context": {}}

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
                json={"imatge": f"data:image/jpeg;base64,{image_base64}", "emotions": emotions_csv},
            )
        except Exception as exc:
            print(f"[ERROR] Fallo durant l'anàlisi d'emocions: {exc}")
            return {"emocions": [], "analisi": "Error", "reaccio": "default", "context": {}}

        if not res.ok:
            print(f"[ERROR] Analisi HTTP {res.status_code}: {res.text}")
            return {"emocions": [], "analisi": "Error", "reaccio": "default", "context": {}}

        data = res.json()
        faces = data.get("faces", []) or []
        summary = data.get("summary", "Cap")

        if faces and "focus_score" in faces[0]:
            faces.sort(key=lambda f: f.get("focus_score", 0.0), reverse=True)

        target = faces[0] if faces else None

        if not target:
            emocions = normalize_emocions(["default"])
            cat_emotion = self.react_to_context(emocions[0], {})
            print(f"[HUMAN] Cap persona clara. Emoció gat: {cat_emotion}")
            return {"emocions": emocions, "analisi": summary, "reaccio": cat_emotion, "context": {}}

        human_emotion_raw = target.get("emotion_human", "default")
        emocions = normalize_emocions([human_emotion_raw])
        human_emotion = emocions[0]

        context = {
            "attention": bool(target.get("attention", False)),
            "eye_contact": bool(target.get("eye_contact", False)),
            "distance_m": target.get("distance_m"),
            "gesture": target.get("hand_gesture", "unknown"),
            "aggression": bool(target.get("aggression_signals", False)),
            "engagement": float(target.get("engagement", 0.0) or 0.0),
            "gaze": target.get("gaze_dir", "unknown"),
            "head_pose": target.get("head_pose", {}),
        }

        print(
            "[HUMAN] Face target → emotion: {emotion}, attention={attention}, eye={eye}, dist={dist}, "
            "gesture={gesture}, aggression={aggression}, engagement={engagement}"
            .format(
                emotion=human_emotion,
                attention=context["attention"],
                eye=context["eye_contact"],
                dist=context["distance_m"],
                gesture=context["gesture"],
                aggression=context["aggression"],
                engagement=context["engagement"],
            )
        )

        cat_emotion = self.react_to_context(human_emotion, context)
        return {
            "emocions": emocions,
            "analisi": summary,
            "reaccio": cat_emotion,
            "context": context,
        }    
