from mpu6050 import mpu6050
import smbus2
import time

# Patching el bus dins la llibreria
mpu6050.smbus = smbus2.SMBus(6)  # força a usar el bus 6

sensor = mpu6050(0x68)

while True:
    accel = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()
    temp = sensor.get_temp()

    print(f"Accel: {accel}")
    print(f"Gyro: {gyro}")
    print(f"Temp: {temp}")
    time.sleep(0.5)
