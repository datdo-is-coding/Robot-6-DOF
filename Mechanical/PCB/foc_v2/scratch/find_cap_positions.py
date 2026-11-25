import math

cx, cy = 100.0, 100.0
R_board = 35.0
R_cap = 5.25 # capacitor radius including courtyard
R_max = R_board - R_cap # 29.75 mm

holes = [
    ("H3", 84.444, 84.444),
    ("H4", 115.556, 84.444),
    ("H2", 84.444, 115.556),
    ("H1", 115.556, 115.556)
]
R_ko = 3.0 # hole keepout

print(f"Max distance from (100, 100) for 10mm cap to be 100% inside board: {R_max:.2f} mm")

# Find valid regions for Left Cap (C_BULK1, x < 100) and Right Cap (C63, x > 100):
valid_left = []
valid_right = []

for x_i in range(650, 1350, 5):
    x = x_i / 10.0
    for y_i in range(650, 1350, 5):
        y = y_i / 10.0
        d_center = math.hypot(x - cx, y - cy)
        if d_center > R_max:
            continue
        # Check holes
        hole_ok = True
        for hname, hx, hy in holes:
            if math.hypot(x - hx, y - hy) < (R_cap + R_ko):
                hole_ok = False
                break
        if not hole_ok:
            continue
        
        if x < 85.0:
            valid_left.append((x, y, d_center))
        elif x > 115.0:
            valid_right.append((x, y, d_center))

print(f"Valid positions found: Left = {len(valid_left)}, Right = {len(valid_right)}")

# Let's inspect some candidates on Left:
print("\nLeft Cap candidates (sorted by x ascending):")
for x, y, d in sorted(valid_left, key=lambda p: p[0])[:10]:
    print(f"  Cap at ({x:.1f}, {y:.1f}): dist_center={d:.2f} mm")

print("\nRight Cap candidates (sorted by x descending):")
for x, y, d in sorted(valid_right, key=lambda p: -p[0])[:10]:
    print(f"  Cap at ({x:.1f}, {y:.1f}): dist_center={d:.2f} mm")
