
positions = {
    #basic positions
    "start": (  0.0,  0.0),
    "sit"  : (-60.0, 120.0),

    #short stand positions
    "center" : (-30.0, 60.0),
    "front": (  0.0, 45.0),
    "back" : (-45.0, 45.0),

    #long stand positions
    "long_front" : (30.0, 0.0),
    "long_back" : (-30.0, 0.0),

    #move postitions
    "up": (-60.0, 120.0),
}

walk_states = {
    "initial" : [],
    "cycle" : [],
    "end" : []
}

# Initial state
walk_states["initial"] = [
    ('move_body', 'upward'),
    ('raise_leg', 0),
    ('lower_leg', 0, 'front'),
    ('move_body', 'forward'),
    ('raise_leg', 3),
    ('lower_leg', 3, 'center'),
]

# Cycle state
walk_states["cycle"] = [
    ('raise_leg', 1),
    ('lower_leg', 1, 'front'),
    ('move_body', 'forward'),
    ('raise_leg', 2),
    ('lower_leg', 2, 'center'),

    ('raise_leg', 0),
    ('lower_leg', 0, 'front'),
    ('move_body', 'forward'),
    ('raise_leg', 3),
    ('lower_leg', 3, 'center'),
]

# End state
walk_states["end"] = [
    ('raise_leg', 1),
    ('lower_leg', 1, 'center'),
    ('move_body', 'forward'),
    ('raise_leg', 2),
    ('lower_leg', 2, 'back'),
    ('move_body', 'backward'),
    ('move_body', 'downward'),
]