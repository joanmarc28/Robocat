import math
#STATES POSITION

# 1^2 = Y_PLANE^2 + X_PLANE^2
Y_PLANE = -0.85
X_PLANE = math.sqrt(1 - Y_PLANE**2)
Y_UP = -1/2

position_states = {
    #basic positions
    "start":            ( 0, -1/2),
    "sit"  :            ( 0,  -1/2),
    "normal":           (0.5, -0.5),
    "up":               (0, Y_PLANE),

    #short stand positions
    "center" :          (   0*X_PLANE,  Y_PLANE),
    "front":            ( 1/4*X_PLANE,  Y_PLANE),
    "back" :            (-1/4*X_PLANE,  Y_PLANE),

    #long stand positions
    "long_front" :      ( 1/2*X_PLANE, Y_PLANE),
    "long_back" :       (-1/2*X_PLANE, Y_PLANE),
    "ll_back" :         (-3/4*X_PLANE, Y_PLANE),
    
    #short stand positions
    "center_down" :          ( 0*X_PLANE,  Y_PLANE -0.1),
    "front_down":            ( 1/4*X_PLANE,Y_PLANE -0.1),
    "back_down" :            (-1/4*X_PLANE,Y_PLANE -0.1),

    #long stand positions
    "long_front_down" :      ( 1/2*X_PLANE, Y_PLANE -0.1),
    "long_back_down" :       (-1/2*X_PLANE, Y_PLANE -0.1),



    #short stand positions
    "center_up" :          ( 0*X_PLANE,  Y_PLANE +0.1),
    "front_up":            ( 1/4*X_PLANE,Y_PLANE +0.1),
    "back_up" :            (-1/4*X_PLANE,Y_PLANE +0.1),

    #long stand positions
    "long_front_up" :      ( 1/2*X_PLANE, Y_PLANE  +0.1),
    "long_back_up" :       (-1/2*X_PLANE, Y_PLANE  +0.1),


    "raise_1" : (1/4*X_PLANE,Y_UP),
    "raise_2" : ( 1/2*X_PLANE,Y_UP)
}


def position(state):
    if isinstance(state, list):
        return [position(substate) for substate in state]

    assert position_states.get(state) is not None,\
        f"State {state} has no position assigned"
    
    return position_states[state]

#STATE CHANGE
forwards_states = {
    "front"      : "long_front",
    "center"     : "front",   
    "back"       : "center",
    "long_back"  : "back",

    "front_up"      : "long_front_up",
    "center_up"     : "front_up",   
    "back_up"       : "center_up",
    "long_back_up"  : "back_up",

    "front_down"      : "long_front_down",
    "center_down"     : "front_down",   
    "back_down"       : "center_down",
    "long_back_down"  : "back_down",    
}

backwards_states = {
    "long_front" : "front",
    "front"      : "center",
    "center"     : "back",   
    "back"       : "long_back",

    "long_front_up" : "front_up",
    "front_up"      : "center_up",
    "center_up"     : "back_up",   
    "back_up"       : "long_back_up",

    "long_front_down" : "front_down",
    "front_down"      : "center_down",
    "center_down"     : "back_down",   
    "back_down"       : "long_back_down",
}

def forwards(old_state):
    if isinstance(old_state, list):
        return [backwards(old_substate) for old_substate in old_state]

    assert forwards_states.get(old_state) is not None,\
        f"State {old_state} has no position forwards state assigned"
    
    return forwards_states[old_state]

def backwards(old_state):
    if isinstance(old_state, list):
        return [forwards(old_substate) for old_substate in old_state]

    assert backwards_states.get(old_state) is not None,\
        f"State {old_state} has no position backwards state assigned"
    
    return backwards_states[old_state]

def upwards(states):
    return ["center" for _ in states]

def downwards(states):
    return ["sit" for _ in states]




# SEQUANCE
up_sequence = {
    "start": [("u", 4, "l")],
    "cycle": [],
    "end": []
}

sit_sequence = {
    "start": [("d", 4, "l")],
    "cycle": [],
    "end": []
}

# Define the walk states
walk_states = {
    "start" : [ ( 'u', 4, 'l'), ( 'f', 4, 'l'),
                ( 'f', 0, 'p'), ( 'f', 4, 'l'), ( 'f', 3, 'p')
    ],
    "cycle" : [ ('ff', 1, 'p'), ( 'f', 4, 'l'), ('ff', 2, 'p'), 
                ('ff', 0, 'p'), ( 'f', 4, 'l'), ('ff', 3, 'p')
    ],
    "end"   : [ ( 'f', 1, 'p'), ( 'f', 2, 'p'), 
                ( 'b', 4, 'l'), 
                ( 'd', 4, 'l')
    ]
}

rot_states = {
    "start" : [],
    "cycle" : [],
    "end" : []
}

# Initial state
rot_states["start"] = [
    ('u', 4, 'l'),
    ("center_up", [0,1,2,3], 'l'),
    ("center_down", [0], 'l')
]

# Cycle state
rot_states["cycle"] = [
    ('f', 0, 'p'),
    ('f', 4, 'l'),
    ('b', 0, 'l'),
    ('b', 4, 'l'),
]

# End state
rot_states["end"] = [   
    ('d', 4, 'l'),
]