
from interface.display import display_message, clear_displays, show_frames
import config
import time
from interface.speaker import say_emotion

def prova():
    emotions = ["neutral", "happy", "surprised", "angry", "sleepy","sad"]
    
    durada_total = 10  # segons
    t_inici = time.time()
    while time.time() - t_inici < durada_total:
        show_frames("neutral")

    clear_displays()
       

    print("→ Reproduint emocions:")
    for e in emotions:
        print(f"  · {e}")
        say_emotion(e)
        time.sleep(1)


def prova_text():
    # Mostra missatge inicial a la pantalla OLED
    display_message("Robocat Ready", line=0)
    display_message(f"Mode: {config.DEFAULT_MODE}", line=1)
