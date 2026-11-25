import math

cx, cy = 100.0, 100.0
r = 35.0
y_cut = 120.2

# Calculate the exact intersection of circle R=35 with Y = 120.2:
# (x - 100)^2 + (120.2 - 100)^2 = 35^2
# (x - 100)^2 + 20.2^2 = 1225
# (x - 100)^2 + 408.04 = 1225
# (x - 100)^2 = 816.96
# x - 100 = +/- 28.5825
x_left = round(100.0 - math.sqrt(35**2 - (y_cut - 100)**2), 4)
x_right = round(100.0 + math.sqrt(35**2 - (y_cut - 100)**2), 4)

print(f"Y_cut = {y_cut}: X_left = {x_left}, X_right = {x_right}")
print(f"Chord length = {x_right - x_left:.2f} mm")

# Calculate arc midpoints for 5-segment watertight outline:
# 1. Top-Left: from (65, 100) to (100, 65), mid = (75.251262, 75.251262)
# 2. Top-Right: from (100, 65) to (135, 100), mid = (124.748737, 75.251262)
# 3. Bottom-Right: from (135, 100) to (x_right, y_cut)
# 4. Flat cut line: from (x_right, y_cut) to (x_left, y_cut)
# 5. Bottom-Left: from (x_left, y_cut) to (65, 100)

def get_arc_mid(x1, y1, x2, y2, cx=100.0, cy=100.0, r=35.0, ccw=False):
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    if not ccw:
        if a2 <= a1:
            a2 += 2 * math.pi
        amid = (a1 + a2) / 2
    else:
        if a2 >= a1:
            a2 -= 2 * math.pi
        amid = (a1 + a2) / 2
    return round(cx + r * math.cos(amid), 4), round(cy + r * math.sin(amid), 4)

mx3, my3 = get_arc_mid(135.0, 100.0, x_right, y_cut)
mx5, my5 = get_arc_mid(x_left, y_cut, 65.0, 100.0)

print(f"Arc 3 (BR) mid: ({mx3}, {my3})")
print(f"Arc 5 (BL) mid: ({mx5}, {my5})")
