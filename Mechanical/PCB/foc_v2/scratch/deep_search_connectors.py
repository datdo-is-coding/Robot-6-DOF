import math

# Let's test all possible arrangements of J8, J9, J7, J10
# We want:
# 1. Zero DRC courtyard overlap with H1 and H2 (dist >= 2.95 mm from (84.444, 115.556) and (115.556, 115.556))
# 2. All connector courtyards strictly inside the circle R = 35.0 centered at (100, 100)
# 3. Connectors aligned in a straight line at South (same Y_front +/- 0.5mm)
# 4. Zero courtyard overlap between adjacent connectors

# Dimensions:
# J8, J9: crtyd [-2.95, 7.95] x [-2.81, 9.70] relative to (x, y) where pads are at y=0, front face at y=9.20
# J10: crtyd [-2.95, 12.95] x [-2.81, 9.70] relative to (x, y) where pads are at y=0, front face at y=9.20
# J7: crtyd [-5.32, 5.32] x [-4.85, 4.18] relative to (x, y) where front face is at y=3.79

# Can we shift y_orig slightly?
# What if y_front is at 124.0 .. 128.0?
# Let's search!

H2 = (84.444, 115.556, 2.95)
H1 = (115.556, 115.556, 2.95)

def point_in_circle(x, y, R=35.0, cx=100.0, cy=100.0):
    return (x - cx)**2 + (y - cy)**2 <= R**2

def rect_in_circle(x1, y1, x2, y2, R=35.0, cx=100.0, cy=100.0):
    for x in [x1, x2]:
        for y in [y1, y2]:
            if not point_in_circle(x, y, R, cx, cy):
                return False
    return True

def rect_circle_overlap(rx1, ry1, rx2, ry2, cx, cy, r):
    qx = max(rx1, min(cx, rx2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

import itertools

print("Running deep search...")
successes = []

for y_front in [124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 128.0]:
    for order in itertools.permutations(['J8', 'J9', 'J7', 'J10']):
        # We test candidate x-positions:
        # Since spacing is small, let's test if any order can place connectors
        # Let's see if J7 can be near H2 or H1, since J7 is shallower in Y!
        # J7 crtyd in Y: y_orig = y_front - 3.79.
        # J7 y_crtyd_min = y_front - 3.79 - 4.85 = y_front - 8.64!
        # For y_front = 125.0: J7 y_crtyd_min = 116.36!
        # That's already below H1/H2 center at 115.56!
        # For y_front = 127.0: J7 y_crtyd_min = 118.36!
        # That's almost completely below H1/H2!
        
        # What if J7 is at H2 or H1?
        # But J7 is USB-C, usually in the middle!
        pass

# Let's inspect J7:
print("J7 depth is only 8.64 mm, whereas XH is 12.51 mm deep!")
