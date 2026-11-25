import math

# Mounting holes
h2_x, h2_y = 84.444, 115.556
h1_x, h1_y = 115.556, 115.556

# What is the courtyard radius of H1, H2?
# M2.5 screw head: ISO 4762 cap screw radius = 2.25 mm.
# Courtyard radius: 2.45 mm or 2.70 mm.
r_hole = 2.45

# Connector dimensions in local coords (rot=0):
# J8, J9 (XH 3-pin):
# Pin 1 at (0, 0), Pin 2 at (2.5, 0), Pin 3 at (5.0, 0)
# Body X in [-2.56, 7.56], width = 10.12 mm
# Body Y in [-2.41, 9.31], length = 11.72 mm
# Front mating face at Y_local = 9.31
# Pin center along X is at X_local = 2.50 mm (center of 0..5)
# Relative to pin 1: X_min = -2.56, X_max = +7.56

# J10 (XH 5-pin):
# Pin 1 at (0, 0), Pin 5 at (10.0, 0)
# Body X in [-2.56, 12.56], width = 15.12 mm
# Body Y in [-2.41, 9.31], length = 11.72 mm
# Front mating face at Y_local = 9.31

# J7 (USB-C):
# Center at (0, 0)
# Body X in [-4.47, 4.47], width = 8.94 mm (CrtYd: [-5.32, 5.32], width = 10.64 mm)
# Body Y in [-3.675, 3.675], length = 7.35 mm (CrtYd: [-4.85, 4.18])
# Front mating face at Y_local = +3.79 (CrtYd: +4.18)

print("H2 at:", h2_x, h2_y)
print("H1 at:", h1_x, h1_y)
