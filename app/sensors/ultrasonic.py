import RPi.GPIO as GPIO
import time
import config
from telemetria_shared import telemetria_data

class ModulUltrasons:
    """Classe per gestionar les potes del quadrúpede."""
    def __init__(self):
        # Configura els pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.ULTRASONIC_TRIG, GPIO.OUT)
        GPIO.setup(config.ULTRASONIC_ECHO, GPIO.IN)

    def mesura_distancia(self):
        # Envia trigger curtet
        GPIO.output(config.ULTRASONIC_TRIG, False)
        time.sleep(0.0002)
        GPIO.output(config.ULTRASONIC_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(config.ULTRASONIC_TRIG, False)

        # Espera l'eco
        while GPIO.input(config.ULTRASONIC_ECHO) == 0:
            start = time.time()
        while GPIO.input(config.ULTRASONIC_ECHO) == 1:
            end = time.time()

        # Calcula temps i distancia
        duration = end - start
        distance = (duration * 34300) / 2  # velocitat so = 34300 cm/s

        return distance
    
    def mesura_distancia_auto(self):
        dist = self.mesura_distancia()
        print(f"Distància: {dist:.2f} cm")

