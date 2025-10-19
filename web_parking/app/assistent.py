from google.cloud import speech_v1p1beta1 as speech  #importem llibreria de reconeixement de veu
import io
import os
import tempfile
import subprocess
from app.database import get_db  #funcio per obtenir sessio de base de dades
from fastapi import APIRouter, Request, UploadFile, File, Depends,HTTPException  #importem fastapi
from pydantic import BaseModel  #per validar dades d'entrada
import google.generativeai as genai  #llibreria de gemini
from google.cloud import texttospeech  #per generar audio
from fastapi.responses import JSONResponse  #per retornar resposta json
import base64
from app.models import Cotxe, Estada, Usuari, Zona, PossibleInfraccio   #models de la base de dades
from app.session import get_user_from_cookie  #per obtenir usuari des de cookies
from sqlalchemy.orm import Session  #sessio per a consultes ORM
from dotenv import load_dotenv  #per carregar variables d'entorn
from datetime import datetime, timezone
import uuid
import json
import re
from typing import Optional, List, Dict, Any

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")  #clau de gemini des del .env

router = APIRouter()  #creem router de fastapi

class PreguntaModel(BaseModel):  #model per rebre preguntes
    pregunta: str

genai.configure(api_key=api_key)  #configurem gemini amb la clau

@router.post("/transcripcio")  #endpoint per transcripcio de veu
async def transcripcio(audio: UploadFile = File(...)):
    client = speech.SpeechClient()  #creem client de reconeixement

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_webm:  #guardem arxiu rebut com a fitxer temporal
        temp_webm.write(await audio.read())
        temp_webm_path = temp_webm.name

    temp_wav_path = temp_webm_path.replace(".webm", ".wav")  #preparem ruta per convertir a wav
    ffmpeg_cmd = [  #comanda per convertir audio amb ffmpeg
        "ffmpeg", "-i", temp_webm_path,
        "-ar", "16000", "-ac", "1", "-f", "wav", temp_wav_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)  #executem conversio

    with open(temp_wav_path, "rb") as wav_file:  #llegim arxiu wav
        audio_content = wav_file.read()

    audio = speech.RecognitionAudio(content=audio_content)  #preparem audio per reconeixer
    config = speech.RecognitionConfig(  #config del reconeixement
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ca-ES"
    )

    response = client.recognize(config=config, audio=audio)  #fem reconeixement

    resultat = ""
    for result in response.results:  #concatenem resultats
        resultat += result.alternatives[0].transcript

    os.remove(temp_webm_path)  #esborrem fitxers temporals
    os.remove(temp_wav_path)

    return {"transcripcio": resultat}  #retornem transcripcio


@router.post("/assistente-gemini")  #endpoint per xat amb assistent
async def assistente_gemini(pregunta: PreguntaModel, db: Session = Depends(get_db)):
    resposta_text = None
    text = pregunta.pregunta.lower()  #passem pregunta a minuscules

    if "quants estacionats" in text:  #cas: contar cotxes actius
        count = db.query(Estada).filter(Estada.activa == True).count()
        resposta_text = f"Tens {count} cotxe(s) aparcat(s) ara mateix."

    elif "quins models" in text:  #cas: mostrar models actius
        cotxes = db.query(Cotxe).join(Estada).filter(Estada.activa == True).all()
        noms = [f"{c.marca} {c.model}" for c in cotxes]
        llista = ", ".join(noms) if noms else "Cap cotxe aparcat."
        resposta_text = f"Els models que tens ara mateix aparcats són: {llista}"

    elif "quins cotxes" in text or "models registrats" in text:  #cas: mostrar tots els cotxes de l'usuari
        cotxes = db.query(Cotxe).filter(Cotxe.usuari_id == Usuari.id).all()
        noms = [f"{c.marca} {c.model}" for c in cotxes]
        llista = ", ".join(noms) if noms else "No tens cap cotxe registrat."
        resposta_text = f"Els cotxes registrats al teu compte són: {llista}"

    elif "quantes zones" in text or "quantes zones hi ha" in text:  #cas: contar zones disponibles
        zones = db.query(Zona).count()
        resposta_text = f"Hi ha {zones} zona(es) disponibles."

    elif "quin és el meu nom" in text or "quin és el meu usuari" in text:  #cas: obtenir nom d'usuari
        user = db.query(Usuari).filter(Usuari.id == pregunta.user_id).first()
        resposta_text = f"El teu nom d’usuari és {user.nom}" if user else "No he pogut trobar el teu nom."

    else:  #qualsevol altre pregunta es gestiona amb gemini
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        prompt = f"""
        Ets un assistent per la web Robocat. Les funcionalitats disponibles són:

        🔹 /registre → Registrar un compte nou
        🔹 /login → Entrar al sistema
        🔹 /perfil → Veure el perfil de l’usuari
        🔹 /historial → Consultar l’historial d’estacionaments
        🔹 /cars → Consultar o registrar un nou cotxe
        🔹 /parking → Registrar un nou aparcament
        🔹 /welcome → Tornar a la pàgina principal
        🔹 /zones → Editar les zones blaves
        🔹 /logout → Tancar la sessió

        Quan l’usuari et pregunta:
        - Si vol fer una d’aquestes accions, respon exclusivament amb el LINK (per exemple: '/registre').
        - No afegeixis cap explicacio extra ni frase llarga, només escriu el link exacte.
        - Si la pregunta no correspon a cap accio disponible, respon amb: "No puc ajudar-te amb això, torna a provar."

        Pregunta de l’usuari: {pregunta.pregunta}
        """
        response = model.generate_content(prompt)
        resposta_text = response.text.strip()

    audio_bytes = generar_audio(resposta_text)  #generem audio de la resposta
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')  #convertim a base64

    return JSONResponse(content={  #retornem resposta i audio
        "resposta": resposta_text,
        "audio": audio_base64
    })

def generar_audio(text):  #funcio per convertir text a veu
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(  #configuracio de la veu
        language_code="ca-ES",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(  #configuracio de sortida
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(  #generem l'audio
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content  #retornem audio


class FrameModel(BaseModel):
    imatge: str
    mode: str  # L'afegim perquè JS l'envia per JSON body

@router.post("/api/deteccio-frame")
async def deteccio_frame(request: Request, frame: FrameModel, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        #return {"error": "No autenticat"}
        print(f"No autenticat: Mode poc Segur")

    mode = frame.mode or "emocions"
    print(f"📷 Mode seleccionat: {mode}")

    try:
        imatge_base64 = frame.imatge.split(",")[1]
        image_bytes = base64.b64decode(imatge_base64)
    except Exception as e:
        print("❌ Error en decodificar la imatge:", e)
        return {"error": "Error en decodificar la imatge"}

    if mode == "emocions":
        prompt = (
            "Analitza aquesta imatge d’un vídeo. "
            "Detecta emocions de les persones. "
            "Retorna un JSON amb 'emocions' (llista) i 'analisi' (descripció breu sense accents)."
        )
    else:
        prompt = (
            "Analitza aquesta imatge d’un vídeo. "
            "Detecta matrícules de cotxes, identifica vehicles i descriu qualsevol infracció de trànsit. "
            "Retorna un JSON amb 'matricules' (llista) i 'infraccio' (comença amb si, no o possible i després una descripció breu sense accents)."
        )

    print(f"🧠 Prompt enviat a Gemini:\n{prompt}")

    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    resposta = model.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": image_bytes}
    ])

    text = resposta.text.strip()
    print("📨 Resposta crua de Gemini:")
    print(text)

    # 🔧 Netegem si ve amb triple backticks
    if text.startswith("```"):
        text = re.sub(r"```[a-zA-Z]*", "", text)  # Elimina ```json o ``` qualsevol format
        text = text.replace("```", "").strip()

    try:
        data = json.loads(text)
    except Exception as e:
        print("❌ Error parsejant JSON:", e)
        return {"error": "Error en el format de resposta de Gemini"}

    print("✅ JSON deserialitzat correctament:")
    print(data)

    if mode == "emocions":
        return {
            "emocions": data.get("emocions", []),
            "analisi": data.get("analisi", "Cap")
        }

    else:
        matricules = data.get("matricules", [])
        infraccio = data.get("infraccio", "Cap")

        if matricules and infraccio:
            nova = PossibleInfraccio(
                id=f"pos_{datetime.utcnow().isoformat()}",
                descripcio=infraccio,
                matricula_cotxe=matricules[0],
                data_posinfraccio=datetime.utcnow(),
                imatge=frame.imatge
            )
            db.add(nova)
            db.commit()

        return {
            "matricules": matricules,
            "infraccio": infraccio or "Cap"
        }
    

# ---------- Model ----------
class FrameModel2(BaseModel):
    imatge: str
    emotions: str  # CSV: "happy,sad,angry,neutral"

# ---------- Helpers ----------
def _parse_emotions_csv(csv_text: Optional[str]) -> List[str]:
    if not csv_text:
        return []
    return [e.strip() for e in csv_text.split(",") if e.strip()]

def _clean_llm_json(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        t = re.sub(r"```[a-zA-Z]*", "", t)
        t = t.replace("```", "").strip()
    if not (t.startswith("{") and t.endswith("}")):
        m = re.search(r"\{[\s\S]*\}$", t)
        if m:
            t = m.group(0)
    return t

def _coerce_emocio(emocio_model: str, permeses: List[str]) -> str:
    if not emocio_model:
        return permeses[0] if permeses else "neutral"
    if not permeses:
        return emocio_model
    low = {e.lower(): e for e in permeses}
    return low.get(emocio_model.lower(), permeses[0])

def _compute_focus_score(face: Dict[str, Any]) -> float:
    attention = 1.0 if face.get("attention") else 0.0
    eye = 1.0 if face.get("eye_contact") else 0.0
    engagement = float(face.get("engagement", 0.0) or 0.0)
    gaze_dir = face.get("gaze_dir", "unknown")
    gaze_bonus = 0.2 if gaze_dir in ("towards", "unknown") else 0.0
    score = 0.45*attention + 0.35*eye + 0.20*engagement + gaze_bonus
    return max(0.0, min(1.0, score))

def _build_prompt(emocions_permeses: List[str]) -> str:
    llista = ", ".join(emocions_permeses) if emocions_permeses else \
             "happy, sad, angry, surprised, disgusted, scared, neutral"
    return (
        "Analitza aquesta imatge d’un vídeo per ajudar un robot social a comprendre l'estat emocional i atencional de les persones.\n"
        "Detecta quantes cares hi ha i retorna un JSON estructurat amb:\n"
        " - 'num_faces': nombre de persones.\n"
        " - 'faces': llista amb camps per cada persona: attention, eye_contact, head_pose, gaze_dir, distance_m, hand_gesture, posture, aggression_signals, engagement, emotion_human (només una de la llista permesa), conf_emotion, bbox.\n"
        " - 'scene': crowd_level i lighting.\n"
        " - 'summary': breu descripcio sense accents.\n"
        "Només retorna JSON, sense text addicional ni markdown.\n"
        f"Les emocions permeses són: [{llista}]."
    )

# ---------- RUTA ÚNICA ----------
@router.post("/api/deteccio-frames2")
async def deteccio_frames2(request: Request, frame: FrameModel2, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        print("⚠️ Mode poc segur: sense autenticació")

    try:
        imatge_base64 = frame.imatge.split(",")[1]
        image_bytes = base64.b64decode(imatge_base64)
    except Exception as e:
        print("❌ Error decodificant imatge:", e)
        return {"error": "Error en decodificar la imatge"}

    emocions_permeses = _parse_emotions_csv(frame.emotions) or \
        ["happy", "sad", "angry", "surprised", "scared", "neutral"]
    prompt = _build_prompt(emocions_permeses)

    print(f"🧠 Prompt enviat a Gemini:\n{prompt}\n")

    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    resposta = model.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": image_bytes}
    ])

    text = _clean_llm_json(resposta.text or "")
    print("📨 Resposta crua Gemini:")
    print(text)

    try:
        data = json.loads(text)
    except Exception as e:
        print("❌ Error parsejant JSON:", e)
        return {"error": "Error en el format de resposta de Gemini"}

    faces = data.get("faces", []) or []
    for f in faces:
        f["emotion_human"] = _coerce_emocio(f.get("emotion_human", "neutral"), emocions_permeses)
        f["focus_score"] = _compute_focus_score(f)

    faces.sort(key=lambda f: f.get("focus_score", 0.0), reverse=True)

    result = {
        "version": "web-perception-1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "num_faces": data.get("num_faces", len(faces)),
        "faces": faces,
        "scene": data.get("scene", {"crowd_level": "unknown", "lighting": "unknown"}),
        "summary": data.get("summary", "Cap"),
    }

    print("✅ Dades processades correctament.")
    return result