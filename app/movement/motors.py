import math
import time
import config
import board
import busio
import numpy as np
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import threading
from sensors.ultrasonic import ModulUltrasons

# Inicialització del bus I2C i la controladora PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz és l’estàndard per a servos

# Inicialitza els 10 primers canals com a servos
servos = []
for i in range(16):
    s = servo.Servo(pca.channels[i], min_pulse=500, max_pulse=2500)
    servos.append(s)

"""class Pota:
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
        self.moure_a_parts_cama(angle_cadera, angle_genoll, duracio)"""
class Pota:
    def __init__(self, cadera, genoll, estats, invertir_cadera=False, invertir_genoll=False):
        self.cadera = cadera
        self.genoll = genoll
        self.estats = estats
        self.invertir_cadera = invertir_cadera
        self.invertir_genoll = invertir_genoll

    def aplica_inversio(self, angle, invertir):
        return 180 - angle if invertir else angle

    def moure_a_la_vegada_cama(self, angle_cadera, angle_genoll, duracio=1):
        angle_cadera = self.aplica_inversio(angle_cadera, self.invertir_cadera)
        angle_genoll = self.aplica_inversio(angle_genoll, self.invertir_genoll)

        t1 = threading.Thread(target=moure_suau, args=(self.genoll, self.genoll.angle or 90, angle_genoll, duracio))
        t1.start()
        t1.join()

        t2 = threading.Thread(target=moure_suau, args=(self.cadera, self.cadera.angle or 90, angle_cadera, duracio))
        t2.start()
        t2.join()
     
    def moure_a_parts_cama(self, angle_cadera, angle_genoll, duracio=1):
        angle_cadera = self.aplica_inversio(angle_cadera, self.invertir_cadera)
        angle_genoll = self.aplica_inversio(angle_genoll, self.invertir_genoll)

        moure_suau(self.genoll, self.genoll.angle or 90, angle_genoll, duracio)
        moure_suau(self.cadera, self.cadera.angle or 90, angle_cadera, duracio)

    def canvia_estat(self, estat, duracio=1):
        if estat not in self.estats:
            raise ValueError(f"[ERROR] Estat '{estat}' no definit per la pota.")
        angle_cadera, angle_genoll = self.estats[estat]
        self.moure_a_parts_cama(angle_cadera, angle_genoll, duracio)


class EstructuraPotes:
    """Classe per gestionar les potes del quadrúpede."""
    def __init__(self,ultrasons=None):
        self.ultrasons = ultrasons
        # Cama - Cuixa
        #Pota Davant Esquerra
        self.pota_davant_esquerra = Pota(servos[12], servos[13], {
            "prova": (0, 180),
            "lower": (180, 180),
            "normal": (130, 120),
            "up": (100, 165),
            "strech": (130, 120),
            "step_1": (115, 165),
            "step_2": (100, 165),
            "step_3": (100, 165),
            "step_4": (100, 165),
            "step_5": (100, 165),
            "step_6": (100, 165)
        })

        self.pota_darrera_esquerra = Pota(servos[6], servos[7], {
            "prova": (0, 180),
            "lower": (180, 180),
            "normal": (130, 120),
            "up": (100, 160),
            "strech": (100, 160),
            "step_1": (115, 130),
            "step_2": (100, 160),
            "step_3": (100, 160),
            "step_4": (100, 160),
            "step_5": (100, 160),
            "step_6": (100, 160)
        })

        self.pota_darrera_dreta = Pota(servos[2], servos[3], {
            "prova": (180, 0),
            "lower": (0, 0),
            "normal": (50, 60),
            "up": (70, 20),
            "strech": (80, 20),
            "step_1": (45, 50),
            "step_2": (70, 20),
            "step_3": (70, 20),
            "step_4": (70, 20),
            "step_5": (70, 20),
            "step_6": (70, 20)
        })

        self.pota_davant_dreta = Pota(servos[10], servos[11], {
            "prova": (180, 0),
            "lower": (0, 0),
            "normal": (30, 50),
            "up": (60, 20),
            "strech": (30, 50),
            "step_1": (45, 20),
            "step_2": (60, 20),
            "step_3": (60, 20),
            "step_4": (60, 20),
            "step_5": (60, 20),
            "step_6": (60, 20)
        })

        self.potes = [
            self.pota_davant_esquerra,
            self.pota_darrera_esquerra,
            self.pota_darrera_dreta,
            self.pota_davant_dreta
        ]
    def moure(self, estat, duracio=1):
        """Mou totes les potes a un estat concret."""
        # Protecio de distància
        """if self.ultrasons and self.ultrasons.mesura_distancia() < config.LLINDAR_ULTRASONIC:
            print("🚨 Distància perillosa detectada, no es mouen les potes!")
            return"""

        for pota in self.potes:
            pota.canvia_estat(estat, duracio)

    # Funció per moure totes les potes en paral·lel
    def moure_4_potes(self,estat, duracio):
        """Mou totes les potes a un estat concret en paral·lel."""
        # Protecio de distància
        """        if self.ultrasons and self.ultrasons.mesura_distancia() < config.LLINDAR_ULTRASONIC:
            print("🚨 Distància perillosa detectada, no es mouen les potes!")
            return"""
        
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

    def caminar_1(self, duracio=0.5):
        print("🔄 Pas 1: aixecant davant esquerra + darrere dreta")
        t1 = threading.Thread(target=self.pota_davant_esquerra.canvia_estat, args=("step_1", duracio))
        t1.start()
        t1.join()
        t1 = threading.Thread(target=self.pota_davant_dreta.canvia_estat, args=("step_1", duracio))
        t1.start()
        t1.join()
        t1 = threading.Thread(target=self.pota_darrera_dreta.canvia_estat, args=("step_1", duracio))
        t1.start()
        t1.join()
        t1 = threading.Thread(target=self.pota_darrera_esquerra.canvia_estat, args=("step_1", duracio))
        t1.start()
        t1.join()
        """t1 = threading.Thread(target=self.pota_davant_esquerra.canvia_estat, args=("step_5", duracio))
        t1.start()
        t1.join()
        t1 = threading.Thread(target=self.pota_davant_esquerra.canvia_estat, args=("step_6", duracio))
        t1.start()
        t1.join()"""
        """t2 = threading.Thread(target=self.pota_darrera_dreta.canvia_estat, args=("step_1", duracio))
        t2.start()
        t2.join()
        t2 = threading.Thread(target=self.pota_darrera_esquerra.canvia_estat, args=("step_1", duracio))
        t2.start()
        t2.join()"""

    def caminar_2(self, duracio=0.5):
        print("🔄 Pas 1: aixecant davant esquerra + darrere dreta")
        t1 = threading.Thread(target=self.pota_davant_dreta.canvia_estat, args=("step_2", duracio))
        t1.start()
        t1.join()
        t1 = threading.Thread(target=self.pota_davant_esquerra.canvia_estat, args=("step_2", duracio))
        t1.start()
        t1.join()
        """t2 = threading.Thread(target=self.pota_darrera_esquerra.canvia_estat, args=("step_2", duracio))
        t2.start()
        t2.join()
        t2 = threading.Thread(target=self.pota_darrera_dreta.canvia_estat, args=("step_2", duracio))
        t2.start()
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







        
class PotaIK(Pota):
    def __init__(self, cadera, genoll, estats, L1, L2, invertir_cadera, invertir_genoll):
        super().__init__(servos[cadera], servos[genoll], estats, invertir_cadera, invertir_genoll)
        self.L1 = L1  # Longitud cuixa
        self.L2 = L2  # Longitud cama

    def calcula_angles_ik(self, x, y):
        D = math.hypot(x, y)
        if D > (self.L1 + self.L2):
            raise ValueError("El punt està fora de l'abast de la pota!")

        # Calcula valor del cosinus
        cos_angle_genoll = (self.L1**2 + self.L2**2 - D**2) / (2 * self.L1 * self.L2)
        cos_angle_genoll = max(-1, min(1, cos_angle_genoll))  # Clamp
        
        angle_genoll = math.acos(cos_angle_genoll)
        angle_genoll_deg = math.degrees(angle_genoll)

        angle_a = math.atan2(y, x)
        cos_angle_b = (D**2 + self.L1**2 - self.L2**2) / (2 * self.L1 * D)
        cos_angle_b = max(-1, min(1, cos_angle_b))  # Clamp

        angle_b = math.acos(cos_angle_b)
        angle_cuixa_deg = math.degrees(angle_a + angle_b)

        return angle_cuixa_deg, angle_genoll_deg


    def moure_ik(self, x, y, duracio=1, part='tot'):
        angle_cuixa, angle_genoll = self.calcula_angles_ik(x, y)

        if part == 'tot':
            self.moure_a_parts_cama(angle_cuixa, angle_genoll, duracio)
        elif part == 'cuixa':
            self.moure_a_parts_cama(angle_cuixa, self.genoll.angle or 90, duracio)
        elif part == 'cama':
            self.moure_a_parts_cama(self.cadera.angle or 90, angle_genoll, duracio)
        else:
            raise ValueError("Part desconeguda, usa 'tot', 'cuixa' o 'cama'.")
