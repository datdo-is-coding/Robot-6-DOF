import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

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
placements["H3"] = (84.444, 84.444, 0, 6.0, 6.0, "both")
placements["H4"] = (115.556, 84.444, 0, 6.0, 6.0, "both")
placements["H2"] = (84.444, 115.556, 0, 6.0, 6.0, "both")
placements["H1"] = (115.556, 115.556, 0, 6.0, 6.0, "both")

# 2. MOTOR PHASE TERMINALS (North, deep inside board: clearance > 4.5 mm)
placements["J1"] = (88.0, 73.0, 0, 3.0, 3.0, "top")  # Phase U
placements["J2"] = (100.0, 72.0, 0, 3.0, 3.0, "top") # Phase V
placements["J3"] = (112.0, 73.0, 0, 3.0, 3.0, "top") # Phase W

# 3. 6 MOSFETs in clean horizontal row (TDSON-8: 5.3 x 6.4 mm)
placements["Q1"] = (86.0, 78.5, 0, 5.3, 6.4, "top")
placements["Q2"] = (91.5, 78.5, 180, 5.3, 6.4, "top")
placements["Q3"] = (97.5, 78.5, 0, 5.3, 6.4, "top")
placements["Q4"] = (103.0, 78.5, 180, 5.3, 6.4, "top")
placements["Q5"] = (109.0, 78.5, 0, 5.3, 6.4, "top")
placements["Q6"] = (114.5, 78.5, 180, 5.3, 6.4, "top")

# Ceramic DC-bus caps (1210: 2.8 x 3.5 mm)
placements["C_BUS1"] = (83.0, 73.0, 0, 3.5, 2.8, "top")
placements["C_BUS2"] = (94.5, 73.0, 0, 3.5, 2.8, "top")
placements["C_BUS3"] = (106.5, 73.0, 0, 3.5, 2.8, "top")

# 3 Shunts (2512: 3.6 x 6.7 mm, rot=90)
placements["R47"] = (91.5, 86.0, 90, 3.6, 6.7, "top")
placements["R48"] = (103.0, 86.0, 90, 3.6, 6.7, "top")
placements["R49"] = (114.5, 86.0, 90, 3.6, 6.7, "top")

# Kelvin net-ties (placed directly on shunt sense pads)
placements["NT1"] = (91.5, 84.45, 90, 0.8, 0.8, "top")
placements["NT2"] = (91.5, 87.55, 90, 0.8, 0.8, "top")
placements["NT3"] = (103.0, 84.45, 90, 0.8, 0.8, "top")
placements["NT4"] = (103.0, 87.55, 90, 0.8, 0.8, "top")
placements["NT5"] = (114.5, 84.45, 90, 0.8, 0.8, "top")
placements["NT6"] = (114.5, 87.55, 90, 0.8, 0.8, "top")

# Gate resistors (0603: 1.8 x 1.0 mm) at y=82.5
placements["R1"] = (88.0, 82.5, 0, 1.8, 1.0, "top")
placements["R2"] = (91.0, 82.5, 0, 1.8, 1.0, "top")
placements["R3"] = (97.5, 82.5, 0, 1.8, 1.0, "top")
placements["R4"] = (100.5, 82.5, 0, 1.8, 1.0, "top")
placements["R5"] = (109.0, 82.5, 0, 1.8, 1.0, "top")
placements["R7"] = (112.0, 82.5, 0, 1.8, 1.0, "top")

# Bulk electrolytic caps (D10.0 mm):
placements["C_BULK1"] = (75.0, 86.0, 0, 10.5, 10.5, "top")
placements["C63"]     = (124.0, 86.0, 0, 10.5, 10.5, "top")

# 4. DRV8323RS (IC1) centered at x=100.0, y=94.0
placements["IC1"] = (100.0, 94.0, 0, 7.5, 7.5, "top")

# Bootstrap caps (0603: 1.0 x 1.8 mm, rot=90)
placements["C1"] = (94.5, 90.5, 90, 1.0, 1.8, "top")
placements["C2"] = (94.5, 92.5, 90, 1.0, 1.8, "top")
placements["C3"] = (94.5, 94.5, 90, 1.0, 1.8, "top")

# DRV charge pump & bypass caps:
placements["C12"] = (94.5, 97.0, 90, 1.6, 2.4, "top") # 0805
placements["C13"] = (94.5, 99.2, 90, 1.0, 1.8, "top") # 0603
placements["C15"] = (105.5, 90.5, 90, 1.0, 1.8, "top") # 0603
placements["C18"] = (105.5, 92.5, 90, 1.0, 1.8, "top") # 0603
placements["C19"] = (105.5, 94.5, 90, 1.0, 1.8, "top") # 0603
placements["C20"] = (105.5, 96.5, 90, 1.0, 1.8, "top") # 0603
placements["C21"] = (105.5, 98.2, 90, 0.8, 1.2, "top") # 0402
placements["C64"] = (105.5, 100.0, 90, 1.0, 1.8, "top") # 0603

# DRV config resistors (0603: 1.8 x 1.0 mm)
placements["R6"]  = (92.0, 90.5, 0, 1.8, 1.0, "top")
placements["R8"]  = (92.0, 92.0, 0, 1.8, 1.0, "top")
placements["R9"]  = (92.0, 93.5, 0, 1.8, 1.0, "top")
placements["R10"] = (92.0, 95.0, 0, 1.8, 1.0, "top")
placements["R50"] = (92.0, 96.5, 0, 1.8, 1.0, "top")
placements["R51"] = (92.0, 98.0, 0, 1.8, 1.0, "top")
placements["R52"] = (92.0, 99.5, 0, 1.8, 1.0, "top")

placements["R55"] = (108.0, 90.5, 0, 1.8, 1.0, "top")
placements["R56"] = (108.0, 92.0, 0, 1.8, 1.0, "top")
placements["R57"] = (108.0, 93.5, 0, 1.8, 1.0, "top")
placements["R58"] = (108.0, 95.0, 0, 1.8, 1.0, "top")
placements["R59"] = (108.0, 96.5, 0, 1.8, 1.0, "top")
placements["R60"] = (108.0, 98.0, 0, 1.8, 1.0, "top")

placements["TP1"] = (86.0, 89.0, 0, 1.5, 1.5, "top")

# 5. CURRENT SENSE RC FILTERS (between IC1 and U1)
placements["R37"] = (95.0, 101.5, 0, 1.8, 1.0, "top")
placements["C54"] = (97.5, 101.5, 0, 1.8, 1.0, "top")
placements["R38"] = (99.5, 101.5, 0, 1.8, 1.0, "top")
placements["C55"] = (102.0, 101.5, 0, 1.8, 1.0, "top")
placements["R39"] = (104.5, 101.5, 0, 1.8, 1.0, "top")
placements["C56"] = (107.0, 101.5, 0, 1.8, 1.0, "top")

# 6. POWER INPUT & BUCK CONVERTER (East side)
# XT30PW-M (rot=-90 facing East, pins at x=120.0, y=98.0)
placements["J11"] = (120.0, 98.0, -90, 15.85, 14.3, "top")
# Fuse Keystone 3568 at y=111.0
placements["F1"]  = (123.0, 111.0, 90, 7.0, 13.0, "top")
# TVS SMBJ30A at y=120.0
placements["D6"]  = (122.0, 120.0, 90, 4.0, 5.5, "top")

# Buck converter:
placements["L1"]  = (115.0, 93.5, 0, 6.5, 6.5, "top")
placements["D4"]  = (115.0, 99.0, 0, 5.2, 2.8, "top")
placements["C16"] = (117.5, 103.0, 90, 1.6, 2.4, "top")
placements["C17"] = (115.0, 103.0, 90, 1.6, 2.4, "top")
placements["R53"] = (109.5, 95.0, 90, 1.0, 1.8, "top")
placements["R54"] = (109.5, 97.5, 90, 1.0, 1.8, "top")

# 7. MICROCONTROLLER SUBSYSTEM (STM32F405 U1)
placements["U1"] = (100.0, 109.5, 0, 12.2, 12.2, "top")

# Decoupling caps
placements["C4"]  = (97.0, 102.8, 0, 1.2, 0.8, "top")
placements["C5"]  = (103.0, 102.8, 0, 1.2, 0.8, "top")
placements["C10"] = (97.0, 116.5, 0, 1.2, 0.8, "top")
placements["C11"] = (103.0, 116.5, 0, 1.2, 0.8, "top")
placements["C6"]  = (107.5, 107.5, 90, 0.8, 1.2, "top")
placements["C7"]  = (107.5, 109.5, 90, 0.8, 1.2, "top")
placements["C50"] = (107.5, 111.5, 90, 0.8, 1.2, "top")
placements["C51"] = (92.5, 107.0, 90, 0.8, 1.2, "top")
placements["C52"] = (92.5, 109.0, 90, 0.8, 1.2, "top")
placements["C53"] = (92.5, 111.0, 90, 1.0, 1.8, "top")

# VDDA filter:
placements["FB1"] = (89.5, 103.0, 0, 1.8, 1.0, "top")

# 12MHz Crystal & load caps:
placements["Y1"]  = (87.5, 106.0, 0, 3.5, 2.8, "top")
placements["C8"]  = (85.0, 105.0, 90, 0.8, 1.2, "top")
placements["C9"]  = (85.0, 107.0, 90, 0.8, 1.2, "top")
placements["R44"] = (87.5, 108.5, 0, 1.8, 1.0, "top")

# Boot & Reset:
placements["R32"] = (87.5, 110.5, 0, 1.2, 0.8, "top")
placements["R34"] = (87.5, 112.0, 0, 1.2, 0.8, "top")

# 3.3V LDO U10 (SOT-23-5: 3.1 x 3.0 mm)
placements["U10"] = (110.0, 106.0, 0, 3.1, 3.0, "top")
placements["C57"] = (112.5, 105.0, 90, 1.0, 1.8, "top")
placements["C58"] = (112.5, 107.0, 90, 1.0, 1.8, "top")

# Status LEDs & resistors (neat bank at x=107..109, y=117..120)
placements["D1"]  = (107.5, 116.5, 0, 1.8, 1.0, "top")
placements["R33"] = (109.5, 116.5, 0, 1.2, 0.8, "top")
placements["D2"]  = (107.5, 118.0, 0, 1.8, 1.0, "top")
placements["R35"] = (109.5, 118.0, 0, 1.2, 0.8, "top")
placements["D3"]  = (107.5, 119.5, 0, 1.8, 1.0, "top")
placements["R36"] = (109.5, 119.5, 0, 1.2, 0.8, "top")

# 8. WEST SIDE: SWD PROGRAMMING CONNECTOR (J10)
# S5B-XH-A: width 15.9, height 12.51 mm, rot=90 facing West
placements["J10"] = (76.5, 95.0, 90, 12.51, 15.9, "top")

# 9. SOUTH CONNECTORS: J8 (CAN_IN), J9 (CAN_OUT), J7 (Type-C)
# J8 at x_pin=88.5, J9 at x_pin=99.0, J7 at x_pin=109.0
placements["J8"] = (88.5, 122.0, 0, 10.9, 12.51, "top")
placements["J9"] = (99.0, 122.0, 0, 10.9, 12.51, "top")
placements["J7"] = (109.0, 127.55, 0, 10.64, 9.42, "top")

# 10. CAN BUS PASSIVES (West side, near J8)
placements["U9"]  = (76.0, 117.5, 0, 3.2, 3.2, "top") # TJA1051
placements["C60"] = (73.5, 116.0, 90, 1.0, 1.8, "top")
placements["C61"] = (73.5, 118.0, 90, 1.0, 1.8, "top")
placements["C62"] = (73.5, 120.0, 90, 1.0, 1.8, "top")
placements["R45"] = (76.0, 120.5, 90, 1.0, 1.8, "top")
placements["R46"] = (76.0, 122.5, 90, 1.0, 1.8, "top")
placements["JP1"] = (76.0, 113.5, 0, 2.0, 2.0, "top")

# 11. USB CIRCUIT PASSIVES (East of J7 / South of H1)
placements["U8"]  = (118.0, 123.5, 0, 3.1, 3.0, "top") # USBLC6-2SC6
placements["R40"] = (118.0, 126.0, 0, 1.8, 1.0, "top")
placements["R41"] = (118.0, 127.5, 0, 1.8, 1.0, "top")
placements["Q7"]  = (115.0, 123.5, 0, 3.0, 2.5, "top") # 2N7002
placements["R42"] = (115.0, 126.0, 0, 1.8, 1.0, "top")
placements["R43"] = (115.0, 127.5, 0, 1.8, 1.0, "top")
placements["C59"] = (115.0, 129.0, 0, 1.8, 1.0, "top")

# 12. ENCODER & PASSIVES (B.Cu - bottom layer)
placements["U2"]  = (100.0, 100.0, 0, 3.2, 3.2, "bottom") # MA730
placements["C14"] = (100.0, 103.0, 0, 1.8, 1.0, "bottom")
placements["R61"] = (100.0, 97.0, 0, 1.8, 1.0, "bottom")
placements["TP2"] = (96.5, 100.0, 0, 1.5, 1.5, "bottom")
placements["TP3"] = (103.5, 100.0, 0, 1.5, 1.5, "bottom")

# ==========================================================
# VERIFICATION SUITE
# ==========================================================
print(f"Total placed components: {len(placements)}")

# NetTie pairs are allowed to overlap their respective shunt
ALLOWED_OVERLAPS = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

overlap_errors = []
keys = list(placements.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        k1, k2 = keys[i], keys[j]
        if (k1, k2) in ALLOWED_OVERLAPS or (k2, k1) in ALLOWED_OVERLAPS:
            continue
        c1, c2 = placements[k1], placements[k2]
        
        l1, l2 = c1[5], c2[5]
        if not ((l1 == l2) or (l1 == "both") or (l2 == "both")):
            continue
            
        if k1 in HOLES:
            hx, hy = c1[0], c1[1]
            rx, ry, _, rw, rh, _ = c2
            cx = max(rx - rw/2, min(hx, rx + rw/2))
            cy = max(ry - rh/2, min(hy, ry + rh/2))
            d = math.hypot(cx - hx, cy - hy)
            if d < R_SCREW_KEEPOUT:
                overlap_errors.append(f"Hole collision {k1} and {k2}: distance {d:.2f} < {R_SCREW_KEEPOUT}")
            continue
        if k2 in HOLES:
            hx, hy = c2[0], c2[1]
            rx, ry, _, rw, rh, _ = c1
            cx = max(rx - rw/2, min(hx, rx + rw/2))
            cy = max(ry - rh/2, min(hy, ry + rh/2))
            d = math.hypot(cx - hx, cy - hy)
            if d < R_SCREW_KEEPOUT:
                overlap_errors.append(f"Hole collision {k2} and {k1}: distance {d:.2f} < {R_SCREW_KEEPOUT}")
            continue
            
        dx = abs(c1[0] - c2[0])
        dy = abs(c1[1] - c2[1])
        min_dx = (c1[3] + c2[3]) / 2.0
        min_dy = (c1[4] + c2[4]) / 2.0
        if dx < min_dx and dy < min_dy:
            overlap_errors.append(f"Overlap {k1} ({c1[0]}, {c1[1]}) and {k2} ({c2[0]}, {c2[1]}): dx={dx:.2f} < {min_dx:.2f}, dy={dy:.2f} < {min_dy:.2f}")

print(f"Overlap errors: {len(overlap_errors)}")
for err in overlap_errors:
    print(" ", err)

# Board boundaries with flat cuts:
# Flat cuts:
# South flat cut at y = 132.0 (from x = 84.0 to 116.0)
# West flat cut at x = 66.5 (from y = 87.0 to 103.0)
# East flat cut at x = 134.0 (from y = 90.0 to 106.0)
# Everywhere else: R <= 35.0 mm.
boundary_errors = []
for k, c in placements.items():
    x, y, _, w, h, _ = c
    if k in ["C_BULK1", "C63"]:
        d = math.hypot(x - CX, y - CY) + 5.25
        if d > 35.5:
            boundary_errors.append(f"Boundary error {k}: cylinder radius {d:.2f} > 35.5")
        continue
    for px in [x - w/2, x + w/2]:
        for py in [y - h/2, y + h/2]:
            # check if inside flat cut regions or inside circle
            if py > 132.0:
                boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) y > 132.0")
            elif px < 66.5:
                boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) x < 66.5")
            elif px > 134.0:
                boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) x > 134.0")
            else:
                d = math.hypot(px - CX, py - CY)
                if d > 35.5 and not (py >= 122.0 or px <= 78.0 or px >= 122.0):
                    boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) radius {d:.2f} > 35.5")

print(f"Boundary errors: {len(boundary_errors)}")
for err in boundary_errors:
    print(" ", err)
