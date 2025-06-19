import math
import time
import config
import board
import busio
import numpy as np
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import threading
from sensors.ultrasonic import ModulUltrasons
from movement.simulation_data import positions, walk_states

# Inicialització del bus I2C i la controladora PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz és l’estàndard per a servos

# Inicialitza els 10 primers canals com a servos
servos = []
for i in range(16):
    s = servo.Servo(pca.channels[i], min_pulse=500, max_pulse=2500)
    servos.append(s)


class Pota:
    def __init__(self, cadera, genoll,right,front):
        self.servo_up = cadera
        self.servo_down = genoll
        self.state = "sit"  # Estat inicial de la pota
        self.right = right  
        self.front = front
        self.old_state = "start"

    def set_new_position(self,t):
        pos = get_angle(self.state,self.right)
        old_pos = get_angle(self.old_state,self.right)

        t1 = threading.Thread(target=new_angle, args=(self.servo_up,pos[0],old_pos[0],t))
        t1.start()
        
        t2 = threading.Thread(target=new_angle, args=(self.servo_down,pos[1],old_pos[1],t))
        t2.start()

        t1.join()
        t2.join()


    def up(self):
        assert self.state != "up", "Already in 'up' position"
        assert self.state != "sit", "Cannot go to 'up' from 'sit' position"
        assert self.state in ["center", "front", "back", "long_front", "long_back"], "State must be one of 'center', 'front', 'back', 'long_front', or 'long_back'"

        self.set_state("up")

    def down(self, new_state):
        assert self.state == "up", "Can only go to from 'up' positions"
        assert new_state in ["center", "front", "back", "long_back"], "New state must be one of 'center', 'front', or 'back'"

        self.set_state(new_state)

    def forward(self):  
        assert self.state != "long_front", "Cannot move backward from 'long_front' position"

        if self.state == "front": self.set_state("long_front")
        if self.state == "center": self.set_state("front")
        if self.state == "back": self.set_state("center")
        if self.state == "long_back": self.set_state("back")

    def backward(self):
        assert self.state != "long_back", "Cannot move forward from 'long_back' position"

        if self.state == "back": self.set_state("long_back")
        if self.state == "center": self.set_state("back")
        if self.state == "front": self.set_state("center")
        if self.state == "long_front": self.set_state("front")
    
    def set_state(self, new_state):
        """Estableix un nou estat per a la pota."""
        assert new_state in positions.keys(), "Invalid state"
        self.old_state = self.state
        self.state = new_state
    

class EstructuraPotes:
    """Classe per gestionar les potes del quadrúpede."""
    def __init__(self,ultrasons: ModulUltrasons=None):
        self.ultrasons:ModulUltrasons = ultrasons

        self.legs = [
            Pota(servos[11], servos[10], True,True),  # Pota 1
            Pota(servos[13], servos[12], False,True),  # Pota 2
            Pota(servos[3], servos[2], True, False),  # Pota 3
            Pota(servos[7], servos[6], False, False)   # Pota 4
        ]
        threads = []

        for leg in self.legs:
            t = threading.Thread(target=leg.set_new_position, args=(0.3,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    
    def set_body_state(self,text):
        for leg in self.legs:
            leg.set_state(text)    

    def set_position(self,text):
        for leg in self.legs:
            leg.set_state(text)
        threads = []
        for leg in self.legs:
            th = threading.Thread(target=leg.set_new_position, args=(0.3,))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()

    def body_forward(self):
        for leg in self.legs:
            leg.backward()

    def body_backward(self):
        for leg in self.legs:
            leg.forward()

    def body_upward(self):
        for leg in self.legs:
            leg.set_state("center")

    def body_downward(self):
        for leg in self.legs:
            leg.set_state("sit")
            
    def sit_hind_legs(self, t=0.2):
        """Sit using only the hind legs while front legs are raised."""
        # hind legs
        self.legs[2].set_state("sit")
        self.legs[3].set_state("sit")
        # raise front legs
        self.legs[0].set_state("up")
        self.legs[1].set_state("up")

        threads = []
        for leg in self.legs:
            th = threading.Thread(target=leg.set_new_position, args=(t,))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()
    """def init_bot(self,t):
        for leg in self.legs:
            leg.state = "sit"
            leg.set_new_position(t)"""
    
    #set_positions
    def get_states(self):
        return [leg.state for leg in self.legs]

    """def follow_order(self, order, states, t=1):"""
    def follow_order(self, order,states = None, t=1):
        legs = self.legs
        action, *args = order
        old_states = self.get_states()
        if action == 'move_body':
            if args[0] == "backward":
                self.body_backward()
                
            elif args[0] == "forward":
                self.body_forward()
                
            elif args[0] == "upward":
                self.body_upward()
                
            elif args[0] == "downward":
                self.body_downward()
            else:
                self.set_body_state(args[0])

        elif action == 'raise_leg':
            legs = [self.legs[args[0]]]
            self.legs[args[0]].up()        

        elif action == 'lower_leg':
            legs = [self.legs[args[0]]]
            self.legs[args[0]].down(args[1])

        new_states = self.get_states()
        #Function move Body
        """for leg in self.legs:
            t1 = threading.Thread(target=leg.set_new_position, args=(t,)).start()"""
        threads = []
        for leg in legs:
            th = threading.Thread(target=leg.set_new_position, args=(t,))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()
        return new_states

    def follow_sequance(self, sequance, cycles=1, t = 1):
        """states = self.init_bot()"""
        states = self.get_states()
        print(f"Initial states: {states}")

        for order in sequance["initial"]:
            states = self.follow_order(order, states, t)
            print(f"After order {order}: {states}")
        
        for _ in range(cycles):
            for order in sequance["cycle"]:
                if self.ultrasons and self.ultrasons.mesura_distancia() > config.LLINDAR_ULTRASONIC:
                    states = self.follow_order(order, states, t)
                    print(f"After order {order}: {states}")
            
        for order in sequance["end"]:
            states = self.follow_order(order, states, t)
            print(f"After order {order}: {states}")
        
        print(f"Final states: {states}")









def get_angle(state,right):
    (up, down) = positions[state]
    if right:
        up = 90 + up
        down = 180 - down
    else:
        up = 90 - up
        down = down
    return (up,down)

def new_angle(servo,angle_final,angle_inicial, duracio, passos=30):
    pas = (angle_final - angle_inicial) / passos
    delay = duracio / passos

    for i in range(passos + 1):
        angle_actual = angle_inicial + i * pas
        servo.angle = max(0, min(180, angle_actual))  # Protecció límits
        time.sleep(delay)

# Crear potes (ajusta els canals segons com els tinguis connectats)

def set_servo_angle(index, angle):
    """Posa un servo concret a un angle determinat."""
    if not (0 <= index < len(servos)):
        raise ValueError("Index de servo fora de rang.")
    if not (0 <= angle <= 180):
        raise ValueError("L'angle ha de ser entre 0 i 180 graus.")
    servos[index].angle = angle

def sweep_servo(index, delay=0.01):
    """Mou el servo d'un extrem a l'altre per provar el rang complet."""
    if not (0 <= index < len(servos)):
        raise ValueError("Index de servo fora de rang.")

    # Anada: de 0 a 180 graus
    for angle in range(0, 181, 1):
        servos[index].angle = angle
        time.sleep(delay)

    # Tornada: de 180 a 0 graus
    for angle in range(180, -1, -1):
        servos[index].angle = angle
        time.sleep(delay)

def mou_cap(index=15, inici=30, pic=90, final=60, duracio=2, passos=40):
    if not (0 <= index < len(servos)):
        raise ValueError("Index de servo fora de rang.")

    def interpolar(ang1, ang2):
        pas = (ang2 - ang1) / passos
        return [ang1 + i * pas for i in range(passos + 1)]

    angles = interpolar(inici, pic) + interpolar(pic, final)[1:]  # Evita duplicar el pic
    delay = duracio / len(angles)

    for angle in angles:
        servos[index].angle = max(0, min(180, angle))
        time.sleep(delay)

