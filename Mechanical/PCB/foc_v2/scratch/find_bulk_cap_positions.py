import math

CX, CY = 100.0, 100.0
R_MAX = 35.0 - 5.25 # max distance from center to cylinder center = 29.75 mm

HOLES = {
    "H3": (84.444, 84.444),
    "H4": (115.556, 84.444),
    "H2": (84.444, 115.556),
    "H1": (115.556, 115.556)
}

R_HOLE_CLEARANCE = 2.95 + 5.25 # 8.20 mm

def is_valid_cap_center(cx, cy):
    # Within circular board
    d_center = math.hypot(cx - CX, cy - CY)
    if d_center > R_MAX:
        return False
    # Clear of all 4 holes
    for hname, (hx, hy) in HOLES.items():
        if math.hypot(cx - hx, cy - hy) < R_HOLE_CLEARANCE:
            return False
    return True

# Scan grid
valid_pts = []
for x in [i * 0.5 for i in range(140, 260)]:
    for y in [j * 0.5 for j in range(140, 260)]:
        if is_valid_cap_center(x, y):
            valid_pts.append((x, y))

print(f"Total valid candidate points for 10mm cap center: {len(valid_pts)}")

# Find clusters / regions
# Region 1: West / North-West
west = [p for p in valid_pts if p[0] < 82 and 75 < p[1] < 95]
print("West valid count:", len(west))
if west:
    print("Sample west points (center cx, cy):", west[:5])

# Region 2: East / North-East
east = [p for p in valid_pts if p[0] > 118 and 75 < p[1] < 95]
print("East valid count:", len(east))
if east:
    print("Sample east points (center cx, cy):", east[:5])
