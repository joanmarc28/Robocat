# config.py

# I2C pins 
I2C_BUS_OLED_LEFT = 3
I2C_BUS_OLED_RIGHT = 4
I2C_BUS_GPS = 5

# Pins de sensors, motors, etc.
ULTRASONIC_TRIG = 8
ULTRASONIC_ECHO = 23

#SERVO_PIN_FRONT_LEFT = 17

# Pantalla OLED
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Configuració de la càmera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
CAMERA_ROTATE = 0  # Rotació de la càmera en graus (0, 90, 180, 270)
CAMERA_FLIP = False  # Inverteix la imatge horitzontalment

# Mode de funcionament per defecte
DEFAULT_MODE = "Patrol"

# temps 
EYE_DELAY = 0.01

STATES_INFO = {"default":{
                "sounds": ["neutral_1_clean.wav"],

                }, 
                "happy":{
                    "sounds": ["cute_1_clean.wav"],

                },  
                "patrol":{
                    "sounds": ["angry_2_clean.wav"],

                },  
                "angry":{
                    "sounds": ["angry_1_clean.wav"],

                },  
                "sad":{
                    "sounds": ["sick_1_clean.wav"],

                }
            }
#STATES_INFO.