import math

# Let's solve the South connector placement mathematically:
# Circle center: (100.0, 100.0), R = 35.0 mm.
# Mounting holes: H2 = (84.444, 115.556), H1 = (115.556, 115.556), keepout radius = 2.95 mm.
# Flat cut: Y = y_cut.

# Let's inspect the connectors:
# J8: CAN_IN (3-pin XH horizontal)
# J9: CAN_OUT (3-pin XH horizontal)
# J7: USB-C (GT-USB-7010ASV)
# J10: SWD (5-pin XH horizontal)

# What are the EXACT physical and courtyard boundaries of each connector?
# J8, J9:
# Pads at (0, 0), (2.5, 0), (5.0, 0).
# Physical body: X in [-2.45, 7.45] (width 9.9mm), Y in [-2.30, 9.20] (depth 11.5mm).
# Courtyard: X in [-2.95, 7.95] (width 10.9mm), Y in [-2.81, 9.70] (height 12.51mm).
# J10:
# Pads at (0, 0) .. (10.0, 0).
# Physical body: X in [-2.45, 12.45] (width 14.9mm), Y in [-2.30, 9.20] (depth 11.5mm).
# Courtyard: X in [-2.95, 12.95] (width 15.9mm), Y in [-2.81, 9.70] (height 12.51mm).
# J7:
# Physical body: X in [-4.47, 4.47] (width 8.94mm), Y in [-3.67, 3.67].
# Courtyard: X in [-5.32, 5.32] (width 10.64mm), Y in [-4.85, 4.18].

# Notice the depths:
# J7 is only 9.03 mm deep in courtyard! Front face is at y_orig + 3.79.
# J8, J9, J10 are 12.51 mm deep in courtyard! Front face is at y_orig + 9.20.

# If we align all their FRONT FACES along the South flat cut at Y = y_cut:
# J8, J9, J10 y_orig = y_cut - 9.20.
# J7 y_orig = y_cut - 3.79.

# Now: What if the order of connectors is:
# Option 1: J8, J9, J7, J10
# Option 2: J8, J7, J9, J10
# Option 3: J10, J8, J7, J9
# Option 4: J10, J7, J8, J9

# Let's test if ANY order can place all 4 connectors along the flat cut!
# To do this, let's test y_cut from 122.0 to 127.0 with step 0.1 mm,
# and test continuous x-positions!

def check_col(rx1, ry1, rx2, ry2, cx, cy, r):
    qx = max(rx1, min(cx, rx2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

def check_in_circle(rx1, ry1, rx2, ry2, R=35.0, cx=100.0, cy=100.0):
    for x in [rx1, rx2]:
        for y in [ry1, ry2]:
            if (x - cx)**2 + (y - cy)**2 > R**2:
                return False
    return True

print("Searching...")
found = []
import itertools

for y_cut in [122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0]:
    for order in itertools.permutations(['J8', 'J9', 'J7', 'J10']):
        # We need to find x_orig for c0, c1, c2, c3
        # Let's see: can we optimize x_orig directly?
        pass
