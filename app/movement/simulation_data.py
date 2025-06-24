import math
#STATES POSITION

# 1^2 = Y_PLANE^2 + X_PLANE^2
Y_PLANE = -2/3
X_PLANE = math.sqrt(5)/3

position_states = {
    #basic positions
    "start":            ( 0, -1/2),
    "sit"  :            ( 0,  -1/2),
    "normal":           (0.5, -0.5),
    "up":               (0, -7/12),

    #short stand positions
    "center" :          (   0*X_PLANE,  Y_PLANE),
    "front":            ( 1/4*X_PLANE,  Y_PLANE),
    "back" :            (-1/4*X_PLANE,  Y_PLANE),

    #long stand positions
    "long_front" :      ( 1/2*X_PLANE, Y_PLANE),
    "long_back" :       (-1/2*X_PLANE, Y_PLANE),
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
}

backwards_states = {
    "long_front" : "front",
    "front"      : "center",
    "center"     : "back",   
    "back"       : "long_back",
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
    "start" : [ ( 'u', 4, 'l'), 
                ( 'f', 0, 'p'), ( 'f', 4, 'l'), ( 'f', 3, 'p')
    ],
    "cycle" : [ ('ff', 1, 'p'), ( 'f', 4, 'l'), ('ff', 2, 'p'), 
                ('ff', 0, 'p'), ( 'f', 4, 'l'), ('ff', 3, 'p')
    ],
    "end"   : [ ( 'f', 1, 'p'), ( 'f', 4, 'l'), ( 'f', 2, 'p'), 
                ( 'b', 4, 'l'), 
                ( 'd', 4, 'l')
    ]
}

