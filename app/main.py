# main.py
import threading
from sensors.ultrasonic import ModulUltrasons
from movement.motors import EstructuraPotes,set_servo_angle,PotaIK
from sensors.gps import thread_gps, thread_heading
#from modes.human import prova
#from interface.display import display_message,clear_displays
import config
import time
from utils.helpers import check_internet,get_local_ip
from multiprocessing import Process

from telemetria_shared import telemetria_data
import asyncio
import websockets
import json
import socket
import random


def start_system(mode, ultrasons=None, heading=None, gps=None):
    """Inicia el sistema Robocat, comprova la connexió a Internet i els sistemes bàsics."""
    temps=0.5
    clear_displays()  # Esborrem la pantalla i el buffer

    display_message("Loading Robocat ........")
    time.sleep(temps)
    display_message(f"Actual Mode: {mode}")
    time.sleep(temps)
    display_message(f"Checking Systems ........")
    time.sleep(temps)

    errors = 0

    # Check Internet Connection
    if check_internet():
        display_message(f"  Internet ..... ok")
    else:
        display_message(f"  Internet ..... Fail")
        errors += 1
    time.sleep(temps)

    # Check Ultrasons
    if ultrasons and ultrasons.mesura_distancia():
        display_message(f"  Ultrasons ..... ok")
    else:
        display_message(f"  Ultrasons ..... Fail")
        errors += 1
    time.sleep(temps)

    # Check Ultrasons
    if heading:
        display_message(f"  Heading ..... ok")
    else:
        display_message(f"  Heading ..... Fail")
        #errors += 1
    time.sleep(temps)

    # Check Ultrasons
    if gps:
        display_message(f"  GPS ..... ok")
    else:
        display_message(f"  GPS ..... Not Found")
        #errors += 1
    time.sleep(temps)

    # Summary
    if errors == 0:
        display_message(f"All Systems Ready")
        time.sleep(temps)
        display_message(f"Welcome ")
        return True
    else:
        display_message(f"Errors Found: {errors}")
        time.sleep(temps)
        display_message(f"Please Check")
        return False

"""def altres():
    start_system()
    time.sleep(0.5)
    #prova()
    while True:
        try:
            print("🔍 Llegint GPS i brúixola...")
            lat, lon = read_gps(timeout=10)
            heading = read_heading()

            if lat is not None and lon is not None:
                print(f"📍 Latitud: {lat:.6f}, Longitud: {lon:.6f}, Heading: {heading:.1f}°")
            else:
                print("❗️ Sense fix GPS actualment")

            time.sleep(1)

        except KeyboardInterrupt:
            print("🛑 Sortint per teclat...")
            break

        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(0.5)
"""
def thread_ultrasons(ultrasons):
    while True:
        ultrasons.mesura_distancia_auto()
        dist = ultrasons.mesura_distancia()
        telemetria_data["dist"] = dist
        time.sleep(0.5)

def main():
    # Loop principal
    
    try:
        ultrasons = ModulUltrasons()
    except Exception as e:
        print(f"[ERROR] No s'ha pogut inicialitzar el mòdul d'ultrasons: {e}")
        ultrasons = None
    
    try:
        estructura = EstructuraPotes(ultrasons)
    except Exception as e:
        print(f"[ERROR] No s'ha pogut inicialitzar els Motors: {e}")
        estructura = None

    # Aquí comprovem si hi ha errors
    """system_ok = start_system(config.DEFAULT_MODE, ultrasons, None, None)
    if not system_ok:
        print("Errors crítics detectats. Aturant el sistema.")
        return  # surt del main"""

    t_ultra = threading.Thread(target=thread_ultrasons, args=(ultrasons,))
    t_ultra.daemon = True
    t_ultra.start()

    t_compas = threading.Thread(target=thread_heading, args=())
    t_compas.daemon = True
    t_compas.start()

    t_gps = threading.Thread(target=thread_gps, args=())
    t_gps.daemon = True
    t_gps.start()
    
    """t_gps = threading.Thread(target=prova, args=())
    t_gps.daemon = True
    t_gps.start()"""
    
    try:
        while True:
            """time.sleep(0.5)
            set_servo_angle(0,50)
            time.sleep(0.5)
            set_servo_angle(0,90)
            time.sleep(0.5)
            set_servo_angle(0,130)"""
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
            pota_davant_esquerra = PotaIK(12, 13, None, L1=12, L2=9, invertir_cadera=True, invertir_genoll=True)
            pota_darrera_esquerra = PotaIK(6, 7, None, L1=12, L2=9, invertir_cadera=True, invertir_genoll=True)
            pota_darrera_dreta = PotaIK(2, 3, None, L1=12, L2=9, invertir_cadera=False, invertir_genoll=False)
            pota_davant_dreta = PotaIK(10, 11, None, L1=12, L2=9, invertir_cadera=False, invertir_genoll=False)

            # Moure el peu a (x=10, y=5) controlant tota la pota

            pota_davant_esquerra.moure_ik(6, 2, duracio=0.1, part='tot')
            pota_darrera_esquerra.moure_ik(6, 2, duracio=0.1, part='tot')
            pota_darrera_dreta.moure_ik(6, 2, duracio=0.1, part='tot')
            pota_davant_dreta.moure_ik(6, 2, duracio=0.1, part='tot')
            time.sleep(0.5)



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

# Simular dades de telemetria (pots substituir-ho per sensors reals)
def obtenir_telemetria():
    return {
        "robot_id": config.ROBOT_ID,
        "ip": get_local_ip(),
        "lat": telemetria_data.get("lat", 0.0),
        "lon": telemetria_data.get("lon", 0.0),
        "heading": telemetria_data.get("heading", 0.0),
        "dist": telemetria_data.get("dist", 0)
    }

# Executar WebSocket
async def connectar():
    uri = f"ws://{config.SERVER_IP}:{config.SERVER_PORT}/ws/telemetria"
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connectat al servidor")
            while True:
                # Enviar dades cada 0.5s
                dades = obtenir_telemetria()
                await websocket.send(json.dumps(dades))
                print("📤 Enviat:", dades)

                # Esperar comandes (no bloquejant)
                try:
                    resposta = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                    comanda = json.loads(resposta)
                    print("📥 Comanda rebuda:", comanda)
                    # Aquí crides funcions reals per moure motors
                except asyncio.TimeoutError:
                    pass
    except Exception as e:
        print("❌ Error de connexió:", e)
        await asyncio.sleep(5)
        await connectar()

if __name__ == "__main__":
    asyncio.run(connectar())
    main()
    
