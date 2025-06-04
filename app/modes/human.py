
from interface.display import start_displays,displays_message,clear_displays, displays_show_frames
import config
import time
from interface.speaker import say_emotion

def prova():
    emotions = ["default", "happy", "angry", "patrol","sad"]

    print("→ Reproduint emocions:")
    for e in emotions:
        print(f"  · {e}")
        #say_emotion(e)
        durada_total = 5  # segons
        t_inici = time.time()
        while time.time() - t_inici < durada_total:
            displays_show_frames(e)

        clear_displays()

def prova_text():
    # Mostra missatge inicial a la pantalla OLED
    displays_message("Robocat Ready", line=0)
    displays_message(f"Mode: {config.DEFAULT_MODE}", line=1)
