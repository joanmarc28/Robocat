# ~/web-robocat/main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form
from fastapi.responses import RedirectResponse
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

load_dotenv()

@app.get("/")
def home(request: Request):
    usuari = {"nom": "Joan Marc"}
    return templates.TemplateResponse("index.html", {
        "request": request,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

@app.get("/mapa")
def parking(request: Request):
    return templates.TemplateResponse("mapa.html", {
        "request": request,
        "google_maps_key": os.getenv("GOOGLE_MAPS_KEY")
    })

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
