import config
import time
from app.vision.plate_detection import PlateDetection

class PoliceBehavior:
    def __init__(self, speaker, camera):
        self.speaker = speaker
        self.camera = camera

    def detect_license_plate(self):
        #print("[POLICE] Detectant matrícula...")
        frame = self.camera.capture()
        car = PlateDetection.detect_car(frame)
        #print("[POLICE] Cotxe detectat")
        plate = PlateDetection.detect_plate(car)
        #print("[POLICE] Matrícula detectada")
        if plate is not None:
            plate_text,_,_ = PlateDetection.detect_ocr(plate)
            #print(f"[POLICE] Matrícula reconeguda: {plate_text}")
            return plate_text
        else:
            #print("[POLICE] No s'ha pogut detectar la matrícula")
            return None



