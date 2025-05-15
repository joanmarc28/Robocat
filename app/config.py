# config.py

# I2C pins (normalment no cal canviar, però pots sobreescriure)
I2C_SDA_PIN = 2      # GPIO2 (Pin 3)
I2C_SCL_PIN = 3      # GPIO3 (Pin 5)

# Pins de sensors, motors, etc.
ULTRASONIC_TRIG = 23
ULTRASONIC_ECHO = 24

SERVO_PIN_FRONT_LEFT = 17
SERVO_PIN_FRONT_RIGHT = 27
SERVO_PIN_BACK_LEFT = 22
SERVO_PIN_BACK_RIGHT = 10

# Pantalla OLED (configurable si tens dues)
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Mode de funcionament per defecte
DEFAULT_MODE = "Patrol"

# temps 
EYE_DELAY = 0.01
