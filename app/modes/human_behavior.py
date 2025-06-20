from interface.display import clear_displays, displays_show_frames
from interface.speaker import Speaker
import config
import time
from vision.camera import RobotCamera
import threading

class HumanBehavior:
    def __init__(self, speaker: Speaker = None, camera: RobotCamera = None):
        self.speaker = speaker
        self.camera = camera

    def express_emotion(self, emotion, duration=3):
        # Funció per parlar en un fil separat
        def speak():
            self.speaker.say_emotion(emotion)

        # Inicia el fil de veu
        t_speak = threading.Thread(target=speak)
        t_speak.start()

        # Mostra l'emoció mentre el fil de veu està funcionant
        t_inici = time.time()
        while time.time() - t_inici < duration:
            displays_show_frames(emotion)

        # Espera que el fil acabi per si no ha acabat encara
        t_speak.join()
        clear_displays()
