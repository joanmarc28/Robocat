import math
from movement.motors import Pota, moure_suau, servors

class PotaIK(Pota):
    def __init__(self, cadera, genoll, estats, L1, L2):
        super().__init__(servos[cadera], servos[genoll], estats)
        self.L1 = L1  # Longitud cuixa
        self.L2 = L2  # Longitud cama

    def calcula_angles_ik(self, x, y):
        # Distància fins al punt
        D = math.hypot(x, y)
        if D > (self.L1 + self.L2):
            raise ValueError("El punt està fora de l'abast de la pota!")

        # Angle del genoll (llei dels cosins)
        angle_genoll = math.acos((self.L1**2 + self.L2**2 - D**2) / (2 * self.L1 * self.L2))
        angle_genoll_deg = math.degrees(angle_genoll)

        # Angle del cuixa
        angle_a = math.atan2(y, x)
        angle_b = math.acos((D**2 + self.L1**2 - self.L2**2) / (2 * self.L1 * D))
        angle_cuixa_deg = math.degrees(angle_a + angle_b)

        return angle_cuixa_deg, angle_genoll_deg

    def moure_ik(self, x, y, duracio=1, part='tot'):
        angle_cuixa, angle_genoll = self.calcula_angles_ik(x, y)

        if part == 'tot':
            self.moure_a_parts_cama(angle_cuixa, angle_genoll, duracio)
        elif part == 'cuixa':
            self.moure_a_parts_cama(angle_cuixa, self.genoll.angle or 90, duracio)
        elif part == 'cama':
            self.moure_a_parts_cama(self.cadera.angle or 90, angle_genoll, duracio)
        else:
            raise ValueError("Part desconeguda, usa 'tot', 'cuixa' o 'cama'.")
