# ~/web-robocat/main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    usuari = {"nom": "Joan Marc"}
    return templates.TemplateResponse("index.html", {"request": request, "usuari": usuari})

@app.get("/mapa")
def parking(request: Request):
    return templates.TemplateResponse("mapa.html", {"request": request, "usuari": "Joan Marc"})