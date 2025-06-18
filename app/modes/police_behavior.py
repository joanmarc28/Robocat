import config
import time

class PoliceBehavior:
    def __init__(self, speaker, camera):
        self.speaker = speaker
        self.camera = camera

    def detect_license_plate(self):
        #print("[POLICE] Detectant matrícula...")
        frame = self.camera.capture()

