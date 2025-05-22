# ~/web-robocat/main.py
from fastapi import FastAPI, Request
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

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/robocat-user-app-5d2b35bd5c22.json"

@app.get("/")
def home(request: Request):
    usuari = {"nom": "Joan Marc"}
    return templates.TemplateResponse("index.html", {
        "request": request,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

@app.get("/login")
def parking(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@app.get("/registre")
def parking(request: Request):
    return templates.TemplateResponse("registre.html", {
        "request": request
    })

@app.get("/welcome")
def parking(request: Request):
    return templates.TemplateResponse("welcome.html", {
        "request": request
    })
@app.get("/parking")
def parking(request: Request):
    return templates.TemplateResponse("parking.html", {
        "request": request
    })
"""
@app.post("/parking-data", response_class=HTMLResponse)
async def parking(request: Request, plate: str = Form(...), model: str = Form(...), capturedImage: str = Form(None)):
    text_detected = "No s'ha detectat text"
    
    if capturedImage:
        image_data = base64.b64decode(capturedImage.split(",")[1])
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_data)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            text_detected = texts[0].description.strip()

    return templates.TemplateResponse("resultat.html", {
        "request": request,
        "plate": plate,
        "model": model,
        "text_detectat": text_detected
    })
"""
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
def parking(request: Request):
    return templates.TemplateResponse("historial.html", {
        "request": request
    })

@app.get("/paymentzones")
def parking(request: Request):
    return templates.TemplateResponse("paymentzones.html", {
        "request": request
    })

@app.get("/cars")
def parking(request: Request):
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
