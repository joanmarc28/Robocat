from fastapi import FastAPI, Request, Depends, Form, Response, HTTPException
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form, Request
from fastapi.responses import RedirectResponse
import json
from google.cloud import vision
import base64
import io
from fastapi.responses import JSONResponse
import requests
from passlib.context import CryptContext
from app import auth, zones, cars, assistent
from app.database import Base, engine
from app.session import get_user_from_cookie
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Usuari,Policia, Client, Cotxe, Estada, Zona
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Carrega les variables d'entorn des del fitxer .env
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/robocat-user-app-5d2b35bd5c22.json"

# Configuració de la base de dades
Base.metadata.create_all(bind=engine)

# Importa i registra rutes de auth
app.include_router(auth.router)
app.include_router(zones.router)
app.include_router(cars.router)
app.include_router(assistent.router)

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user_id": user_id,
            "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
        })

    # Si està loguejat, redirigeix a welcome
    return RedirectResponse(url="/welcome", status_code=303)

"""@app.get("/welcome")
def welcome(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    role = "client"
    if db.query(Policia).filter_by(user_id=user.id).first():
        role = "policia"

    return templates.TemplateResponse("welcome.html", {
        "request": request,
        "user_id": user_id,
        "role": role,
        "user": user
    })"""

@app.get("/welcome")
def welcome(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    role = "client"
    if db.query(Policia).filter_by(user_id=user.id).first():
        role = "policia"

    estada_activa = None
    if role == "client":
        estada_activa = db.query(Estada).filter_by(dni_usuari=user.client.dni, activa=True).first()

    return templates.TemplateResponse("welcome.html", {
        "request": request,
        "user_id": user_id,
        "role": role,
        "user": user,
        "estada_activa": estada_activa,
        "datetime": datetime  # 👉 afegim el mòdul aquí!
    })

@app.get("/parking")
def parking(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    client = db.query(Client).filter_by(user_id=user.id).first()
    if not client:
        return RedirectResponse(url="/welcome", status_code=303)

    any_actual = datetime.now().year

    return templates.TemplateResponse("parking.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "client": client,
        "any_actual": any_actual,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

@app.get("/zones")
def parking(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    if db.query(Client).filter_by(user_id=user.id).first():
        return RedirectResponse(url="/welcome", status_code=303)

    role = "policia"
    return templates.TemplateResponse("zones.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "role": role,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

"""
@app.get("/cars")
def cars(request: Request):
    plate = "1234ABC"
    model = "Prius"
    brand = "Toyota"
    year = 2003
    color = "Blue"
    # Aquí podries fer una consulta a la base de dades per obtenir la matrícula i el model
    image_link = cercar_imatges(brand+" "+model+" "+color+" "+str(year))

    return templates.TemplateResponse("cars.html", {
        "request": request,
        "plate": plate,
        "model": model,
        "year": 2020,
        "color": color,
        "brand": brand,
        "fuel": "diesel",
        "dgt": "b",
        "image_car": image_link
    })"""

@app.get("/cars")
def cars(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    if db.query(Policia).filter_by(user_id=user.id).first():
        return RedirectResponse(url="/welcome", status_code=303)


    client = db.query(Client).filter_by(user_id=user.id).first()

    cotxes = []
    print(f"Client: {client}")
    print(f"Cotxes del client: {client.cotxes}")
    for cotxe in client.cotxes:
        image_link = cercar_imatges(f"{cotxe.marca} {cotxe.model} {cotxe.color} {cotxe.any_matriculacio}")
        cotxes.append({
            "matricula": cotxe.matricula,
            "model": cotxe.model,
            "marca": cotxe.marca,
            "any": cotxe.any_matriculacio,
            "color": cotxe.color,
            "combustible": cotxe.combustible,
            "dgt": cotxe.dgt,
            "image_car": image_link
        })

    return templates.TemplateResponse("cars.html", {
        "request": request,
        "user_id": user_id,
        "user": user,
        "client": client,
        "cotxes": cotxes
    })


@app.post("/extract-plate")
async def analitzar_matricula(capturedImage: str = Form(...)):
    try:
        image_data = base64.b64decode(capturedImage.split(",")[1])
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_data)
        response = client.text_detection(image=image)

        texts = response.text_annotations
        if texts:
            text_detected = texts[0].description.strip().replace("\n", "")
        else:
            text_detected = ""

        return JSONResponse(content={"plate": text_detected})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def cercar_imatges(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'cx': os.getenv("CSE_ID"),
        'key': os.getenv("API_KEY"),
        'searchType': 'image',
        'num': 1
    }
    print(f"Buscant: {query}")
    response = requests.get(url, params=params)
    print("URL final:", response.url)
    print("Codi resposta:", response.status_code)
    print("Resposta:", response.text)

    if response.status_code == 200:
        resultats = response.json().get('items', [])
        return resultats[0]['link'] if resultats else None
    return None


@app.get("/historial")
def veure_historial(request: Request, db: Session = Depends(get_db)):

    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    usuari = db.query(Usuari).get(user_id)
    if db.query(Policia).filter_by(user_id=usuari.id).first():
        return RedirectResponse(url="/welcome", status_code=303)

    estades = db.query(Estada).filter(Estada.dni_usuari == usuari.client.dni).all()
    client = db.query(Client).filter_by(user_id=usuari.id).first()

    dades = []
    for estada in estades:
        zona = db.query(Zona).filter(Zona.id == estada.id_zona).first()
        cotxe = db.query(Cotxe).filter_by(matricula=estada.matricula_cotxe).first()
        image_link = cercar_imatges(f"{cotxe.marca} {cotxe.model} {cotxe.color} {cotxe.any_matriculacio}")

        dades.append({
            "id": estada.id,
            "data_inici": estada.data_inici,
            "data_final": estada.data_final,
            "matricula": estada.matricula_cotxe,
            "zona": zona.tipus,
            "carrer": zona.carrer,
            "ciutat": zona.ciutat,
            "preu": estada.preu,
            "activa": estada.activa,
            "image_car": image_link
        })
    dades.reverse()

    return templates.TemplateResponse("historial.html", {
        "request": request,
        "estades": dades,
        "user_id": user_id,
        "user": usuari,
        "client": client
    })

@app.post("/finalitzar-estada")
async def finalitzar_estada(estada_id: int = Form(...), db: Session = Depends(get_db)):
    estada = db.query(Estada).filter(Estada.id == estada_id).first()
    if not estada:
        raise HTTPException(status_code=404, detail="Estada no trobada")

    estada.activa = False
    db.commit()

    return RedirectResponse(url="/historial", status_code=303)


"""
@app.post("/guardar-zona")
async def guardar_zona(nom: str = Form(...), coords: str = Form(...)):
    zona = {
        "nom": nom,
        "coordenades": json.loads(coords)
    }
    # ⚠️ Per ara, ho guardem a fitxer (pots canviar per PostgreSQL després)
    with open("zones.json", "a") as f:
        f.write(json.dumps(zona) + "\n")

    return RedirectResponse(url="/mapa", status_code=303)
"""

