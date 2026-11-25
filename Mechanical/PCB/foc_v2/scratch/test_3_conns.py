import math
import itertools

CX, CY = 100.0, 100.0
R_BOARD = 35.0

delta = 22.0 / math.sqrt(2)
H2 = (100 - delta, 100 + delta) # (84.444, 115.556)
H1 = (100 + delta, 100 + delta) # (115.556, 115.556)
R_KO = 3.0

conns = {
    "J8": (9.9, 12.51),
    "J9": (9.9, 12.51),
    "J7": (8.94, 8.50)
}

def check_box(xmin, xmax, ymin, ymax):
    for px in [xmin, xmax]:
        for py in [ymin, ymax]:
            if math.hypot(px - CX, py - CY) > 34.8:
                return False
    for hx, hy in [H2, H1]:
        cx = max(xmin, min(hx, xmax))
        cy = max(ymin, min(hy, ymax))
        if math.hypot(cx - hx, cy - hy) < R_KO:
            return False
    return True

found = []
for perm in itertools.permutations(["J8", "J9", "J7"]):
    for y_front_int in range(1180, 1340, 2):
        y_front = y_front_int / 10.0
        for x_start_int in range(700, 950, 2):
            x_start = x_start_int / 10.0
            cur_x = x_start
            all_ok = True
            pos = {}
            for name in perm:
                w, h = conns[name]
                xmin = cur_x
                xmax = cur_x + w
                ymax = y_front
                ymin = y_front - h
                if not check_box(xmin, xmax, ymin, ymax):
                    all_ok = False
                    break
                pos[name] = (xmin, xmax, ymin, ymax)
                cur_x += w + 1.2
            if all_ok:
                found.append((y_front, x_start, perm, pos))

print(f"Total valid 3-connector (J8, J9, J7) placements found: {len(found)}")
if found:
    best = min(found, key=lambda f: abs((f[1] + sum(conns[c][0] for c in f[2])/2) - 100.0))
    print(f"Best: Y_front={best[0]}, X_start={best[1]}, Order={best[2]}")
    for name in best[2]:
        xmin, xmax, ymin, ymax = best[3][name]
        print(f"  {name:4s}: X [{xmin:.2f}, {xmax:.2f}], Y [{ymin:.2f}, {ymax:.2f}]")
# Append check for J7 in middle
mid_configs = [f for f in found if f[2] == ('J8', 'J7', 'J9')]
print(f"Found {len(mid_configs)} with J7 in the middle: J8 (CAN_IN) - J7 (Type-C) - J9 (CAN_OUT)")
if mid_configs:
    best = min(mid_configs, key=lambda f: abs((f[1] + (9.9 + 8.94 + 9.9 + 2.4)/2) - 100.0))
    print(f"Best J7 in middle: Y_front={best[0]}, X_start={best[1]}")
    for name in best[2]:
        xmin, xmax, ymin, ymax = best[3][name]
        print(f"  {name:4s}: X [{xmin:.2f}, {xmax:.2f}], Y [{ymin:.2f}, {ymax:.2f}]")
