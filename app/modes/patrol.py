import config
import time


class Patrol:

    def __init__(self, camera=None):
        self.active = False
        self.camera = camera