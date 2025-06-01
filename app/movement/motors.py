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

    def moure_a_la_vegada_cama(self, angle_cadera, angle_genoll, duracio=1):
        t1 = threading.Thread(target=moure_suau, args=(self.genoll, self.genoll.angle or 90, angle_genoll, duracio))
        t1.start()
        t1.join()

        t2 = threading.Thread(target=moure_suau, args=(self.cadera, self.cadera.angle or 90, angle_cadera, duracio))
        t2.start()
        t2.join()
     
    def moure_a_parts_cama(self, angle_cadera, angle_genoll, duracio=1):
        moure_suau(self.genoll, self.genoll.angle or 90, angle_genoll, duracio)
        moure_suau(self.cadera, self.cadera.angle or 90, angle_cadera, duracio)

    def canvia_estat(self, estat, duracio=1):
        if estat not in self.estats:
            raise ValueError(f"[ERROR] Estat '{estat}' no definit per la pota.")
        angle_cadera, angle_genoll = self.estats[estat]
        self.moure_a_parts_cama(angle_cadera, angle_genoll, duracio)

class EstructuraPotes:
    """Classe per gestionar les potes del quadrúpede."""
    def __init__(self):
        # Cama - Cuixa
        #Pota Davant Esquerra
        self.pota_davant_esquerra = Pota(servos[12], servos[13], {
            "prova": (0, 180),
            "lower": (180, 180),
            "normal": (130, 120),
            "up": (100, 165),
            "strech": (130, 120),
            "step_1": (100, 100),  # avança
            "step_2": (160, 140)   # recull
        })

        self.pota_darrera_esquerra = Pota(servos[6], servos[7], {
            "prova": (0, 180),
            "lower": (180, 180),
            "normal": (130, 120),
            "up": (100, 160),
            "strech": (100, 160),
            "step_1": (100, 100),
            "step_2": (160, 140)
        })

        self.pota_darrera_dreta = Pota(servos[2], servos[3], {
            "prova": (180, 0),
            "lower": (0, 0),
            "normal": (50, 60),
            "up": (70, 20),
            "strech": (80, 20),
            "step_1": (80, 80),
            "step_2": (20, 40)
        })

        self.pota_davant_dreta = Pota(servos[10], servos[11], {
            "prova": (180, 0),
            "lower": (0, 0),
            "normal": (30, 50),
            "up": (60, 20),
            "strech": (30, 50),
            "step_1": (60, 70),
            "step_2": (0, 30)
        })

        self.potes = [
            self.pota_davant_esquerra,
            self.pota_darrera_esquerra,
            self.pota_darrera_dreta,
            self.pota_davant_dreta
        ]
    def moure(self, estat, duracio=1):
        for pota in self.potes:
            pota.canvia_estat(estat, duracio)

    # Funció per moure totes les potes en paral·lel
    def moure_4_potes(self,estat, duracio):
        threads = []
        """ for pota in potes:
            t = threading.Thread(target=pota.canvia_estat, args=(estat, duracio))
            threads.append(t)
            t.start()"""
        t = threading.Thread(target=self.pota_darrera_esquerra.canvia_estat, args=(estat, duracio))
        threads.append(t)
        t.start()
        t = threading.Thread(target=self.pota_darrera_dreta.canvia_estat, args=(estat, duracio))
        threads.append(t)
        t.start()

        time.sleep(0.07)
        t = threading.Thread(target=self.pota_davant_esquerra.canvia_estat, args=(estat, duracio))
        threads.append(t)
        t.start()
        t = threading.Thread(target=self.pota_davant_dreta.canvia_estat, args=(estat, duracio))
        threads.append(t)
        t.start()
        for t in threads:
            t.join()

    def ajupir(self, duracio=0.5):
        print("🔻 Baixant totes les potes")
        self.moure_4_potes("lower", duracio)

    def estirament(self, duracio=0.5):
        print("🤸 Estirant potes")
        self.potes[0].canvia_estat("strech", duracio)
        self.potes[1].canvia_estat("strech", duracio)
        self.potes[2].canvia_estat("strech", duracio)
        self.potes[3].canvia_estat("strech", duracio)

    def saluda_amb_davant_dreta(self, duracio=1):
        self.pota_davant_dreta.canvia_estat("up", duracio)
        time.sleep(duracio)
        self.pota_davant_dreta.canvia_estat("normal", duracio)

    def caminar_1(estructura, duracio=0.5):
        print("🔄 Pas 1: aixecant davant esquerra + darrere dreta")
        t1 = threading.Thread(target=estructura.pota_darrera_dreta.canvia_estat, args=("step_1", duracio))
        t2 = threading.Thread(target=estructura.pota_darrera_esquerra.canvia_estat, args=("step_1", duracio))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

"""        t1 = threading.Thread(target=estructura.pota_darrera_dreta.canvia_estat, args=("step_2", duracio))
        t2 = threading.Thread(target=estructura.pota_darrera_esquerra.canvia_estat, args=("step_2", duracio))
        t1.start()
        t2.start()
        t1.join()
        t2.join()"""


# Moviment suau (simula velocitat)
def moure_suau(servo, angle_inicial, angle_final, duracio, passos=30):
    pas = (angle_final - angle_inicial) / passos
    delay = duracio / passos

    for i in range(passos + 1):
        angle_actual = angle_inicial + i * pas
        servo.angle = max(0, min(180, angle_actual))  # Protecció límits
        time.sleep(delay)

# Crear potes (ajusta els canals segons com els tinguis connectats)

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