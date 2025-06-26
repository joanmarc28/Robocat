#from movement.inverse_kinematics.position import coord_to_servo
from movement.inverse_kinematics.interpolation import interpolation


ALTURA = 1/2

def position_steps(old_position, new_position, steps, inter_method, correction_factor=(0,0)):
    position_steps_list = []


    next_positions_coord = old_position
    #next_positions_servo = correction(coord_to_servo(next_positions_coord), correction_factor)
    for i in range(steps):
        factor = (i+1) / steps
        
        next_positions_coord = interpolation(old_position, new_position, factor, method=inter_method, height=ALTURA)
        #next_positions_servo = correction(coord_to_servo(next_positions_coord), correction_factor)

        position_steps_list.append(next_positions_coord)
    
    return position_steps_list
