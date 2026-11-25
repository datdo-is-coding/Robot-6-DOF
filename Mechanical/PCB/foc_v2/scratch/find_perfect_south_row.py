import math

# Center of board
CX, CY = 100.0, 100.0
R_BOARD = 35.0

# Holes PCD 44 mm:
delta = 22.0 / math.sqrt(2)
H2 = (100 - delta, 100 + delta) # (84.444, 115.556)
H1 = (100 + delta, 100 + delta) # (115.556, 115.556)
R_KO = 3.0 # keepout radius

# Dimensions of connectors:
# J8 (XH 3p): width 9.9 mm, depth 12.51 mm, pins at y_pin, front at y_pin + 9.70, back at y_pin - 2.81
#   Pads at x in [0, 5.0], body x in [-2.45, 7.45]
# J9 (XH 3p): same
# J10 (XH 5p): width 14.9 mm, depth 12.51 mm, pads at x in [0, 10.0], body x in [-2.45, 12.45]
# J7 (Type-C): width 8.94 mm, depth 8.5 mm (front at y_c + 3.75, back at y_c - 4.75)
#   Pads around center, body x in [-4.47, 4.47]

# Let's test if ALL 4 connectors can be placed along a straight line facing South:
# Permutations of [J8, J9, J7, J10]:
import itertools

conns = {
    "J8": (9.9, 12.51, 9.70, 2.81, 2.45), # w, h, front_offset, back_offset, left_pad_offset
    "J9": (9.9, 12.51, 9.70, 2.81, 2.45),
    "J10": (14.9, 12.51, 9.70, 2.81, 2.45),
    "J7": (8.94, 8.50, 3.75, 4.75, 4.47)
}

def check_box(xmin, xmax, ymin, ymax):
    # Check 4 corners against board circle R=35.0
    for px in [xmin, xmax]:
        for py in [ymin, ymax]:
            if math.hypot(px - CX, py - CY) > 34.8: # 0.2mm margin
                return False
    # Check distance to H2 and H1
    for hx, hy in [H2, H1]:
        # closest point in box to hole
        cx = max(xmin, min(hx, xmax))
        cy = max(ymin, min(hy, ymax))
        if math.hypot(cx - hx, cy - hy) < R_KO:
            return False
    return True

# Test permutations and spacing
found = []
for perm in itertools.permutations(["J8", "J9", "J7", "J10"]):
    # Let's test Y_front from 118.0 to 130.0 in steps of 0.2 mm
    for y_front_int in range(1180, 1300, 2):
        y_front = y_front_int / 10.0
        
        # Test X starting position
        for x_start_int in range(700, 800, 2):
            x_start = x_start_int / 10.0
            
            cur_x = x_start
            all_ok = True
            pos = {}
            for name in perm:
                w, h, f_off, b_off, l_off = conns[name]
                xmin = cur_x
                xmax = cur_x + w
                ymax = y_front
                ymin = y_front - h
                if not check_box(xmin, xmax, ymin, ymax):
                    all_ok = False
                    break
                pos[name] = (xmin, xmax, ymin, ymax)
                cur_x += w + 1.2 # 1.2 mm gap between connectors
                
            if all_ok:
                found.append((y_front, x_start, perm, pos))

print(f"Total valid 4-connector straight-line placements found: {len(found)}")
if found:
    # Print the best one (closest to center X=100)
    best = min(found, key=lambda f: abs((f[1] + sum(conns[c][0] for c in f[2])/2) - 100.0))
    print(f"Best configuration: Y_front={best[0]}, X_start={best[1]}, Order={best[2]}")
    for name in best[2]:
        xmin, xmax, ymin, ymax = best[3][name]
        print(f"  {name:4s}: X [{xmin:.2f}, {xmax:.2f}], Y [{ymin:.2f}, {ymax:.2f}]")
