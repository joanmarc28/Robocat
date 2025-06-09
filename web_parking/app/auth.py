from fastapi import APIRouter, Response, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud_users import create_user
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from app.models import Usuari,Policia, Client
from app.session import create_session_cookie, get_user_from_cookie, clear_session_cookie
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
#Mail API 
import requests
from email.mime.text import MIMEText
import pickle
import os
import base64

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="app/templates")

# Configuració Gmail API
MAILGUN_DOMAIN = 'sandbox2ec3eca2b5c848e58adabcbf4537d632.mailgun.org'

# Carregar les variables del fitxer .env
load_dotenv()

# Agafar la clau de l’entorn
MAILGUN_API_KEY = os.getenv("GEMINI_API_KEY")
@router.post("/registre")
async def processar_registre(
    email: str = Form(...),
    password: str = Form(...),
    data_naixement: str = Form(...),
    ciutat: str = Form(...),
    pais: str = Form(...),
    es_policia: bool = Form(False),
    dni: str = Form(None),
    nom: str = Form(None),
    cognoms: str = Form(None),
    direccio: str = Form(None),
    codi_postal: str = Form(None),
    telefon: str = Form(None),
    placa: str = Form(None),
    db: Session = Depends(get_db)
):
    await create_user(
        db=db,
        email=email,
        password=pwd_context.hash(password),
        data_naixement=data_naixement,
        ciutat=ciutat,
        pais=pais,
        es_policia=es_policia,
        dni=dni,
        nom=nom,
        cognoms=cognoms,
        direccio=direccio,
        codi_postal=codi_postal,
        telefon=telefon,
        placa=placa
    )
    return RedirectResponse(url="/login", status_code=303)

@router.get("/login")
def parking(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@router.get("/registre")
def parking(request: Request):
    user_id = get_user_from_cookie(request)
    if user_id:
        return RedirectResponse(url="/welcome", status_code=303)

    return templates.TemplateResponse("registre.html", {
        "request": request
    })

@router.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Usuari).filter(Usuari.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return RedirectResponse(url="/login?error=1", status_code=303)
    
    session_cookie = create_session_cookie(user.id)
    response = RedirectResponse(url="/welcome", status_code=303)
    response.set_cookie(key="session", value=session_cookie, httponly=True)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    clear_session_cookie(response)
    return response

@router.post("/recuperar_contrasenya")
async def recover_password(email: str = Form(...)):
    try:
        recovery_link = f"https://robocat.jmprojects.cat/reset-password?email={email}"
        result = send_recovery_email(email, recovery_link)
        return RedirectResponse("/login?msg=recovery_sent", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviant correu: {e}")

@router.get("/recuperar_contrasenya", response_class=HTMLResponse)
def recuperar_contrasenya_form(request: Request):
    return templates.TemplateResponse("recuperar_contrasenya.html", {"request": request})

def send_recovery_email(to_email, recovery_link):
    subject = "Recuperació de contrasenya"
    text_content = f"""
    Hola,

    Has demanat recuperar la teva contrasenya. Fes clic al següent enllaç per reiniciar-la:
    {recovery_link}

    Si no ho has demanat, ignora aquest missatge.
    """

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Robocat <postmaster@{MAILGUN_DOMAIN}>",
            "to": to_email,
            "subject": subject,
            "text": text_content
        }
    )

    if response.status_code != 200:
        raise Exception(f"Mailgun error: {response.text}")

    return response.json()

@router.get("/perfil")
def welcome(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    policia = db.query(Policia).filter_by(user_id=user.id).first()
    client = db.query(Client).filter_by(user_id=user.id).first()

    if policia:
        return RedirectResponse(url="/welcome", status_code=303)

    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "client": client
    })
    

@router.post("/perfil/update")
def update_perfil(
    request: Request,
    email: str = Form(...),
    data_naixement: str = Form(...),
    ciutat: str = Form(...),
    pais: str = Form(None),
    nom: str = Form(...),
    cognoms: str = Form(None),
    direccio: str = Form(None),
    codi_postal: str = Form(None),
    telefon: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    if not user or not user.client:
        return RedirectResponse(url="/login", status_code=303)

    # Update Usuari
    user.email = email
    user.data_naixement = data_naixement
    user.ciutat = ciutat
    user.pais = pais

    # Update Client
    client = user.client
    client.nom = nom
    client.cognoms = cognoms
    client.direccio = direccio
    client.codi_postal = codi_postal
    client.telefon = telefon

    db.commit()
    return RedirectResponse(url="/perfil", status_code=303)
