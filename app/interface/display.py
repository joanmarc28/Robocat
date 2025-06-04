# interface/display.py
from PIL import Image, ImageDraw
import board
import busio
import config
import os
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

"""WIDTH = config.OLED_WIDTH
HEIGHT = config.OLED_HEIGHT

serial = i2c(port=config.I2C_BUS_OLED_LEFT, address=0x3C)
left_eye = ssd1306(serial, width=config.OLED_WIDTH, height=config.OLED_HEIGHT)

serial2 = i2c(port=config.I2C_BUS_OLED_RIGHT, address=0x3C)
right_eye = ssd1306(serial2, width=config.OLED_WIDTH, height=config.OLED_HEIGHT)

# Crea imatge en blanc una vegada
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# Calcula quantes línies caben segons altura i mida de lletra (~10 px per línia)
MAX_LINES = HEIGHT // 10

# Guarda les línies que es mostraran
line_cache = []

def clear_displays():
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    left_eye.display(image)    
    right_eye.display(image)

def display_message(text):
    global line_cache

    # Afegeix la nova línia al final
    line_cache.append(text)

    # Si tenim més línies del que cap, elimina les més antigues
    if len(line_cache) > MAX_LINES:
        line_cache = line_cache[-MAX_LINES:]

    # Esborra la imatge
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Escriu totes les línies del buffer
    for i, line in enumerate(line_cache):
        y = i * 10
        draw.text((0, y), line, fill=255)

    # Actualitza les dues pantalles
    left_eye.display(image)
    right_eye.display(image)



def show_frames(carpeta_frames):
    # Llegeix i ordena els fitxers de la carpeta
    fitxers_left = sorted([
        f for f in os.listdir("assets/eyes_img/"+carpeta_frames+"/left")
        if f.lower().endswith(('.png', '.bmp'))
    ])
    
    fitxers_right = sorted([
        f for f in os.listdir("assets/eyes_img/"+carpeta_frames+"/right")
        if f.lower().endswith(('.png', '.bmp'))
    ])

    if not fitxers_left or not fitxers_right:
        print("No s'han trobat imatges a la carpeta.")
        return

    #print(f"Mostrant {len(fitxers)} frames...")

    for nom_fitxer in fitxers_left:
        ruta = os.path.join("assets/eyes_img/"+carpeta_frames+"/left", nom_fitxer)
        #print(f"{nom_fitxer}")

        # Obre i redimensiona la imatge si cal
        imatge = Image.open(ruta).convert("1").resize((WIDTH, HEIGHT))
        left_eye.display(imatge)
        time.sleep(config.EYE_DELAY)
    
    for nom_fitxer in fitxers_right:
        ruta = os.path.join("assets/eyes_img/"+carpeta_frames+"/right", nom_fitxer)

        # Obre i redimensiona la imatge si cal
        imatge = Image.open(ruta).convert("1").resize((WIDTH, HEIGHT))
        right_eye.display(imatge)
        time.sleep(config.EYE_DELAY)
"""

class Display:
    """Classe per gestionar displays"""
    def __init__(self,width=config.OLED_WIDTH, height=config.OLED_HEIGHT, bus=None, address=0x3C):
        self.serial2 = i2c(port=bus, address=address)
        self.display = ssd1306(self.serial2, width=width, height=height)
        self.image = Image.new("1", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.width = width
        self.height = height
        self.max_lines = height // 10
        self.line_cache = []

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.display.display(self.image)    

    def display_message(self,text):
        global line_cache

        # Afegeix la nova línia al final
        line_cache.append(text)

        # Si tenim més línies del que cap, elimina les més antigues
        if len(line_cache) > self.max_lines:
            line_cache = line_cache[-self.max_lines:]

        # Esborra la imatge
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Escriu totes les línies del buffer
        for i, line in enumerate(line_cache):
            y = i * 10
            self.draw.text((0, y), line, fill=255)

        # Actualitza les dues pantalles
        self.display.display(self.image)

    def show_frames(self,carpeta_frames,side="left",eye_delay=config.EYE_DELAY):
        # Llegeix i ordena els fitxers de la carpeta
        fitxers = sorted([
            f for f in os.listdir("assets/eyes_img/"+carpeta_frames+"/"+side)
            if f.lower().endswith(('.png', '.bmp'))
        ])

        if not fitxers:
            print("No s'han trobat imatges a la carpeta.")
            return

        #print(f"Mostrant {len(fitxers)} frames...")

        for nom_fitxer in fitxers:
            ruta = os.path.join("assets/eyes_img/"+carpeta_frames+"/"+side, nom_fitxer)
            #print(f"{nom_fitxer}")

            # Obre i redimensiona la imatge si cal
            imatge = Image.open(ruta).convert("1").resize((self.width, self.height))
            self.display.display(imatge)
            time.sleep(eye_delay)

display_right = None
display_left = None

def start_displays():
    """Inicialitza les pantalles OLED"""
    global display_right, display_left

    try:
        display_right = Display(width=config.OLED_WIDTH, height=config.OLED_HEIGHT, bus=config.I2C_BUS_OLED_RIGHT)
        display_left = Display(width=config.OLED_WIDTH, height=config.OLED_HEIGHT, bus=config.I2C_BUS_OLED_LEFT)
        return True
    except Exception as e:
        print(f"[ERROR] Displays: {e}")
        return False

def clear_displays():
    if display_left is None or display_right is None:
        print("No es pot Netejar les pantalles, no estan inicialitzades")
        return
    display_left.clear()
    display_right.clear()

def displays_message(text):
    """Mostra un missatge a les pantalles OLED"""
    if display_left is None or display_right is None:
        print(text)
        return
    display_left.display_message(text)
    display_right.display_message(text)

def displays_show_frames(carpeta_frames, eye_delay=config.EYE_DELAY):
    if display_left is None or display_right is None:
        print("Displays no inicialitzats")
        return
    """Mostra els frames d'animació a les pantalles OLED"""
    display_left.show_frames(carpeta_frames, "left", eye_delay)
    display_right.show_frames(carpeta_frames, "right", eye_delay)