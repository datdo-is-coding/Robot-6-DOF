import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

P = {}

# 1. MOUNTING HOLES (PCD Ø44 mm)
delta_h = 22.0 / math.sqrt(2)
P['H3'] = (100.0 - delta_h, 100.0 - delta_h, 0, 'F.Cu') # NW (84.444, 84.444)
P['H4'] = (100.0 + delta_h, 100.0 - delta_h, 0, 'F.Cu') # NE (115.556, 84.444)
P['H2'] = (100.0 - delta_h, 100.0 + delta_h, 0, 'F.Cu') # SW (84.444, 115.556)
P['H1'] = (100.0 + delta_h, 100.0 + delta_h, 0, 'F.Cu') # SE (115.556, 115.556)

# 2. MOTOR PHASE TERMINALS (North: deep inside board, uncut circles)
P['J1'] = (88.0, 69.5, 0, 'F.Cu')
P['J2'] = (100.0, 69.0, 0, 'F.Cu')
P['J3'] = (112.0, 69.5, 0, 'F.Cu')

# 3. 6 MOSFETS (y = 75.8, rot=90 for high-side, rot=270 for low-side)
P['Q1'] = (83.5, 75.8, 90, 'F.Cu')
P['Q2'] = (90.1, 75.8, 270, 'F.Cu')
P['Q3'] = (96.7, 75.8, 90, 'F.Cu')
P['Q4'] = (103.3, 75.8, 270, 'F.Cu')
P['Q5'] = (109.9, 75.8, 90, 'F.Cu')
P['Q6'] = (116.5, 75.8, 270, 'F.Cu')

# DC Bus Ceramic Caps (1210: 3.5 x 2.8 at rot=0) - placed between motor pads
P['C_BUS1'] = (82.5, 70.0, 0, 'F.Cu')
P['C_BUS2'] = (94.0, 69.5, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 69.5, 0, 'F.Cu')

# Gate Resistors (0603: 2.96 x 1.46 at rot=0) at y = 80.6
P['R1'] = (83.5, 80.6, 0, 'F.Cu')
P['R2'] = (89.5, 80.6, 0, 'F.Cu')
P['R3'] = (96.0, 80.6, 0, 'F.Cu')
P['R4'] = (102.5, 80.6, 0, 'F.Cu')
P['R5'] = (109.5, 80.6, 0, 'F.Cu')
P['R7'] = (116.5, 80.6, 0, 'F.Cu')

# 3 Shunts (2512: 3.86 x 7.66 at rot=90) at y = 85.3
P['R47'] = (93.0, 85.3, 90, 'F.Cu')
P['R48'] = (100.0, 85.3, 90, 'F.Cu')
P['R49'] = (107.0, 85.3, 90, 'F.Cu')

# Kelvin NetTies (allowed overlap with their respective shunt pads)
P['NT1'] = (93.0, 83.5, 90, 'F.Cu')
P['NT2'] = (93.0, 87.1, 90, 'F.Cu')
P['NT3'] = (100.0, 83.5, 90, 'F.Cu')
P['NT4'] = (100.0, 87.1, 90, 'F.Cu')
P['NT5'] = (107.0, 83.5, 90, 'F.Cu')
P['NT6'] = (107.0, 87.1, 90, 'F.Cu')

# Bulk Capacitors (D10.0mm cylinder: center at (x + 2.5, y), r = 5.25)
P['C_BULK1'] = (70.5, 83.0, 0, 'F.Cu') # cylinder center = (73.0, 83.0)
P['C63']     = (124.5, 83.0, 0, 'F.Cu') # cylinder center = (127.0, 83.0)

# 4. GATE DRIVER IC1 (DRV8323RS) at (100.0, 93.5)
P['IC1'] = (100.0, 93.5, 0, 'F.Cu')

# Bootstrap Caps (0603 at rot=0: width 2.96, height 1.46)
P['C1'] = (94.0, 90.0, 0, 'F.Cu')
P['C2'] = (94.0, 92.0, 0, 'F.Cu')
P['C3'] = (94.0, 94.0, 0, 'F.Cu')

# DRV charge pump & bypass caps
P['C12'] = (94.0, 96.5, 0, 'F.Cu') # 0805
P['C13'] = (94.0, 99.0, 0, 'F.Cu') # 0603

P['C15'] = (106.0, 90.0, 0, 'F.Cu') # 0603
P['C18'] = (106.0, 92.0, 0, 'F.Cu') # 0603
P['C19'] = (106.0, 94.0, 0, 'F.Cu') # 0603
P['C20'] = (106.0, 96.0, 0, 'F.Cu') # 0603
P['C21'] = (106.0, 97.7, 0, 'F.Cu') # 0402
P['C64'] = (106.0, 99.5, 0, 'F.Cu') # 0603

# DRV config resistors (0603 at rot=0)
P['R6']  = (90.5, 90.0, 0, 'F.Cu')
P['R8']  = (90.5, 91.8, 0, 'F.Cu')
P['R9']  = (90.5, 93.6, 0, 'F.Cu')
P['R10'] = (90.5, 95.4, 0, 'F.Cu')
P['R50'] = (90.5, 97.2, 0, 'F.Cu')
P['R51'] = (88.0, 94.5, 0, 'F.Cu')
P['R52'] = (88.0, 96.5, 0, 'F.Cu')

P['R55'] = (109.5, 90.0, 0, 'F.Cu')
P['R56'] = (109.5, 91.8, 0, 'F.Cu')
P['R57'] = (109.5, 93.6, 0, 'F.Cu')
P['R58'] = (109.5, 95.4, 0, 'F.Cu')
P['R59'] = (109.5, 97.2, 0, 'F.Cu')
P['R60'] = (109.5, 99.0, 0, 'F.Cu')

# Test Point TP1
P['TP1'] = (86.0, 90.0, 0, 'F.Cu')

# Current Sense RC Filters (0603 at y = 101.5)
P['R37'] = (91.5, 101.5, 0, 'F.Cu')
P['C54'] = (94.0, 101.5, 0, 'F.Cu')
P['R38'] = (97.5, 101.5, 0, 'F.Cu')
P['C55'] = (100.5, 101.5, 0, 'F.Cu')
P['R39'] = (103.5, 101.5, 0, 'F.Cu')
P['C56'] = (106.5, 101.5, 0, 'F.Cu')

# Test points TP2, TP3
P['TP2'] = (89.0, 101.5, 0, 'F.Cu')
P['TP3'] = (112.5, 101.5, 0, 'F.Cu')

# 5. POWER INPUT COLUMN (East edge: J11, F1, D6)
# XT30 J11: at x = 122.0, y = 104.5, rot = 270 (faces East)
P['J11'] = (122.0, 104.5, 270, 'F.Cu')
P['F1']  = (126.0, 114.5, 90, 'F.Cu')
P['D6']  = (125.0, 122.0, 90, 'F.Cu')

# Buck Converter (L1, D4, C16, C17, R53, R54)
P['L1']  = (117.0, 91.5, 0, 'F.Cu')
P['D4']  = (114.0, 96.0, 0, 'F.Cu')
P['C16'] = (114.0, 99.0, 90, 'F.Cu')
P['C17'] = (114.0, 101.8, 90, 'F.Cu')
P['R53'] = (118.0, 96.0, 0, 'F.Cu')
P['R54'] = (118.0, 98.0, 0, 'F.Cu')

# 6. MCU SUBSYSTEM (STM32F405 U1)
P['U1']  = (100.0, 111.5, 0, 'F.Cu')

# Decoupling caps
P['C4']  = (96.5, 104.0, 0, 'F.Cu')
P['C5']  = (103.5, 104.0, 0, 'F.Cu')
P['C10'] = (96.5, 119.5, 0, 'F.Cu')
P['C11'] = (103.5, 119.5, 0, 'F.Cu')

P['C51'] = (91.5, 108.0, 90, 'F.Cu')
P['C52'] = (91.5, 111.0, 90, 'F.Cu')
P['C53'] = (91.5, 114.0, 90, 'F.Cu')

P['C6']  = (108.5, 108.0, 90, 'F.Cu')
P['C7']  = (108.5, 111.0, 90, 'F.Cu')
P['C50'] = (108.5, 114.0, 90, 'F.Cu')

# 3.3V LDO U10
P['U10'] = (112.5, 106.0, 0, 'F.Cu')
P['C57'] = (116.5, 104.5, 90, 'F.Cu')
P['C58'] = (116.5, 107.5, 90, 'F.Cu')

# Crystal Y1 & passives
P['FB1'] = (88.5, 104.0, 0, 'F.Cu')
P['Y1']  = (86.0, 107.5, 0, 'F.Cu')
P['C8']  = (82.5, 106.0, 90, 'F.Cu')
P['C9']  = (82.5, 109.0, 90, 'F.Cu')
P['R44'] = (86.0, 110.5, 0, 'F.Cu')
P['R32'] = (88.5, 110.5, 0, 'F.Cu')
P['R34'] = (88.5, 112.5, 0, 'F.Cu')

# Status LEDs
P['D1']  = (107.5, 117.5, 0, 'F.Cu')
P['R33'] = (111.0, 117.5, 0, 'F.Cu')
P['D2']  = (107.5, 119.5, 0, 'F.Cu')
P['R35'] = (111.0, 119.5, 0, 'F.Cu')
P['D3']  = (107.5, 121.5, 0, 'F.Cu')
P['R36'] = (111.0, 121.5, 0, 'F.Cu')

# 7. SOUTH CONNECTORS BANK: J8, J9, J7, J10
P['J8']  = (74.5, 122.5, 0, 'F.Cu')  # CAN_IN
P['J9']  = (86.0, 122.5, 0, 'F.Cu')  # CAN_OUT
P['J7']  = (100.0, 128.0, 0, 'F.Cu') # Type-C
P['J10'] = (109.5, 122.5, 0, 'F.Cu') # SWD

# CAN Bus Passives (West area near J8)
P['U9']  = (72.0, 117.5, 0, 'F.Cu')
P['C60'] = (68.5, 115.5, 90, 'F.Cu')
P['C61'] = (68.5, 118.5, 90, 'F.Cu')
P['C62'] = (68.5, 121.5, 90, 'F.Cu')
P['R45'] = (72.0, 121.5, 0, 'F.Cu')
P['R46'] = (72.0, 123.5, 0, 'F.Cu')
P['JP1'] = (72.0, 113.5, 0, 'F.Cu')

# USB Circuit Passives on B.Cu
P['U8']  = (100.0, 121.5, 0, 'B.Cu')
P['Q7']  = (105.0, 121.5, 0, 'B.Cu')
P['R40'] = (97.0, 124.0, 0, 'B.Cu')
P['R41'] = (97.0, 126.0, 0, 'B.Cu')
P['R42'] = (103.0, 124.0, 0, 'B.Cu')
P['R43'] = (103.0, 126.0, 0, 'B.Cu')
P['C59'] = (100.0, 127.5, 0, 'B.Cu')

# 8. BOTTOM LAYER ENCODER
P['U2']  = (100.0, 100.0, 0, 'B.Cu')
P['C14'] = (100.0, 103.0, 0, 'B.Cu')
P['R61'] = (100.0, 97.0, 0, 'B.Cu')

ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

HOLES = {
    "H3": (84.444, 84.444),
    "H4": (115.556, 84.444),
    "H2": (84.444, 115.556),
    "H1": (115.556, 115.556)
}
R_KO = 3.0

bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    box = get_world_bbox(ref, is_b, shapes, x, y, rot)
    bboxes[ref] = box

overlaps = []
refs = list(bboxes.keys())
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        r1, r2 = refs[i], refs[j]
        if (r1, r2) in ALLOWED or (r2, r1) in ALLOWED:
            continue
        b1, b2 = bboxes[r1], bboxes[r2]
        if b1['layer'] != b2['layer']:
            continue
        if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
            dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
            dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
            overlaps.append((r1, r2, dx, dy, b1, b2))

hole_errs = []
for hname, (hx, hy) in HOLES.items():
    for r, b in bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx - hx, cy - hy)
        if d < R_KO:
            hole_errs.append((hname, r, d))

print(f"==========================================")
print(f"TOTAL COMPONENTS: {len(P)} / 124")
print(f"OVERLAPS DETECTED: {len(overlaps)}")
print(f"HOLE COLLISIONS: {len(hole_errs)}")
print(f"==========================================")
for r1, r2, dx, dy, b1, b2 in overlaps:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, d in hole_errs:
    print(f"  HOLE: {h} <--> {r} : dist={d:.2f}")
