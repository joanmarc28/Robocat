# main.py
import threading
from sensors.ultrasonic import ModulUltrasons
from movement.motors import EstructuraPotes,set_servo_angle,PotaIK
from sensors.gps import thread_gps, thread_heading
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
# Variable global per accedir a l'estructura de potes
estructura = None

def start_system(mode, ultrasons=None, heading=None, gps=None):
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
    if heading:
        displays_message(f"  Heading ..... ok")
        sensors_status["heading"] = True
    else:
        displays_message(f"  Heading ..... Fail")
        sensors_status["heading"] = False
        #errors += 1
    time.sleep(temps)

    # Check Ultrasons
    if gps:
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

def thread_ultrasons(ultrasons):
    while True:
        ultrasons.mesura_distancia_auto()
        dist = ultrasons.mesura_distancia()
        telemetria_data["dist"] = dist
        time.sleep(0.5)

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
        
    if start_displays():
        system_ok = start_system(config.DEFAULT_MODE, ultrasons, None, None)
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
        t_ultra = threading.Thread(target=thread_ultrasons, args=(ultrasons,), daemon=True)
        t_ultra.start()

    t_compas = threading.Thread(target=thread_heading, daemon=True)
    t_compas.start()

    t_gps = threading.Thread(target=thread_gps, daemon=True)
    t_gps.start()


    t_gps = threading.Thread(target=prova, args=())
    t_gps.daemon = True
    t_gps.start()
    
    try:
        while True:
            """time.sleep(0.5)
            set_servo_angle(15,50)
            time.sleep(0.5)
            set_servo_angle(15,90)
            time.sleep(0.5)
            set_servo_angle(15,130)"""
            """time.sleep(1)
            set_servo_angle(13,120)
            set_servo_angle(12,130)

            time.sleep(1)
            set_servo_angle(13,150)
            set_servo_angle(12,160)

            time.sleep(1)
            set_servo_angle(13,165)
            set_servo_angle(12,90)

            time.sleep(1)
            set_servo_angle(13,150)
            set_servo_angle(12,145)"""

            """print("🔄 Executant moviment Ajupir ...")
            estructura.ajupir()
            time.sleep(0.5)

            print("🔄 Executant moviment normal 90graus...")
            estructura.moure_4_potes("normal", 0.3)
            time.sleep(0.5)

            print("🔄 Executant moviment up...")
            estructura.moure_4_potes("up", 0.3)
            time.sleep(0.5)

            print("🔄 Executant moviment strech...")
            estructura.moure_4_potes("strech", 0.3)
            time.sleep(0.5)"""

            """print("🔄 Executant moviment up...")
            estructura.moure_4_potes("up", 0.1)
            time.sleep(0.05)"""

            """print("🔄 Executant moviment Caminant_1...")
            estructura.caminar_1()
            time.sleep(0.05)"""

            # Ex: longituds de la cuixa i cama en mm o cm segons el teu robot
            """pota_davant_esquerra = PotaIK(12, 13, None, L1=12, L2=9, invertir_cadera=True, invertir_genoll=True)
            pota_darrera_esquerra = PotaIK(6, 7, None, L1=12, L2=9, invertir_cadera=True, invertir_genoll=True)
            pota_darrera_dreta = PotaIK(2, 3, None, L1=12, L2=9, invertir_cadera=False, invertir_genoll=False)
            pota_davant_dreta = PotaIK(10, 11, None, L1=12, L2=9, invertir_cadera=False, invertir_genoll=False)

            # Moure el peu a (x=10, y=5) controlant tota la pota

            pota_davant_esquerra.moure_ik(6, 2, duracio=0.1, part='tot')
            pota_darrera_esquerra.moure_ik(6, 2, duracio=0.1, part='tot')
            pota_darrera_dreta.moure_ik(6, 2, duracio=0.1, part='tot')
            pota_davant_dreta.moure_ik(6, 2, duracio=0.1, part='tot')
            time.sleep(0.5)"""



    except KeyboardInterrupt:
        print("🛑 Aturat per teclat (Ctrl+C).")

    """    try:
        while True:
            time.sleep(0.5)
            print("🔄 Iniciant moviment de les potes...")
            estructura.ajupir()
            time.sleep(0.5)
            estructura.moure_4_potes("normal", 0.3)
            time.sleep(0.5)
            estructura.moure_4_potes("up", 0.3)
            time.sleep(0.5)
            estructura.moure_4_potes("strech", 0.3)
            time.sleep(0.5)
            estructura.moure_4_potes("up", 0.3)
            time.sleep(0.5)
            #estructura.caminar_1()
            #print("✅ Moviment de les potes completat.")
            #time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Aturat per teclat.")"""

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
                            estructura.ajupir()
                            time.sleep(0.5)
                        elif accio == "endavant":
                            estructura.caminar_1()
                            time.sleep(0.5)
                        elif accio == "normal":
                            estructura.moure_4_potes("normal", 0.3)
                            time.sleep(0.5)
                        elif accio == "up":
                            estructura.moure_4_potes("up", 0.3)
                            time.sleep(0.5)
                        elif accio == "strech":
                            estructura.moure_4_potes("strech", 0.3)
                            time.sleep(0.5)

                except asyncio.TimeoutError:
                    pass
    except Exception as e:
        print("❌ Error de connexió:", e)
        await asyncio.sleep(5)
        await connectar()

# Llançar `main()` i WebSocket en paral·lel
if __name__ == "__main__":
    """main()"""
    threading.Thread(target=main, daemon=True).start()
    asyncio.run(connectar())

