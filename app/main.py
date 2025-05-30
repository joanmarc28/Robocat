# main.py
import threading
from sensors.ultrasonic import ModulUltrasons
from movement.motors import EstructuraPotes
from sensors.gps import thread_gps, thread_heading
#from modes.human import prova
from interface.display import display_message,clear_displays
import config
import time
from utils.helpers import check_internet
from multiprocessing import Process


def start_system():
    display_message("Loading Robocat ........", line=0)
    time.sleep(0.5)
    display_message(f"Actual Mode: {config.DEFAULT_MODE}", line=1)
    time.sleep(0.5)
    display_message(f"Checking Systems ........", line=2)
    time.sleep(0.5)
    if check_internet():
        display_message(f"Internet ..... ok", line=3)
    else:
        display_message(f"Internet ..... Fail", line=3)
    time.sleep(0.5)
    display_message(f"All Systems Ready", line=4)
    time.sleep(0.5)
    display_message(f"Welcome ", line=5)

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
        time.sleep(0.5)

def main():
    # Loop principal
    estructura = EstructuraPotes()
    start_system()
    ultrasons = ModulUltrasons()

    t_ultra = threading.Thread(target=thread_ultrasons, args=(ultrasons,))
    t_ultra.daemon = True
    t_ultra.start()

    t_compas = threading.Thread(target=thread_heading, args=())
    t_compas.daemon = True
    t_compas.start()

    t_gps = threading.Thread(target=thread_gps, args=())
    t_gps.daemon = True
    t_gps.start()

    try:
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
        print("🛑 Aturat per teclat.")


if __name__ == "__main__":
    main()
