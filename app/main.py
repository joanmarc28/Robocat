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

    try:
        while True:
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

            print("🔄 Executant moviment up...")
            estructura.moure_4_potes("up", 0.1)
            time.sleep(0.05)

            print("🔄 Executant moviment Caminant_1...")
            estructura.caminar_1()
            time.sleep(0.05)

            print("🔄 Executant moviment up...")
            estructura.moure_4_potes("up", 0.1)
            time.sleep(0.05)

            print("🔄 Executant moviment Caminant_2...")
            estructura.caminar_2()
            time.sleep(0.05)


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


if __name__ == "__main__":
    main()
