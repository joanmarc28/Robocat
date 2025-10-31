import config
import time
from vision.container_detection import ContainerDetection
import requests
import base64
from datetime import datetime
from interface.speaker import Speaker
import cv2
from vision.camera import RobotCamera
from interface.display import clear_displays, displays_show_frames

class CityBehavior:
    def __init__(self, speaker:Speaker, camera):
        self.speaker = speaker
        self.camera = camera
        #self.detected_plates = []  # Llista d'últimes matrícules detectades
        #self.max_plates_stored = 5  # Quantes últimes guardes
        self.similarity_threshold = 0.85  # Percentatge mínim de similitud per considerar-la la mateixa

    def detect_container(self, state="city", duration=3):
        t_inici = time.time()
        while time.time() - t_inici < duration:
            displays_show_frames(state)
        try:
            frame = self.camera.capture()
            container, _ = ContainerDetection.detect_container(frame, camera=self.camera)
            if container is not None:
                print(f"[CITY] Nou container detectat")
                #falta que mostri el frame amb el container!
            return None
        except Exception as e:
            print(f"[ERROR] Error en la detecció del container {e}")
            return None
