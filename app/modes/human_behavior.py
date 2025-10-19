import os
import time
import threading
import base64
import json
import cv2
import requests
from typing import Any, Dict, List, Tuple

from movement.motors import EstructuraPotes
from interface.display import clear_displays, displays_show_frames
from interface.speaker import Speaker
from vision.camera import RobotCamera
import config
from utils.helpers import normalize_emocions
from movement.simulation_data import *

# --- helpers de coerció (eviten 500 i sorpreses del LLM) ---
def _to_bool(x) -> bool:
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    s = str(x).strip().lower()
    return s in {"true", "1", "yes", "si", "sí", "y", "t", "on"}

def _to_float01(x) -> float:
    try:
        if isinstance(x, (int, float)):
            v = float(x)
        else:
            s = str(x).strip().lower()
            if s.endswith("%"):
                v = float(s[:-1]) / 100.0
            elif s in {"none", "null", ""}:
                v = 0.0
            elif s in {"low", "baixa"}:
                v = 0.2
            elif s in {"medium", "mitjana"}:
                v = 0.5
            elif s in {"high", "alta"}:
                v = 0.8
            else:
                v = float(s)
    except Exception:
        v = 0.0
    return max(0.0, min(1.0, v))

class HumanBehavior:
    def __init__(self, speaker: Speaker = None, camera: RobotCamera = None, motors:EstructuraPotes=None):
        self.speaker = speaker
        self.camera = camera
        self.motors = motors
        
        
    def express_emotion(self, emotion, duration=3):
        if emotion not in config.STATES:
            print(f"[HUMAN] Emoció desconeguda: {emotion}")
            return
        # Si no hi ha altaveu, igualment mostrem ulls; no sortim.
        t_inici = time.time()
        while time.time() - t_inici < duration:
            displays_show_frames(emotion)
            time.sleep(0.03)  # cedeix CPU

    def determine_reaction(self, human_emotion: str, context: Dict) -> Tuple[str, List[Any]]:
        """Decideix l'emoció i les accions del gat segons l'estat humà."""
        human_emotion = human_emotion or "default"
        context = context or {}

        # Coercions robustes
        attention = _to_bool(context.get("attention"))
        eye_contact = _to_bool(context.get("eye_contact"))
        engagement = _to_float01(context.get("engagement"))
        gesture = (context.get("gesture") or "unknown").lower()
        distance = context.get("distance_m")

        # "aggression_signals" del LLM sol ser string ("none", "fist", ...).
        aggr_raw = (context.get("aggression") or context.get("aggression_signals") or "").strip().lower()
        aggression = aggr_raw not in {"", "none", "no", "false"}

        # Situacions de tensió o agressió
        if aggression:
            #if distance is None or distance < 0.8:
                #    actions.append(deepcopy(SEQUENCE_LIBRARY["step_back"]))
            return "scared"

        if isinstance(distance, (int, float)) and distance < 0.4:
            #actions.append(deepcopy(SEQUENCE_LIBRARY["step_back"]))
            return "surprised"

        if human_emotion == "angry":
            #actions.append("body_downward")
            self.motors.set_position("up")
            return "surprised"

        if human_emotion == "disgusted":
            return "angry"

        if human_emotion == "scared":
            return "surprised"

        # Gestos o actituds amigables
        friendly_gestures = {"wave", "thumbs_up", "ok", "open_hand", "peace"}
        if gesture in friendly_gestures or (human_emotion in {"happy", "surprised"} and attention and engagement > 0.6):
            self.motors.follow_sequance(maneta_states, cycles=6, t=0.8)
            return "happy"

        if human_emotion == "sad":
            #actions.append("body_upward")
            return "happy"

        head_pose = context.get("head_pose") or {}
        pitch = _to_float01(head_pose.get("pitch")) * 100  # si ve 0..1, escalam a graus
        yaw = _to_float01(head_pose.get("yaw")) * 100

        if attention and eye_contact:
            if abs(pitch) > 20 or abs(yaw) > 25:
                # Persona inclinada a prop → el gat es prepara per interactuar
                #actions.append(deepcopy(SEQUENCE_LIBRARY["sit_soft"]))
                self.motors.set_position("sit")
                return "surprised"
            return "surprised"

        return "default"

    def react_to_context(self, human_emotion: str, context: Dict | None = None) -> str:
        """Calcula i executa la resposta del gat a partir del context humà."""
        cat_emotion = self.determine_reaction(human_emotion, context or {})
        self.express_emotion(cat_emotion)
        return cat_emotion

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
        emotions_allowed = list(config.STATES.keys())
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
            "attention": _to_bool(target.get("attention", False)),
            "eye_contact": _to_bool(target.get("eye_contact", False)),
            "distance_m": target.get("distance_m"),
            "gesture": target.get("hand_gesture", "unknown"),
            "aggression": target.get("aggression_signals", "none"),
            "engagement": _to_float01(target.get("engagement", 0.0)),
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
