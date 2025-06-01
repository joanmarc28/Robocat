# interface/display.py
from PIL import Image, ImageDraw
import board
import busio
import config
import os
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

WIDTH = config.OLED_WIDTH
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
