# main.py
import threading
from movement.motors import moure_4_potes, set_servo_angle,sweep_servo
#from sensors.gps import read_gps, read_heading
#from modes.human import prova
#from interface.display import display_message,clear_displays
import config
import time
from utils.helpers import check_internet
from multiprocessing import Process

"""
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

def altres():
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
def servos_prova(num):
            set_servo_angle(num, 0)
            time.sleep(0.5)
            set_servo_angle(num, 15)
            time.sleep(0.5)
            set_servo_angle(num, 30)
            time.sleep(0.5)
            set_servo_angle(num, 90)
            time.sleep(0.5)
            set_servo_angle(num, 120)
            time.sleep(0.5)
            set_servo_angle(num, 180)
            time.sleep(0.5)

def main():
    # Loop principal
    try:
        while True:
            """print("🔻 Baixant...")
            moure_4_potes("lower", 1)
            time.sleep(2)
            print("🔼 Tornant a normal...")
            moure_4_potes("normal", 1)"""
            servos_prova(7)
            time.sleep(2)
    except KeyboardInterrupt:
        print("🛑 Aturat per teclat.")


if __name__ == "__main__":
    main()
