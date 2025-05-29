from google.cloud import speech_v1p1beta1 as speech
import io
import os
import tempfile
import subprocess
from app.database import get_db
from fastapi import APIRouter, Request,UploadFile, File,Depends
from pydantic import BaseModel
import google.generativeai as genai

from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import texttospeech

from app.models import Cotxe, Estada
from app.session import get_user_from_cookie
from sqlalchemy.orm import Session
# Carregar les variables del fitxer .env
load_dotenv()

# Agafar la clau de l’entorn
api_key = os.getenv("GEMINI_API_KEY")

router = APIRouter()

class PreguntaModel(BaseModel):
    pregunta: str

# 🔑 Configura la clau d’API
genai.configure(api_key=api_key)

@router.post("/transcripcio")
async def transcripcio(audio: UploadFile = File(...)):
    client = speech.SpeechClient()

    # Guarda el .webm a fitxer temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_webm:
        temp_webm.write(await audio.read())
        temp_webm_path = temp_webm.name

    # Converteix a .wav LINEAR16 amb ffmpeg
    temp_wav_path = temp_webm_path.replace(".webm", ".wav")
    ffmpeg_cmd = [
        "ffmpeg", "-i", temp_webm_path, 
        "-ar", "16000", "-ac", "1", "-f", "wav", temp_wav_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    # Llegeix el fitxer wav convertit
    with open(temp_wav_path, "rb") as wav_file:
        audio_content = wav_file.read()

    # Configura Google Speech
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ca-ES"
    )

    # Envia a Google Cloud Speech
    response = client.recognize(config=config, audio=audio)

    resultat = ""
    for result in response.results:
        resultat += result.alternatives[0].transcript

    # Neteja fitxers temporals
    os.remove(temp_webm_path)
    os.remove(temp_wav_path)

    return {"transcripcio": resultat}


from fastapi.responses import JSONResponse
import base64
import io

@router.post("/assistente-gemini")
async def assistente_gemini(pregunta: PreguntaModel, db: Session = Depends(get_db)):
    resposta_text = None

    text = pregunta.pregunta.lower()
    if "quants cotxes" in text or "quants estacionats" in text:
        count = db.query(Estada).filter(Estada.activa == True).count()
        resposta_text = f"Tens {count} cotxe(s) aparcat(s) ara mateix."

    elif "quins models" in text or "quins cotxes" in text:
        cotxes = db.query(Cotxe).join(Estada).filter(Estada.activa == True).all()
        noms = [f"{c.marca} {c.model}" for c in cotxes]
        llista = ", ".join(noms) if noms else "Cap cotxe aparcat."
        resposta_text = f"Els models que tens ara mateix aparcats són: {llista}"

    elif "quins cotxes registrats" in text or "models registrats" in text:
        cotxes = db.query(Cotxe).all()
        noms = [f"{c.marca} {c.model}" for c in cotxes]
        llista = ", ".join(noms) if noms else "No tens cap cotxe registrat."
        resposta_text = f"Els cotxes registrats al teu compte són: {llista}"

    elif "quantes zones" in text or "quantes zones hi ha" in text:
        zones = db.query(Zona).count()
        resposta_text = f"Hi ha {zones} zona(es) disponibles."

    elif "quin és el meu nom" in text or "quin és el meu usuari" in text:
        user = db.query(Usuari).filter(Usuari.id == pregunta.user_id).first()
        resposta_text = f"El teu nom d’usuari és {user.nom}" if user else "No he pogut trobar el teu nom."

    else:
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
        ✅ Si vol fer una d’aquestes accions, respon exclusivament amb el LINK (per exemple: '/registre').
        ✅ No afegeixis cap explicació extra ni frase llarga, només escriu el link exacte.
        ✅ Si la pregunta no correspon a cap acció disponible, respon amb: "No puc ajudar-te amb això, torna a provar."

        Pregunta de l’usuari: {pregunta.pregunta}
        """
        response = model.generate_content(prompt)
        resposta_text = response.text.strip()

    # 🔥 Generem àudio
    audio_bytes = generar_audio(resposta_text)
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    return JSONResponse(content={
        "resposta": resposta_text,
        "audio": audio_base64
    })


def generar_audio(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ca-ES",  # català
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content
