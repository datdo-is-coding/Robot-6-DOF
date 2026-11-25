import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

# 4 Holes PCD 44 mm:
delta_h = 22.0 / math.sqrt(2)
HOLES = {
    "H3": (CX - delta_h, CY - delta_h), # NW (84.444, 84.444)
    "H4": (CX + delta_h, CY - delta_h), # NE (115.556, 84.444)
    "H2": (CX - delta_h, CY + delta_h), # SW (84.444, 115.556)
    "H1": (CX + delta_h, CY + delta_h), # SE (115.556, 115.556)
}
R_SCREW_KEEPOUT = 3.0

placements = {}

# 1. MOUNTING HOLES (4)
placements["H3"] = (84.444, 84.444, 0, 5.0, 5.0, "both")
placements["H4"] = (115.556, 84.444, 0, 5.0, 5.0, "both")
placements["H2"] = (84.444, 115.556, 0, 5.0, 5.0, "both")
placements["H1"] = (115.556, 115.556, 0, 5.0, 5.0, "both")

# 2. WEST CONNECTOR BANK (J8: CAN_IN, J9: CAN_OUT, J10: SWD)
# Facing West (rot=90).
# In KiCad rot=90:
# Pad 1 is at (x, y). Shroud extends towards -X by 9.7 mm. Back extends towards +X by 2.81 mm.
# Y span: for 3p (J8, J9): from y - 2.45 to y + 7.45 (total width in Y = 9.9 mm).
# Y span: for 5p (J10): from y - 2.45 to y + 12.45 (total width in Y = 14.9 mm).
# Let's set x_pin = 78.0.
# Shroud front is at x = 78.0 - 9.7 = 68.3 mm.
# Shroud back is at x = 78.0 + 2.81 = 80.81 mm < 81.44 (clears H3 and H2 keepouts!).
# Let's arrange along Y:
# Total height = J10 (14.9) + 2.0 + J8 (9.9) + 2.0 + J9 (9.9) = 38.7 mm.
# Y span centered around Y=100: [80.65, 119.35].
# Let's place J10 at y_pin = 85.0: Y range [82.55, 97.45]
# Let's place J8  at y_pin = 100.0: Y range [97.55, 107.45]
# Let's place J9  at y_pin = 110.0: Y range [107.55, 117.45]
placements["J10"] = (78.0, 85.0, 90, 12.51, 14.9, "top")
placements["J8"]  = (78.0, 100.0, 90, 12.51, 9.9, "top")
placements["J9"]  = (78.0, 110.0, 90, 12.51, 9.9, "top")

# 3. SOUTH CONNECTOR: J7 USB TYPE-C
# Centered at x=100.0, y=125.0, rot=0 (facing South).
# Mouth at y = 125.0 + 3.75 = 128.75 mm <= 130.0 mm.
placements["J7"] = (100.0, 124.0, 0, 9.0, 8.5, "top")

# 4. EAST CONNECTOR: J11 XT30PW-M (rot=270, facing East)
# Front mouth towards +X (East).
# Pad pins at x = 124.0, y = 100.0.
placements["J11"] = (124.0, 100.0, 90, 11.0, 12.5, "top")
placements["F1"]  = (124.0, 110.0, 90, 7.0, 13.0, "top")
placements["D6"]  = (124.0, 118.0, 90, 4.0, 5.5, "top")

# 5. MOTOR PHASE TERMINALS & POWER STAGE (North)
placements["J1"] = (88.0, 73.0, 0, 3.2, 3.2, "top")
placements["J2"] = (100.0, 72.0, 0, 3.2, 3.2, "top")
placements["J3"] = (112.0, 73.0, 0, 3.2, 3.2, "top")

print(f"Key components placed: {len(placements)}")

# Check collisions among key components and holes:
keys = list(placements.keys())
overlap_errors = []
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        k1, k2 = keys[i], keys[j]
        c1, c2 = placements[k1], placements[k2]
        dx = abs(c1[0] - c2[0])
        dy = abs(c1[1] - c2[1])
        min_dx = (c1[3] + c2[3]) / 2.0
        min_dy = (c1[4] + c2[4]) / 2.0
        if dx < min_dx and dy < min_dy:
            overlap_errors.append(f"Overlap {k1} and {k2}: dx={dx:.2f} < {min_dx:.2f}, dy={dy:.2f} < {min_dy:.2f}")

print("Overlap errors:", len(overlap_errors))
for err in overlap_errors:
    print(" ", err)

# Check boundary:
boundary_errors = []
for k, c in placements.items():
    x, y, _, w, h, _ = c
    for px in [x - w/2, x + w/2]:
        for py in [y - h/2, y + h/2]:
            d = math.hypot(px - CX, py - CY)
            if d > 35.0:
                boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) distance {d:.2f} > 35.0")
print("Boundary errors:", len(boundary_errors))
for err in boundary_errors:
    print(" ", err)
