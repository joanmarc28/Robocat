# main.py
import threading
"""from app.vision.old_cameraweb import send_frames"""
from vision.camera import RobotCamera
from sensors.ultrasonic import ModulUltrasons
from movement.motors import EstructuraPotes
from sensors.gps import ModulGPS
from interface.display import start_displays, displays_message, clear_displays
import config
import time
from utils.helpers import check_internet, get_local_ip
from telemetria_shared import telemetria_data, sensors_status
import asyncio
import websockets
import json
from movement.simulation_data import walk_states
from vision.slam import start_autonomous_slam
from queue import Queue

estructura = None
camera = RobotCamera()


moviment_queue = Queue()
slam_controller = None

def start_system(mode, ultrasons:ModulUltrasons=None, gps=None):
    clear_displays()
    temps = 0.5
    displays_message("Loading Robocat ........")
    time.sleep(temps)
    displays_message(f"Actual Mode: {mode}")
    time.sleep(temps)
    displays_message(f"Checking Systems ........")
    time.sleep(temps)
    errors = 0

    if check_internet():
        displays_message(f"  Internet ..... ok")
        sensors_status["internet"] = True
    else:
        displays_message(f"  Internet ..... Fail")
        sensors_status["internet"] = False
        errors += 1
    time.sleep(temps)

    if ultrasons and ultrasons.mesura_distancia():
        displays_message(f"  Ultrasons ..... ok")
        sensors_status["ultrasons"] = True
    else:
        displays_message(f"  Ultrasons ..... Fail")
        sensors_status["ultrasons"] = False
        errors += 1
    time.sleep(temps)

    if gps and gps.read_heading() is not None:
        displays_message(f"  Heading ..... ok")
        sensors_status["heading"] = True
    else:
        displays_message(f"  Heading ..... Fail")
        sensors_status["heading"] = False
    time.sleep(temps)

    if gps and gps.read_gps() is not None:
        displays_message(f"  GPS ..... ok")
        sensors_status["gps"] = True
    else:
        displays_message(f"  GPS ..... Not Found")
        sensors_status["gps"] = False
    time.sleep(temps)

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

def main():
    global estructura, slam_controller
    print("🔄 Iniciant el sistema Robocat...")

    try:
        ultrasons = ModulUltrasons()
    except Exception as e:
        print(f"[ERROR] Ultrasons: {e}")
        ultrasons = None

    try:
        gps = ModulGPS()
    except Exception as e:
        print(f"[ERROR] GPS: {e}")
        gps = None

    if start_displays():
        if not start_system(config.DEFAULT_MODE, ultrasons, gps):
            print("Errors crítics detectats. Aturant el sistema.")
            return

    try:
        estructura = EstructuraPotes(ultrasons)
    except Exception as e:
        print(f"[ERROR] Motors: {e}")
        estructura = None

    if ultrasons:
        threading.Thread(target=ultrasons.thread_ultrasons, daemon=True).start()
    if gps:
        threading.Thread(target=gps.thread_heading, daemon=True).start()
        threading.Thread(target=gps.thread_gps, daemon=True).start()

    while True:
        accio = moviment_queue.get()
        try:
            if accio == "endavant":
                estructura.follow_sequance(walk_states, cycles=6, t=0.2)
            elif accio == "ajupir":
                estructura.set_position("sit")
                """estructura.follow_sequance(sit_sequence, cycles=1, t=0.2)"""
            elif accio == "normal":
                """estructura.follow_sequance(up_sequence, cycles=1, t=0.2)"""
                estructura.set_position("normal")
            elif accio == "hind_sit":
                estructura.sit_hind_legs()
            elif accio == "up":
                estructura.set_position("up")
            elif accio == "strech":
                pass
            elif accio == "autonom":
                if slam_controller is None:
                    try:
                        slam_controller = start_autonomous_slam()
                    except Exception as e:
                        print(f"[ERROR] Autonomous SLAM: {e}")
        except Exception as e:
            print(f"[ERROR] Executant acció '{accio}': {e}")
        moviment_queue.task_done()

def obtenir_telemetria():
    return {
        "robot_id": config.ROBOT_ID,
        "ip": get_local_ip(),
        "lat": telemetria_data.get("lat", 0.0),
        "lon": telemetria_data.get("lon", 0.0),
        "heading": telemetria_data.get("heading", 0.0),
        "dist": telemetria_data.get("dist", 0)
    }

async def connectar():
    uri = f"wss://{config.SERVER_IP}/ws/telemetria"
    global estructura
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ Connectat al servidor")
                while True:
                    await websocket.send(json.dumps(obtenir_telemetria()))

                    try:
                        resposta = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                        comanda = json.loads(resposta)
                        if estructura:
                            accio = comanda.get("moviment")
                            print("Comanda: "+ accio)
                            if accio:
                                print(f"📥 Comanda rebuda: {accio}")
                                moviment_queue.put(accio)

                    except asyncio.TimeoutError:
                        pass
        except Exception as e:
            print("❌ Error de connexió:", e)
            await asyncio.sleep(5)
            continue

async def main_async():
    await asyncio.gather(
        camera.stream_frames(),
        connectar()
    )

if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()
    asyncio.run(main_async())
