import math
from itertools import permutations

# Connectors:
# 'J8': XH 3-pin
# 'J9': XH 3-pin
# 'J10': XH 5-pin
# 'J7': Type-C

h1_x, h1_y = 115.556, 115.556
h2_x, h2_y = 84.444, 115.556

def get_box(cname, px, py):
    if cname in ['J8', 'J9']:
        return (px - 2.56, px + 7.56, py - 2.41, py + 9.31)
    elif cname == 'J10':
        return (px - 2.56, px + 12.56, py - 2.41, py + 9.31)
    elif cname == 'J7':
        return (px - 5.32, px + 5.32, py - 4.85, py + 4.18)

def dist_box_pt(box, px, py):
    x1, x2, y1, y2 = box
    cx = max(x1, min(px, x2))
    cy = max(y1, min(py, y2))
    return math.hypot(cx - px, cy - py)

def inside_board(box, y_edge, r_board=35.0):
    x1, x2, y1, y2 = box
    if y2 > y_edge + 0.05:
        return False
    for x in [x1, x2]:
        for y in [y1, y2]:
            if math.hypot(x - 100.0, y - 100.0) > r_board:
                return False
    return True

# Test permutations
conns = ['J8', 'J7', 'J10', 'J9']
# Permutations of order
all_perms = list(permutations(conns))

results = []

for y_edge in [119.5, 120.0, 120.5, 121.0, 121.5, 122.0]:
    py_xh = y_edge - 9.31
    py_typec = y_edge - 4.18  # so CrtYd max reaches exactly y_edge
    
    # Board width at y_edge
    x_half = math.sqrt(35.0**2 - (y_edge - 100.0)**2)
    x_min_cut = 100.0 - x_half
    x_max_cut = 100.0 + x_half
    
    for perm in all_perms:
        # We need to choose x positions for each connector in order
        # Let's see: we want them arranged left to right
        # With clearance >= 0.5 mm between adjacent connectors
        # And clearance to H1, H2 >= 2.45 mm
        # We can optimize / search with fine steps or grid
        pass

print("Loaded connector search framework.")
