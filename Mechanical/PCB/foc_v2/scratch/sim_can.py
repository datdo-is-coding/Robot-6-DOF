import math

# Footprint courtyards:
# U9: X: [-2.13, 2.13], Y: [-1.75, 1.75]
# JP1: X: [-1.65, 1.65], Y: [-1.25, 1.25]
# R45, R46: X: [-1.48, 1.48], Y: [-0.73, 0.73] (if rot=0), or X: [-0.73, 0.73], Y: [-1.48, 1.48] (if rot=90)
# C60: (71.5, 94.0), C61: (71.5, 97.5), C62: (71.5, 101.0)
# D1: (74.5, 101.5), R33: (77.5, 101.5)
# D2: (74.5, 103.5), R35: (77.5, 103.5)
# D3: (74.5, 105.2), R36: (77.5, 105.2)

# Notice: D1, D2, D3 and R33, R35, R36 are LEDs and resistors!
# And J8 is at Y = 110.30!
# There is plenty of space between Y = 96 and Y = 101.

# Let's test combinations:
# Can R45 and R46 be at Y = 98.8 and Y = 98.8?
# What if JP1 is at (73.5, 97.5, 90)?
# Local of JP1: rot 90 => X: [-1.25, 1.25], Y: [-1.65, 1.65].

def check_box(b1, b2):
    # b = (xmin, xmax, ymin, ymax)
    return not (b1[1] <= b2[0] or b1[0] >= b2[1] or b1[3] <= b2[2] or b1[2] >= b2[3])

print("Checking layout options...")
