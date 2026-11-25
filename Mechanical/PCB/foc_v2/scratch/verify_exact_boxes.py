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

def kicad_transform(x0, y0, rot_deg, lx, ly):
    rad = math.radians(rot_deg)
    return (
        x0 + lx * math.cos(rad) - ly * math.sin(rad),
        y0 + lx * math.sin(rad) + ly * math.cos(rad)
    )

def make_box(ref, x, y, rot, lx1, ly1, lx2, ly2, layer):
    c1 = kicad_transform(x, y, rot, lx1, ly1)
    c2 = kicad_transform(x, y, rot, lx2, ly1)
    c3 = kicad_transform(x, y, rot, lx1, ly2)
    c4 = kicad_transform(x, y, rot, lx2, ly2)
    xs = [c1[0], c2[0], c3[0], c4[0]]
    ys = [c1[1], c2[1], c3[1], c4[1]]
    return {
        'ref': ref,
        'x': x, 'y': y, 'rot': rot,
        'x1': min(xs), 'x2': max(xs),
        'y1': min(ys), 'y2': max(ys),
        'layer': layer
    }

def sym_box(ref, x, y, rot, w, h, layer):
    return make_box(ref, x, y, rot, -w/2, -h/2, w/2, h/2, layer)

boxes = {}

# 1. MOTOR PHASE TERMINALS (North, deep inside board: clearance > 4.5 mm)
boxes['J1'] = sym_box('J1', 89.0, 70.0, 0, 3.0, 3.0, 'top')
boxes['J2'] = sym_box('J2', 100.0, 69.5, 0, 3.0, 3.0, 'top')
boxes['J3'] = sym_box('J3', 111.0, 70.0, 0, 3.0, 3.0, 'top')

# 2. 6 MOSFETs in horizontal bank (Q1..Q6) at y=76.8
boxes['Q1'] = sym_box('Q1', 86.5, 76.8, 0, 5.3, 6.4, 'top')
boxes['Q2'] = sym_box('Q2', 92.0, 76.8, 180, 5.3, 6.4, 'top')
boxes['Q3'] = sym_box('Q3', 97.5, 76.8, 0, 5.3, 6.4, 'top')
boxes['Q4'] = sym_box('Q4', 103.0, 76.8, 180, 5.3, 6.4, 'top')
boxes['Q5'] = sym_box('Q5', 108.5, 76.8, 0, 5.3, 6.4, 'top')
boxes['Q6'] = sym_box('Q6', 114.0, 76.8, 180, 5.3, 6.4, 'top')

# DC Bus Caps (1210: 3.5 x 2.8) at y=71.8
boxes['C_BUS1'] = sym_box('C_BUS1', 83.5, 71.8, 0, 3.5, 2.8, 'top')
boxes['C_BUS2'] = sym_box('C_BUS2', 94.8, 71.8, 0, 3.5, 2.8, 'top')
boxes['C_BUS3'] = sym_box('C_BUS3', 105.5, 71.8, 0, 3.5, 2.8, 'top')

# 3. 3 Shunts (2512: 3.6 x 6.7, rot=90) at y=84.0
boxes['R47'] = sym_box('R47', 91.0, 84.0, 90, 3.6, 6.7, 'top')
boxes['R48'] = sym_box('R48', 99.5, 84.0, 90, 3.6, 6.7, 'top')
boxes['R49'] = sym_box('R49', 108.0, 84.0, 90, 3.6, 6.7, 'top')

# Kelvin NetTies (placed at sense pads)
boxes['NT1'] = sym_box('NT1', 91.0, 82.5, 90, 0.8, 0.8, 'top')
boxes['NT2'] = sym_box('NT2', 91.0, 85.5, 90, 0.8, 0.8, 'top')
boxes['NT3'] = sym_box('NT3', 99.5, 82.5, 90, 0.8, 0.8, 'top')
boxes['NT4'] = sym_box('NT4', 99.5, 85.5, 90, 0.8, 0.8, 'top')
boxes['NT5'] = sym_box('NT5', 108.0, 82.5, 90, 0.8, 0.8, 'top')
boxes['NT6'] = sym_box('NT6', 108.0, 85.5, 90, 0.8, 0.8, 'top')

# Gate resistors (0603: 1.8 x 1.0) at y=80.8
boxes['R1'] = sym_box('R1', 88.5, 80.8, 0, 1.8, 1.0, 'top')
boxes['R2'] = sym_box('R2', 91.5, 80.8, 0, 1.8, 1.0, 'top')
boxes['R3'] = sym_box('R3', 97.5, 80.8, 0, 1.8, 1.0, 'top')
boxes['R4'] = sym_box('R4', 100.5, 80.8, 0, 1.8, 1.0, 'top')
boxes['R5'] = sym_box('R5', 106.0, 80.8, 0, 1.8, 1.0, 'top')
boxes['R7'] = sym_box('R7', 111.0, 80.8, 0, 1.8, 1.0, 'top')

# Bulk caps (D10.0mm cylinder, radius 5.0mm, keepout 10.5 x 10.5)
boxes['C_BULK1'] = sym_box('C_BULK1', 75.0, 85.0, 0, 10.5, 10.5, 'top')
boxes['C63']     = sym_box('C63', 124.5, 83.5, 0, 10.5, 10.5, 'top')

# 4. DRV8323RS (IC1) at (100.0, 93.0)
boxes['IC1'] = sym_box('IC1', 100.0, 93.0, 0, 7.5, 7.5, 'top')

# Bootstrap caps (0603: 1.0 x 1.8)
boxes['C1'] = sym_box('C1', 94.5, 89.5, 90, 1.0, 1.8, 'top')
boxes['C2'] = sym_box('C2', 94.5, 91.5, 90, 1.0, 1.8, 'top')
boxes['C3'] = sym_box('C3', 94.5, 93.5, 90, 1.0, 1.8, 'top')

# DRV charge pump & bypass caps
boxes['C12'] = sym_box('C12', 94.5, 96.0, 90, 1.6, 2.4, 'top') # 0805
boxes['C13'] = sym_box('C13', 94.5, 98.2, 90, 1.0, 1.8, 'top') # 0603
boxes['C15'] = sym_box('C15', 105.5, 89.5, 90, 1.0, 1.8, 'top') # 0603
boxes['C18'] = sym_box('C18', 105.5, 91.5, 90, 1.0, 1.8, 'top') # 0603
boxes['C19'] = sym_box('C19', 105.5, 93.5, 90, 1.0, 1.8, 'top') # 0603
boxes['C20'] = sym_box('C20', 105.5, 95.5, 90, 1.0, 1.8, 'top') # 0603
boxes['C21'] = sym_box('C21', 105.5, 97.2, 90, 0.8, 1.2, 'top') # 0402
boxes['C64'] = sym_box('C64', 105.5, 99.0, 90, 1.0, 1.8, 'top') # 0603

# DRV config resistors (0603: 1.8 x 1.0)
boxes['R6']  = sym_box('R6',  92.0, 89.5, 0, 1.8, 1.0, 'top')
boxes['R8']  = sym_box('R8',  92.0, 91.0, 0, 1.8, 1.0, 'top')
boxes['R9']  = sym_box('R9',  92.0, 92.5, 0, 1.8, 1.0, 'top')
boxes['R10'] = sym_box('R10', 92.0, 94.0, 0, 1.8, 1.0, 'top')
boxes['R50'] = sym_box('R50', 92.0, 95.5, 0, 1.8, 1.0, 'top')
boxes['R51'] = sym_box('R51', 92.0, 97.0, 0, 1.8, 1.0, 'top')
boxes['R52'] = sym_box('R52', 92.0, 98.5, 0, 1.8, 1.0, 'top')

boxes['R55'] = sym_box('R55', 108.0, 89.5, 0, 1.8, 1.0, 'top')
boxes['R56'] = sym_box('R56', 108.0, 91.0, 0, 1.8, 1.0, 'top')
boxes['R57'] = sym_box('R57', 108.0, 92.5, 0, 1.8, 1.0, 'top')
boxes['R58'] = sym_box('R58', 108.0, 94.0, 0, 1.8, 1.0, 'top')
boxes['R59'] = sym_box('R59', 108.0, 95.5, 0, 1.8, 1.0, 'top')
boxes['R60'] = sym_box('R60', 108.0, 97.0, 0, 1.8, 1.0, 'top')

boxes['TP1'] = sym_box('TP1', 86.0, 89.0, 0, 1.5, 1.5, 'top')

# 5. CURRENT SENSE RC FILTERS (y=100.5)
boxes['R37'] = sym_box('R37', 94.5, 100.5, 0, 1.8, 1.0, 'top')
boxes['C54'] = sym_box('C54', 97.0, 100.5, 0, 1.8, 1.0, 'top')
boxes['R38'] = sym_box('R38', 99.5, 100.5, 0, 1.8, 1.0, 'top')
boxes['C55'] = sym_box('C55', 102.0, 100.5, 0, 1.8, 1.0, 'top')
boxes['R39'] = sym_box('R39', 104.5, 100.5, 0, 1.8, 1.0, 'top')
boxes['C56'] = sym_box('C56', 107.0, 100.5, 0, 1.8, 1.0, 'top')

# 6. BUCK CONVERTER (L1, D4, C16, C17, R53, R54)
boxes['L1']  = sym_box('L1', 113.0, 92.5, 0, 6.5, 6.5, 'top')
boxes['D4']  = sym_box('D4', 113.0, 97.5, 0, 5.2, 2.8, 'top')
boxes['C16'] = sym_box('C16', 113.0, 100.0, 90, 1.6, 2.4, 'top')
boxes['C17'] = sym_box('C17', 113.0, 102.5, 90, 1.6, 2.4, 'top')
boxes['R53'] = sym_box('R53', 117.0, 98.0, 0, 1.8, 1.0, 'top')
boxes['R54'] = sym_box('R54', 117.0, 100.0, 0, 1.8, 1.0, 'top')

# 7. POWER INPUT COLUMN (East edge: J11, F1, D6)
# XT30PW-M: rot=90 facing East at y=99.5
boxes['J11'] = make_box('J11', 121.0, 99.5, 90, -9.65, -13.6, 4.65, 2.25, 'top')

# Fuse F1 at y=111.0
boxes['F1'] = sym_box('F1', 125.5, 111.0, 90, 7.0, 13.0, 'top')

# TVS D6 at y=119.5
boxes['D6'] = sym_box('D6', 124.0, 119.5, 90, 4.0, 5.5, 'top')

# 8. SWD PROGRAMMING HEADER (West edge: J10)
boxes['J10'] = make_box('J10', 76.5, 95.0, 90, -2.95, -2.81, 12.95, 9.70, 'top')

# 9. MICROCONTROLLER SUBSYSTEM (STM32F405 U1)
boxes['U1'] = sym_box('U1', 100.0, 109.5, 0, 12.2, 12.2, 'top')

# Decoupling caps
boxes['C4']  = sym_box('C4',  97.0, 102.5, 0, 1.2, 0.8, 'top')
boxes['C5']  = sym_box('C5',  103.0, 102.5, 0, 1.2, 0.8, 'top')
boxes['C10'] = sym_box('C10', 97.0, 116.5, 0, 1.2, 0.8, 'top')
boxes['C11'] = sym_box('C11', 103.0, 116.5, 0, 1.2, 0.8, 'top')
boxes['C6']  = sym_box('C6',  107.5, 107.5, 90, 0.8, 1.2, 'top')
boxes['C7']  = sym_box('C7',  107.5, 109.5, 90, 0.8, 1.2, 'top')
boxes['C50'] = sym_box('C50', 107.5, 111.5, 90, 0.8, 1.2, 'top')
boxes['C51'] = sym_box('C51', 92.5, 107.0, 90, 0.8, 1.2, 'top')
boxes['C52'] = sym_box('C52', 92.5, 109.0, 90, 0.8, 1.2, 'top')
boxes['C53'] = sym_box('C53', 92.5, 111.0, 90, 1.0, 1.8, 'top')

# VDDA filter
boxes['FB1'] = sym_box('FB1', 89.5, 103.0, 0, 1.8, 1.0, 'top')

# Crystal Y1 & load caps
boxes['Y1']  = sym_box('Y1',  87.0, 106.0, 0, 3.5, 2.8, 'top')
boxes['C8']  = sym_box('C8',  84.5, 105.0, 90, 0.8, 1.2, 'top')
boxes['C9']  = sym_box('C9',  84.5, 107.0, 90, 0.8, 1.2, 'top')
boxes['R44'] = sym_box('R44', 87.0, 108.5, 0, 1.8, 1.0, 'top')

# Boot & Reset
boxes['R32'] = sym_box('R32', 87.0, 110.5, 0, 1.2, 0.8, 'top')
boxes['R34'] = sym_box('R34', 87.0, 112.0, 0, 1.2, 0.8, 'top')

# 3.3V LDO U10
boxes['U10'] = sym_box('U10', 109.5, 105.5, 0, 3.1, 3.0, 'top')
boxes['C57'] = sym_box('C57', 112.5, 104.5, 90, 1.0, 1.8, 'top')
boxes['C58'] = sym_box('C58', 112.5, 106.5, 90, 1.0, 1.8, 'top')

# Status LEDs
boxes['D1']  = sym_box('D1',  107.5, 116.5, 0, 1.8, 1.0, 'top')
boxes['R33'] = sym_box('R33', 109.5, 116.5, 0, 1.2, 0.8, 'top')
boxes['D2']  = sym_box('D2',  107.5, 118.0, 0, 1.8, 1.0, 'top')
boxes['R35'] = sym_box('R35', 109.5, 118.0, 0, 1.2, 0.8, 'top')
boxes['D3']  = sym_box('D3',  107.5, 119.5, 0, 1.8, 1.0, 'top')
boxes['R36'] = sym_box('R36', 109.5, 119.5, 0, 1.2, 0.8, 'top')

# 10. SOUTH CONNECTORS: J8 (CAN_IN), J9 (CAN_OUT), J7 (Type-C)
boxes['J8'] = make_box('J8', 86.0, 122.5, 0, -2.95, -2.81, 7.95, 9.70, 'top')
boxes['J9'] = make_box('J9', 97.5, 122.5, 0, -2.95, -2.81, 7.95, 9.70, 'top')
boxes['J7'] = make_box('J7', 112.0, 128.05, 0, -5.32, -5.27, 5.32, 4.15, 'top')

# 11. CAN BUS PASSIVES (West side)
boxes['U9']  = sym_box('U9',  76.0, 117.5, 0, 3.2, 3.2, 'top') # TJA1051
boxes['C60'] = sym_box('C60', 73.5, 116.0, 90, 1.0, 1.8, 'top')
boxes['C61'] = sym_box('C61', 73.5, 118.0, 90, 1.0, 1.8, 'top')
boxes['C62'] = sym_box('C62', 73.5, 120.0, 90, 1.0, 1.8, 'top')
boxes['R45'] = sym_box('R45', 76.0, 120.5, 90, 1.0, 1.8, 'top')
boxes['R46'] = sym_box('R46', 76.0, 122.5, 90, 1.0, 1.8, 'top')
boxes['JP1'] = sym_box('JP1', 76.0, 113.5, 0, 2.0, 2.0, 'top')

# 12. USB CIRCUIT PASSIVES (Neat array in safe South-East zone)
boxes['Q7']  = sym_box('Q7',  119.0, 120.0, 0, 2.5, 3.0, 'top') # 2N7002
boxes['U8']  = sym_box('U8',  119.5, 123.5, 0, 3.0, 3.1, 'top') # USBLC6-2SC6
boxes['R40'] = sym_box('R40', 118.5, 126.0, 0, 1.8, 1.0, 'top')
boxes['R41'] = sym_box('R41', 121.0, 126.0, 0, 1.8, 1.0, 'top')
boxes['R42'] = sym_box('R42', 118.5, 127.5, 0, 1.8, 1.0, 'top')
boxes['R43'] = sym_box('R43', 121.0, 127.5, 0, 1.8, 1.0, 'top')
boxes['C59'] = sym_box('C59', 119.5, 129.0, 0, 1.8, 1.0, 'top')

# 13. ENCODER & PASSIVES (B.Cu)
boxes['U2']  = sym_box('U2',  100.0, 100.0, 0, 3.2, 3.2, 'bottom')
boxes['C14'] = sym_box('C14', 100.0, 103.0, 0, 1.8, 1.0, 'bottom')
boxes['R61'] = sym_box('R61', 100.0, 97.0, 0, 1.8, 1.0, 'bottom')
boxes['TP2'] = sym_box('TP2', 96.5, 100.0, 0, 1.5, 1.5, 'bottom')
boxes['TP3'] = sym_box('TP3', 103.5, 100.0, 0, 1.5, 1.5, 'bottom')

print(f"Total boxed components: {len(boxes)} / 120 (plus 4 mounting holes = 124)")

# NetTie allowed overlaps
ALLOWED_OVERLAPS = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

overlap_errors = []
bkeys = list(boxes.keys())
for i in range(len(bkeys)):
    for j in range(i + 1, len(bkeys)):
        k1, k2 = bkeys[i], bkeys[j]
        if (k1, k2) in ALLOWED_OVERLAPS or (k2, k1) in ALLOWED_OVERLAPS:
            continue
        b1, b2 = boxes[k1], boxes[k2]
        if b1['layer'] != b2['layer']:
            continue
        
        # AABB overlap test
        if not (b1['x2'] <= b2['x1'] or b1['x1'] >= b2['x2'] or b1['y2'] <= b2['y1'] or b1['y1'] >= b2['y2']):
            dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
            dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
            overlap_errors.append(f"Overlap {k1} and {k2}: intersect {dx:.2f} x {dy:.2f} mm")

print(f"Component-to-component overlaps: {len(overlap_errors)}")
for err in overlap_errors:
    print(" ", err)

hole_collisions = []
for hname, (hx, hy) in HOLES.items():
    for k, b in boxes.items():
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx - hx, cy - hy)
        if d < R_SCREW_KEEPOUT:
            hole_collisions.append(f"Collision {hname} and {k}: dist {d:.2f} < {R_SCREW_KEEPOUT:.2f} mm")

print(f"Hole collisions: {len(hole_collisions)}")
for err in hole_collisions:
    print(" ", err)

boundary_errors = []
for k, b in boxes.items():
    if k in ['C_BULK1', 'C63']:
        d = math.hypot(b['x'] - CX, b['y'] - CY) + 5.1
        if d > 35.0:
            boundary_errors.append(f"Boundary error {k}: cylinder radius {d:.2f} > 35.0")
        continue
    for px, py in [(b['x1'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y1']), (b['x2'], b['y2'])]:
        if py > 132.5:
            boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) y > 132.5")
        elif px < 66.5:
            boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) x < 66.5")
        elif px > 135.0:
            boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) x > 135.0")
        else:
            d = math.hypot(px - CX, py - CY)
            if d > 35.5:
                in_south = (py >= 120.0 and 83.0 <= px <= 122.5 and py <= 132.5)
                in_west  = (px <= 78.0 and 91.0 <= py <= 108.5 and px >= 66.5)
                in_east  = (px >= 120.0 and 87.0 <= py <= 116.0 and px <= 135.0)
                if not (in_south or in_west or in_east):
                    boundary_errors.append(f"Boundary error {k}: point ({px:.2f}, {py:.2f}) radius {d:.2f} > 35.5 outside flat cuts")

print(f"Boundary errors: {len(boundary_errors)}")
for err in boundary_errors:
    print(" ", err)
