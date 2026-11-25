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

# 2. MOTOR PHASE TERMINALS (North, clearance > 4.5 mm to edge)
placements["J1"] = (87.0, 72.5, 0, 3.0, 3.0, "top")  # Phase U
placements["J2"] = (100.0, 71.5, 0, 3.0, 3.0, "top") # Phase V
placements["J3"] = (113.0, 72.5, 0, 3.0, 3.0, "top") # Phase W

# 3. 6 MOSFETs in clean horizontal row (TDSON-8: 5.3 x 6.4 mm)
# Placed at y=77.5, well above H3/H4 keepout (y <= 81.44)
placements["Q1"] = (86.0, 77.5, 0, 5.3, 6.4, "top")
placements["Q2"] = (91.5, 77.5, 180, 5.3, 6.4, "top")
placements["Q3"] = (97.5, 77.5, 0, 5.3, 6.4, "top")
placements["Q4"] = (103.0, 77.5, 180, 5.3, 6.4, "top")
placements["Q5"] = (109.0, 77.5, 0, 5.3, 6.4, "top")
placements["Q6"] = (114.5, 77.5, 180, 5.3, 6.4, "top")

# Ceramic DC-bus caps (1210: 2.8 x 3.5 mm)
placements["C_BUS1"] = (82.0, 73.0, 0, 3.5, 2.8, "top")
placements["C_BUS2"] = (94.5, 73.0, 0, 3.5, 2.8, "top")
placements["C_BUS3"] = (106.0, 73.0, 0, 3.5, 2.8, "top")

# 3 Shunts (2512: 3.6 x 6.7 mm, rot=90) directly below low-side FETs
# Q2 is at x=91.5, Q4 is at x=103.0, Q6 is at x=114.5
placements["R47"] = (91.5, 84.5, 90, 3.6, 6.7, "top")
placements["R48"] = (103.0, 84.5, 90, 3.6, 6.7, "top")
placements["R49"] = (111.0, 84.5, 90, 3.6, 6.7, "top")

# Kelvin net-ties (NT1..NT6)
placements["NT1"] = (89.0, 84.5, 0, 0.8, 0.8, "top")
placements["NT2"] = (94.0, 84.5, 0, 0.8, 0.8, "top")
placements["NT3"] = (100.5, 84.5, 0, 0.8, 0.8, "top")
placements["NT4"] = (105.5, 84.5, 0, 0.8, 0.8, "top")
placements["NT5"] = (108.5, 84.5, 0, 0.8, 0.8, "top")
placements["NT6"] = (113.5, 84.5, 0, 0.8, 0.8, "top")

# Gate resistors (0603: 1.8 x 1.0 mm)
placements["R1"] = (86.0, 81.5, 0, 1.8, 1.0, "top")
placements["R2"] = (91.5, 81.5, 0, 1.8, 1.0, "top")
placements["R3"] = (97.5, 81.5, 0, 1.8, 1.0, "top")
placements["R4"] = (103.0, 81.5, 0, 1.8, 1.0, "top")
placements["R5"] = (107.0, 81.5, 0, 1.8, 1.0, "top")
placements["R7"] = (111.0, 81.5, 0, 1.8, 1.0, "top")

# Bulk electrolytic caps (D10.0 mm):
# C_BULK1 at x=75.5, y=86.0; C63 at x=122.0, y=84.0
placements["C_BULK1"] = (75.5, 86.0, 0, 10.5, 10.5, "top")
placements["C63"]     = (122.0, 84.0, 0, 10.5, 10.5, "top")

# 4. DRV8323RS (IC1) centered at x=100.0, y=94.5
placements["IC1"] = (100.0, 94.5, 0, 7.5, 7.5, "top")

# Bootstrap caps (0603: 1.0 x 1.8 mm, rot=90)
placements["C1"] = (94.5, 91.0, 90, 1.0, 1.8, "top")
placements["C2"] = (94.5, 93.0, 90, 1.0, 1.8, "top")
placements["C3"] = (94.5, 95.0, 90, 1.0, 1.8, "top")

# DRV charge pump & bypass caps:
placements["C12"] = (94.5, 97.5, 90, 1.6, 2.4, "top") # 0805
placements["C13"] = (94.5, 100.0, 90, 1.0, 1.8, "top") # 0603
placements["C15"] = (105.5, 91.0, 90, 1.0, 1.8, "top") # 0603
placements["C18"] = (105.5, 93.0, 90, 1.0, 1.8, "top") # 0603
placements["C19"] = (105.5, 95.0, 90, 1.0, 1.8, "top") # 0603
placements["C20"] = (105.5, 97.0, 90, 1.0, 1.8, "top") # 0603
placements["C21"] = (105.5, 99.0, 90, 0.8, 1.2, "top") # 0402
placements["C64"] = (105.5, 101.0, 90, 1.0, 1.8, "top") # 0603

# DRV config resistors (0603: 1.8 x 1.0 mm)
placements["R6"]  = (92.0, 91.0, 0, 1.8, 1.0, "top")
placements["R8"]  = (92.0, 92.5, 0, 1.8, 1.0, "top")
placements["R9"]  = (92.0, 94.0, 0, 1.8, 1.0, "top")
placements["R10"] = (92.0, 95.5, 0, 1.8, 1.0, "top")
placements["R50"] = (92.0, 97.0, 0, 1.8, 1.0, "top")
placements["R51"] = (92.0, 98.5, 0, 1.8, 1.0, "top")
placements["R52"] = (92.0, 100.0, 0, 1.8, 1.0, "top")

placements["R55"] = (108.0, 91.0, 0, 1.8, 1.0, "top")
placements["R56"] = (108.0, 92.5, 0, 1.8, 1.0, "top")
placements["R57"] = (108.0, 94.0, 0, 1.8, 1.0, "top")
placements["R58"] = (108.0, 95.5, 0, 1.8, 1.0, "top")
placements["R59"] = (108.0, 97.0, 0, 1.8, 1.0, "top")
placements["R60"] = (108.0, 98.5, 0, 1.8, 1.0, "top")

placements["TP1"] = (92.0, 89.0, 0, 1.5, 1.5, "top")

# 5. POWER INPUT & BUCK CONVERTER (East side)
# XT30PW-M (12.5 x 11.0 mm, rot=90) at x=124.0, y=96.0
placements["J11"] = (124.0, 96.0, 90, 11.0, 12.5, "top")
# Fuse Keystone 3568 (13.0 x 7.0 mm) at y=108.0
placements["F1"]  = (124.0, 108.0, 90, 7.0, 13.0, "top")
# TVS SMBJ30A (SMB: 5.4 x 3.9 mm) at y=117.0
placements["D6"]  = (124.0, 117.0, 90, 4.0, 5.5, "top")

# Buck converter:
# L1 (SRN6045TA: 6.5 x 6.5 mm)
placements["L1"]  = (115.0, 92.0, 0, 6.5, 6.5, "top")
# D4 (SMA: 5.2 x 2.8 mm)
placements["D4"]  = (115.0, 98.0, 0, 5.2, 2.8, "top")
# C16, C17 (0805: 1.6 x 2.4 mm, rot=90)
placements["C16"] = (117.5, 102.0, 90, 1.6, 2.4, "top")
placements["C17"] = (115.0, 102.0, 90, 1.6, 2.4, "top")
placements["R53"] = (111.0, 95.0, 90, 1.0, 1.8, "top")
placements["R54"] = (111.0, 97.5, 90, 1.0, 1.8, "top")

# 6. MICROCONTROLLER SUBSYSTEM (STM32F405 U1)
# U1 (LQFP-64: 12.2 x 12.2 mm) centered at x=100.0, y=109.0
placements["U1"] = (100.0, 109.0, 0, 12.2, 12.2, "top")

# Decoupling caps (0402: 1.2 x 0.8 mm, 0603: 1.8 x 1.0 mm)
# North pins:
placements["C4"]  = (98.0, 101.7, 0, 1.2, 0.8, "top")
placements["C5"]  = (102.0, 101.7, 0, 1.2, 0.8, "top")
# South pins:
placements["C10"] = (98.0, 116.3, 0, 1.2, 0.8, "top")
placements["C11"] = (102.0, 116.3, 0, 1.2, 0.8, "top")
# East pins:
placements["C6"]  = (107.3, 106.5, 90, 0.8, 1.2, "top")
placements["C7"]  = (107.3, 108.5, 90, 0.8, 1.2, "top")
placements["C50"] = (107.3, 110.5, 90, 0.8, 1.2, "top")
# West pins:
placements["C51"] = (92.7, 105.0, 90, 0.8, 1.2, "top")
placements["C52"] = (92.7, 107.0, 90, 0.8, 1.2, "top")
placements["C53"] = (92.7, 109.0, 90, 1.0, 1.8, "top")

# VDDA filter:
placements["FB1"] = (96.0, 101.7, 0, 1.8, 1.0, "top")
placements["C54"] = (94.0, 101.7, 0, 1.8, 1.0, "top")
placements["C55"] = (96.0, 103.0, 0, 1.8, 1.0, "top")
placements["C56"] = (94.0, 103.0, 0, 1.8, 1.0, "top")

# 12MHz Crystal & load caps:
placements["Y1"]  = (88.5, 105.0, 0, 3.5, 2.8, "top")
placements["C8"]  = (86.0, 104.0, 90, 0.8, 1.2, "top")
placements["C9"]  = (86.0, 106.0, 90, 0.8, 1.2, "top")
placements["R44"] = (88.5, 107.5, 0, 1.8, 1.0, "top")

# Boot & Reset:
placements["R32"] = (88.5, 109.5, 0, 1.2, 0.8, "top")
placements["R34"] = (88.5, 111.0, 0, 1.2, 0.8, "top")

# 3.3V LDO U10 (SOT-23-5: 3.1 x 3.0 mm)
placements["U10"] = (110.0, 105.0, 0, 3.1, 3.0, "top")
placements["C57"] = (112.5, 104.0, 90, 1.0, 1.8, "top")
placements["C58"] = (112.5, 106.0, 90, 1.0, 1.8, "top")

# Status LEDs & resistors:
placements["D1"]  = (80.0, 103.0, 0, 1.8, 1.0, "top")
placements["R33"] = (82.5, 103.0, 0, 1.2, 0.8, "top")
placements["D2"]  = (80.0, 105.0, 0, 1.8, 1.0, "top")
placements["R35"] = (82.5, 105.0, 0, 1.2, 0.8, "top")
placements["D3"]  = (80.0, 107.0, 0, 1.8, 1.0, "top")
placements["R36"] = (82.5, 107.0, 0, 1.2, 0.8, "top")

# Damping resistors (0603)
placements["R37"] = (80.0, 109.5, 0, 1.8, 1.0, "top")
placements["R38"] = (82.5, 109.5, 0, 1.8, 1.0, "top")
placements["R39"] = (80.0, 111.0, 0, 1.8, 1.0, "top")

# 7. WEST SIDE: SWD PROGRAMMING CONNECTOR (J10)
# S5B-XH-A: 14.9 x 12.51 mm, rot=90 facing West
placements["J10"] = (74.0, 102.0, 90, 12.51, 14.9, "top")

# 8. SOUTH CONNECTORS: J8 (CAN_IN), J9 (CAN_OUT), J7 (Type-C)
# J8 at x=93.0, y=123.0
# J9 at x=103.5, y=123.0
# J7 at x=113.5, y=127.0
placements["J8"] = (93.0, 123.0, 0, 9.9, 12.51, "top")
placements["J9"] = (103.5, 123.0, 0, 9.9, 12.51, "top")
placements["J7"] = (113.5, 127.0, 0, 8.94, 8.5, "top")

# 9. CAN BUS PASSIVES (in x in [74, 83], y in [116, 122])
placements["U9"]  = (76.0, 117.0, 0, 3.2, 3.2, "top") # TJA1051
placements["C60"] = (73.0, 116.0, 90, 1.0, 1.8, "top")
placements["C61"] = (73.0, 118.0, 90, 1.0, 1.8, "top")
placements["C62"] = (73.0, 120.0, 90, 1.0, 1.8, "top")
placements["R45"] = (76.0, 120.0, 90, 1.0, 1.8, "top")
placements["R46"] = (76.0, 122.0, 90, 1.0, 1.8, "top")
placements["JP1"] = (76.0, 114.0, 0, 2.0, 2.0, "top")

# 10. USB CIRCUIT PASSIVES (in x in [106, 114], y in [119, 124])
placements["U8"]  = (108.5, 119.5, 0, 3.1, 3.0, "top") # USBLC6-2SC6
placements["R40"] = (105.5, 119.5, 90, 1.0, 1.8, "top")
placements["R41"] = (111.5, 119.5, 90, 1.0, 1.8, "top")
placements["Q7"]  = (105.5, 121.5, 0, 3.0, 2.5, "top") # 2N7002
placements["R42"] = (105.5, 123.5, 0, 1.8, 1.0, "top")
placements["R43"] = (111.5, 121.5, 0, 1.8, 1.0, "top")
placements["C59"] = (111.5, 123.5, 0, 1.8, 1.0, "top")

# 11. ENCODER & PASSIVES (B.Cu - bottom layer)
placements["U2"]  = (100.0, 100.0, 0, 3.2, 3.2, "bottom") # MA730
placements["C14"] = (100.0, 103.0, 0, 1.8, 1.0, "bottom")
placements["R61"] = (100.0, 97.0, 0, 1.8, 1.0, "bottom")
placements["TP2"] = (96.5, 100.0, 0, 1.5, 1.5, "bottom")
placements["TP3"] = (103.5, 100.0, 0, 1.5, 1.5, "bottom")

# ==========================================================
# VERIFICATION SUITE
# ==========================================================
overlap_errors = []
keys = list(placements.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        k1, k2 = keys[i], keys[j]
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

boundary_errors = []
for k, c in placements.items():
    x, y, _, w, h, _ = c
    if k in ["C_BULK1", "C63"]:
        d = math.hypot(x - CX, y - CY) + 5.25
        if d > 35.0:
            boundary_errors.append(f"Boundary error {k}: cylinder radius {d:.2f} > 35.0")
        continue
    for px in [x - w/2, x + w/2]:
        for py in [y - h/2, y + h/2]:
            d = math.hypot(px - CX, py - CY)
            if d > 35.0:
                boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) radius {d:.2f} > 35.0")
                break

print(f"Boundary errors: {len(boundary_errors)}")
for err in boundary_errors:
    print(" ", err)
