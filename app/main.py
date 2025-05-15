# main.py
from modes.human import prova
from interface.display import display_message,clear_displays
import config
import time


def start_system():
    display_message("Loading Robocat ........", line=0)
    time.sleep(1)
    display_message(f"Actual Mode: {config.DEFAULT_MODE}", line=1)
    time.sleep(1)
    display_message(f"All Systems Ready", line=2)
    time.sleep(1)
    display_message(f"Welcome to Robocat Interaction Systems", line=3)
    display_message(f"......................................", line=4)

def main():
    start_system()
    time.sleep(1)
    prova()

if __name__ == "__main__":
    main()
