from interface.display import clear_displays, displays_show_frames
from interface.speaker import Speaker
import config
import time
from vision.camera import RobotCamera
import threading
import base64
import json
import re
import google.generativeai as genai

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

        # Funció per parlar en un fil separat
        def speak():
            self.speaker.say_emotion(emotion)

        # Inicia el fil de veu
        t_speak = threading.Thread(target=speak)
        t_speak.start()

        # Mostra l'emoció mentre el fil de veu està funcionant
        t_inici = time.time()
        while time.time() - t_inici < duration:
            displays_show_frames(emotion)

        # Espera que el fil acabi per si no ha acabat encara
        t_speak.join()
        clear_displays()
    """import base64
    import json
    import re
    import google.generativeai as genai

    # Assegura't que la API key ja estigui configurada
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def detectar_emocions_gemini(frame_rgb):
        _, jpeg = cv2.imencode(".jpg", frame_rgb)
        image_bytes = jpeg.tobytes()

        prompt = (
            "Analitza aquesta imatge d’un vídeo. "
            "Detecta emocions de les persones. "
            "Retorna un JSON amb 'emocions' (llista) i 'analisi' (descripció breu sense accents)."
        )

        model = genai.GenerativeModel('gemini-2.0-flash-lite')

        resposta = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])

        text = resposta.text.strip()

        if text.startswith("```"):
            text = re.sub(r"```[a-zA-Z]*", "", text).replace("```", "").strip()

        try:
            data = json.loads(text)
        except Exception as e:
            print("❌ Error parsejant JSON:", e)
            return {"emocions": [], "analisi": "Error"}

        return {
            "emocions": data.get("emocions", []),
            "analisi": data.get("analisi", "Cap")
        }"""
