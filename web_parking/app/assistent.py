from google.cloud import speech_v1p1beta1 as speech  #importem llibreria de reconeixement de veu
import io
import os
import tempfile
import subprocess
from app.database import get_db  #funcio per obtenir sessio de base de dades
from fastapi import APIRouter, Request, UploadFile, File, Depends  #importem fastapi
from pydantic import BaseModel  #per validar dades d'entrada
import google.generativeai as genai  #llibreria de gemini
from google.cloud import texttospeech  #per generar audio

from app.models import Cotxe, Estada  #models de la base de dades
from app.session import get_user_from_cookie  #per obtenir usuari des de cookies
from sqlalchemy.orm import Session  #sessio per a consultes ORM

from dotenv import load_dotenv  #per carregar variables d'entorn
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

from fastapi.responses import JSONResponse  #per retornar resposta json
from app.models import Cotxe, Estada, Usuari, Zona  #models
import base64
import io

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
