# app/router_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Robot
from datetime import datetime
import json
import requests
import copy

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

clients = {}
telemetria_data = {}

#WebSocket -> telemetria i registrar robots
@router.websocket("/ws/telemetria")
async def websocket_telemetria(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    robot_id = None
    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)

            robot_id = data.get("robot_id")
            ip = data.get("ip")

            if robot_id and ip:
                robot = db.query(Robot).filter_by(identificador=robot_id).first()
                if not robot:
                    robot = Robot(nom=robot_id.upper(), identificador=robot_id)
                    db.add(robot)

                robot.ip = ip
                robot.estat = "online"
                robot.ultima_connexio = datetime.utcnow()
                db.commit()

                clients[robot_id] = websocket
                telemetria_data[robot_id] = data

    except WebSocketDisconnect:
        if robot_id:
            robot = db.query(Robot).filter_by(identificador=robot_id).first()
            if robot:
                robot.estat = "offline"
                db.commit()
            clients.pop(robot_id, None)
            telemetria_data.pop(robot_id, None)
            

import asyncio

@router.websocket("/ws/telemetria/clients/{robot_id}")
async def websocket_client(websocket: WebSocket, robot_id: str):
    await websocket.accept()
    print(f"👤 Navegador connectat per {robot_id}")
    anterior = None
    try:
        while True:
            actual = telemetria_data.get(robot_id)
            if actual is not None:
                if actual != anterior:
                    await websocket.send_text(json.dumps(actual))
                    anterior = copy.deepcopy(actual)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"Navegador desconnectat per {robot_id}")


#enviar comanda a robot concret
@router.post("/comanda/{robot_id}")
async def enviar_comanda(robot_id: str, request: Request):
    msg = await request.json()
    ws = clients.get(robot_id)
    if ws:
        await ws.send_text(json.dumps(msg))
        return {"status": "comanda enviada"}
    return {"error": "robot no disponible"}

#stream MJPEG desde IP robot
@router.get("/video/{robot_id}")
def video_feed(robot_id: str, db: Session = Depends(get_db)):
    robot = db.query(Robot).filter_by(identificador=robot_id).first()
    if not robot or not robot.ip:
        return StreamingResponse(content=b"Robot no disponible", media_type="text/plain")

    def proxy_stream():
        try:
            url = f"http://{robot.ip}:8080/video"
            r = requests.get(url, stream=True)
            for chunk in r.iter_content(chunk_size=1024):
                yield chunk
        except:
            yield b"Error accedint al video"

    return StreamingResponse(proxy_stream(), media_type='multipart/x-mixed-replace; boundary=frame')

#interficie control
@router.get("/robocat/{robot_id}")
def robocat_ui(robot_id: str, request: Request):
    return templates.TemplateResponse("robocat.html", {
        "request": request,
        "robot_id": robot_id
    })

@router.get("/robots")
def llista_robots(request: Request, db: Session = Depends(get_db)):
    robots = db.query(Robot).all()
    return templates.TemplateResponse("robots.html", {
        "request": request,
        "robots": robots
    })
