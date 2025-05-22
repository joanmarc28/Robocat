from fastapi import FastAPI, Request, Depends, Form, Response
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
from app import auth
from app.database import Base, engine
from app.session import get_user_from_cookie
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Usuari

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/robocat-user-app-5d2b35bd5c22.json"

Base.metadata.create_all(bind=engine)

# Importa i registra rutes de auth
app.include_router(auth.router)

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
        })

    # Si està loguejat, redirigeix a welcome
    return RedirectResponse(url="/welcome", status_code=303)

@app.get("/welcome")
def welcome(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    return templates.TemplateResponse("welcome.html", {
        "request": request,
        "user": user
    })

@app.get("/parking")
def parking(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_from_cookie(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(Usuari).get(user_id)
    return templates.TemplateResponse("parking.html", {
        "request": request,
        "user": user
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

@app.get("/historial")
def historial(request: Request):
    return templates.TemplateResponse("historial.html", {
        "request": request
    })

@app.get("/paymentzones")
def paymentzones(request: Request):
    return templates.TemplateResponse("paymentzones.html", {
        "request": request
    })

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
    })
@app.get("/perfil")
def parking(request: Request):
    return templates.TemplateResponse("perfil.html", {
        "request": request
    })

@app.get("/mapa")
def parking(request: Request):
    return templates.TemplateResponse("mapa.html", {
        "request": request,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

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
