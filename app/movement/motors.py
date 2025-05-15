import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Inicialitzacio del bus I2C i la controladora PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz és l’estàndard per a servos

servos = []
for i in range(10):
    s = servo.Servo(pca.channels[i])
    #s.set_pulse_width_range(min_pulse=600, max_pulse=2400)
    servos.append(s)

def set_servo_angle(servo, angle):
    if angle < 0 or angle > 180:
        raise ValueError("L'angle ha de ser entre 0 i 180 graus.")
    servo.angle = angle
    #print(f"Servo {servo} configurat a {angle} graus.")
    servos[0].angle = angle

def move_leg(number):
    if number < 0 or number > 3:
        raise ValueError("El número del cama ha de ser entre 0 i 3.")
