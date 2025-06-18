from interface.display import clear_displays, displays_show_frames
from interface.speaker import Speaker
import config
import time
from vision.camera import RobotCamera

class Human:

    def __init__(self, speaker:Speaker=None,camera:RobotCamera=None):
        self.active = False
        self.speaker = speaker

    def express_emotion(self, emotion, duration=5):
        print(f"[🤖] Expressant emoció: {emotion}")
        
        # Dir l'emoció amb veu
        self.speaker.say_emotion(emotion)

        # Mostrar-la durant `duration` segons
        t_inici = time.time()
        while time.time() - t_inici < duration:
            displays_show_frames(emotion)
        
        clear_displays()