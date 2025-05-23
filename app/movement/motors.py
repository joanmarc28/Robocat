import time
import board
import busio
import numpy as np
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import threading

# Inicialització del bus I2C i la controladora PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz és l’estàndard per a servos

# Inicialitza els 10 primers canals com a servos
servos = []
for i in range(16):
    s = servo.Servo(pca.channels[i], min_pulse=500, max_pulse=2500)
    servos.append(s)

class Pota:
    def __init__(self, cadera, genoll,estats):
        self.cadera = cadera
        self.genoll = genoll
        self.estats = estats

    def moure(self, angle_cadera, angle_genoll, duracio=1):
        t1 = threading.Thread(target=moure_suau, args=(self.cadera, self.cadera.angle or 90, angle_cadera, duracio))
        t2 = threading.Thread(target=moure_suau, args=(self.genoll, self.genoll.angle or 90, angle_genoll, duracio))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def canvia_estat(self, estat, duracio=1):
        if estat not in self.estats:
            raise ValueError(f"[ERROR] Estat '{estat}' no definit per la pota.")
        angle_cadera, angle_genoll = self.estats[estat]
        self.moure(angle_cadera, angle_genoll, duracio)


# Moviment suau (simula velocitat)
def moure_suau(servo, angle_inicial, angle_final, duracio):
    passos = 4
    pas = (angle_final - angle_inicial) / passos
    delay = duracio / passos

    for i in range(passos + 1):
        angle_actual = angle_inicial + i * pas
        servo.angle = max(0, min(180, angle_actual))  # Protecció límits
        time.sleep(delay)

# Crear potes (ajusta els canals segons com els tinguis connectats)
potes = [
    Pota(servos[0], servos[1],{"normal": (90, 0),"lower": (120, 60)}),
    Pota(servos[11], servos[10],{"normal": (90, 90),"lower": (120, 60)}),
    Pota(servos[15], servos[14],{"normal": (180, 180),"lower": (120, 120)}),
    Pota(servos[7], servos[6],{"normal": (120, 90),"lower": (120, 120)}),
]

def set_servo_angle(index, angle):
    """Posa un servo concret a un angle determinat."""
    if not (0 <= index < len(servos)):
        raise ValueError("Index de servo fora de rang.")
    if not (0 <= angle <= 180):
        raise ValueError("L'angle ha de ser entre 0 i 180 graus.")
    servos[index].angle = angle

def sweep_servo(index, delay=0.01):
    """Mou el servo d'un extrem a l'altre per provar el rang complet."""
    if not (0 <= index < len(servos)):
        raise ValueError("Index de servo fora de rang.")

    # Anada: de 0 a 180 graus
    for angle in range(0, 181, 1):
        servos[index].angle = angle
        time.sleep(delay)

    # Tornada: de 180 a 0 graus
    for angle in range(180, -1, -1):
        servos[index].angle = angle
        time.sleep(delay)

# Funció per moure totes les potes en paral·lel
def moure_4_potes(estat, duracio):
    threads = []
    for pota in potes:
        t = threading.Thread(target=pota.canvia_estat, args=(estat, duracio))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
