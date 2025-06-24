from positions import coord_to_servo
from interpolation import interpolation


ALTURA = 0.5


def correction(position, correction_factor=(0,0))
    (A, B) = position
    (C, D) = correction_factor
    return (C(A), D(B))

def position_steps(old_position, new_position, steps, inter_method, correction_factor=(0,0))
    position_steps_list = []

    prev_postition_coord = None
    prev_positions_servo = None

    next_positions_coord = old_position
    next_positions_servo = correction(coord_to_servo(next_positions_coord), correction_factor)
    for i in range(steps):
        factor = (i+1) / steps
        prev_postition_coord = next_positions_coord
        prev_positions_servo = next_positions_servo

        next_positions_coord = interpolation(old_position, new_position, factor, method=inter_method, height=ALTURA)
        next_positions_servo = correction(coord_to_servo(next_positions_coord), correction_factor)

        position_steps_list.append(next_positions_servo)
    
    return position_steps_list
