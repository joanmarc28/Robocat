# main.py
import threading
from vision.cameraweb import start_webrtc_client
from sensors.ultrasonic import ModulUltrasons
from movement.motors import EstructuraPotes,set_servo_angle
from sensors.gps import ModulGPS
from modes.human import prova
from interface.display import start_displays,displays_message,clear_displays
import config
import time
from utils.helpers import check_internet,get_local_ip
from multiprocessing import Process

from telemetria_shared import telemetria_data,sensors_status
import asyncio
import websockets
import json
import socket
import random


from movement.simulation_data import walk_states
# Variable global per accedir a l'estructura de potes
estructura = None

def start_system(mode, ultrasons: ModulUltrasons = None, gps: ModulGPS = None):
    """Inicia el sistema Robocat, comprova la connexió a Internet i els sistemes bàsics."""
    temps=0.5
    clear_displays()  # Esborrem la pantalla i el buffer

    displays_message("Loading Robocat ........")
    time.sleep(temps)
    displays_message(f"Actual Mode: {mode}")
    time.sleep(temps)
    displays_message(f"Checking Systems ........")
    time.sleep(temps)

    errors = 0

    # Check Internet Connection
    if check_internet():
        displays_message(f"  Internet ..... ok")
        sensors_status["internet"] = True
    else:
        displays_message(f"  Internet ..... Fail")
        sensors_status["internet"] = False
        errors += 1
    time.sleep(temps)

    # Check Ultrasons
    if ultrasons and ultrasons.mesura_distancia():
        displays_message(f"  Ultrasons ..... ok")
        sensors_status["ultrasons"] = True
    else:
        displays_message(f"  Ultrasons ..... Fail")
        sensors_status["ultrasons"] = False
        errors += 1
    time.sleep(temps)

    # Check Ultrasons
    if gps.read_heading() != None:
        displays_message(f"  Heading ..... ok")
        sensors_status["heading"] = True
    else:
        displays_message(f"  Heading ..... Fail")
        sensors_status["heading"] = False
        #errors += 1
    time.sleep(temps)

    # Check Ultrasons
    if gps.read_gps() != None:
        displays_message(f"  GPS ..... ok")
        sensors_status["gps"] = True
    else:
        displays_message(f"  GPS ..... Not Found")
        sensors_status["gps"] = False
        #errors += 1
    time.sleep(temps)

    # Summary
    if errors == 0:
        displays_message(f"All Systems Ready")
        time.sleep(temps)
        displays_message(f"Welcome ")
        return True
    else:
        displays_message(f"Errors Found: {errors}")
        time.sleep(temps)
        displays_message(f"Please Check")
        return False
    
# Funció per inicialitzar tot el sistema físic
def main():
    # Loop principal
    global estructura
    print("🔄 Iniciant el sistema Robocat...")
    # Iniciar els displays

    try:
        ultrasons = ModulUltrasons()
    except Exception as e:
        print(f"[ERROR] Ultrasons: {e}")
        ultrasons = None
        
    try:
        gps = ModulGPS()
    except Exception as e:
        print(f"[ERROR] Ultrasons: {e}")
        gps = None

    if start_displays():
        system_ok = start_system(config.DEFAULT_MODE, ultrasons, gps)
        if not system_ok:
            print("Errors crítics detectats. Aturant el sistema.")
            return  # surt del main

    try:
        estructura = EstructuraPotes(ultrasons)
    except Exception as e:
        print(f"[ERROR] Motors: {e}")
        estructura = None

    # Threads sensors
    if ultrasons:
        t_ultra = threading.Thread(target=ultrasons.thread_ultrasons, daemon=True)
        t_ultra.start()

    if gps:
        t_compas = threading.Thread(target=gps.thread_heading, daemon=True)
        t_compas.start()
        t_gps = threading.Thread(target=gps.thread_gps, daemon=True)
        t_gps.start()


    """t_gps = threading.Thread(target=prova, args=())
    t_gps.daemon = True
    t_gps.start()"""

# Enviar dades reals de telemetria
def obtenir_telemetria():
    return {
        "robot_id": config.ROBOT_ID,
        "ip": get_local_ip(),
        "lat": telemetria_data.get("lat", 0.0),
        "lon": telemetria_data.get("lon", 0.0),
        "heading": telemetria_data.get("heading", 0.0),
        "dist": telemetria_data.get("dist", 0)
    }

# Connectar amb servidor i escoltar comandes
async def connectar():
    uri = f"wss://{config.SERVER_IP}/ws/telemetria"
    global estructura
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connectat al servidor")
            while True:
                dades = obtenir_telemetria()
                await websocket.send(json.dumps(dades))
                print("📤 Enviat:", dades)

                try:
                    resposta = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                    comanda = json.loads(resposta)
                    print("📥 Comanda rebuda:", comanda)

                    if estructura:
                        accio = comanda.get("moviment")
                        if accio == "ajupir":
                            estructura.set_position("sit")
                            """estructura.ajupir()"""
                            time.sleep(0.5)
                        elif accio == "endavant":
                            estructura.follow_sequance(walk_states,cycles=1,t=0.4)
                            """estructura.caminar_1()"""
                            time.sleep(0.5)
                        elif accio == "normal":
                            """estructura.moure_4_potes("normal", 0.3)"""
                            time.sleep(0.5)
                        elif accio == "up":
                            estructura.set_position("up")
                            """estructura.moure_4_potes("up", 0.3)"""
                            time.sleep(0.5)
                        elif accio == "strech":
                            """estructura.moure_4_potes("strech", 0.3)"""
                            time.sleep(0.5)
                        elif accio == "prova":
                            """estructura.moure_4_potes("prova", 0.3)"""
                            time.sleep(0.5)

                except asyncio.TimeoutError:
                    pass
    except Exception as e:
        print("❌ Error de connexió:", e)
        await asyncio.sleep(5)
        await connectar()


async def main_async():
    # Llança les dues corroutines async en paral·lel
    await asyncio.gather(
        start_webrtc_client(),
        connectar()
    )

if __name__ == "__main__":
    # Llança el codi sincrònic en un thread
    threading.Thread(target=main, daemon=True).start()

    # Llança el loop asyncio amb les dues funcions async
    asyncio.run(main_async())

    
    
