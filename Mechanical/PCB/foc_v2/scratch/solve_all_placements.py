import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
print(f"Loaded {len(fps)} footprints from foc_v2.kicad_pcb")

# Define updated placements
# (x, y, rot, layer)
P = {}

# 1. MOUNTING HOLES (PCD Ø44 mm: R = 22.0 mm at 45 deg)
delta_h = 22.0 / math.sqrt(2) # 15.55635 mm
P['H3'] = (100.0 - delta_h, 100.0 - delta_h, 0, 'F.Cu') # NW (84.444, 84.444)
P['H4'] = (100.0 + delta_h, 100.0 - delta_h, 0, 'F.Cu') # NE (115.556, 84.444)
P['H2'] = (100.0 - delta_h, 100.0 + delta_h, 0, 'F.Cu') # SW (84.444, 115.556)
P['H1'] = (100.0 + delta_h, 100.0 + delta_h, 0, 'F.Cu') # SE (115.556, 115.556)

# 2. MOTOR PHASE TERMINALS (North: deep inside board, uncut circles)
P['J1'] = (88.0, 70.0, 0, 'F.Cu')
P['J2'] = (100.0, 69.5, 0, 'F.Cu')
P['J3'] = (112.0, 70.0, 0, 'F.Cu')

# 3. 6 MOSFETS (y = 75.8, rot=90 for high-side, rot=270 for low-side)
# Width in X is 5.66 mm. Pitch = 6.6 mm.
P['Q1'] = (83.5, 75.8, 90, 'F.Cu')
P['Q2'] = (90.1, 75.8, 270, 'F.Cu')
P['Q3'] = (96.7, 75.8, 90, 'F.Cu')
P['Q4'] = (103.3, 75.8, 270, 'F.Cu')
P['Q5'] = (109.9, 75.8, 90, 'F.Cu')
P['Q6'] = (116.5, 75.8, 270, 'F.Cu')

# DC Bus Ceramic Caps (1210: 3.5 x 2.8 at rot=0)
P['C_BUS1'] = (86.8, 71.5, 0, 'F.Cu')
P['C_BUS2'] = (100.0, 71.5, 0, 'F.Cu')
P['C_BUS3'] = (113.2, 71.5, 0, 'F.Cu')

# Gate Resistors (0603: 2.96 x 1.46 at rot=0) at y = 80.2
P['R1'] = (84.0, 80.2, 0, 'F.Cu')
P['R2'] = (89.5, 80.2, 0, 'F.Cu')
P['R3'] = (96.0, 80.2, 0, 'F.Cu')
P['R4'] = (102.5, 80.2, 0, 'F.Cu')
P['R5'] = (109.5, 80.2, 0, 'F.Cu')
P['R7'] = (115.5, 80.2, 0, 'F.Cu')

# 3 Shunts (2512: 3.86 x 7.66 at rot=90) at y = 85.3
P['R47'] = (90.1, 85.3, 90, 'F.Cu')
P['R48'] = (103.3, 85.3, 90, 'F.Cu')
P['R49'] = (116.5, 85.3, 90, 'F.Cu')

# Kelvin NetTies (allowed overlap with their respective shunt pads)
P['NT1'] = (90.1, 83.5, 90, 'F.Cu')
P['NT2'] = (90.1, 87.1, 90, 'F.Cu')
P['NT3'] = (103.3, 83.5, 90, 'F.Cu')
P['NT4'] = (103.3, 87.1, 90, 'F.Cu')
P['NT5'] = (116.5, 83.5, 90, 'F.Cu')
P['NT6'] = (116.5, 87.1, 90, 'F.Cu')

# Bulk Capacitors (D10.0mm cylinder: center at (x + 2.5, y), r = 5.25)
P['C_BULK1'] = (70.5, 83.0, 0, 'F.Cu') # cylinder center = (73.0, 83.0), dist to H3 = 11.5 mm > 8.2 mm!
P['C63']     = (124.5, 83.0, 0, 'F.Cu') # cylinder center = (127.0, 83.0), dist to H4 = 11.5 mm > 8.2 mm!

# 4. GATE DRIVER IC1 (DRV8323RS) at (100.0, 93.5)
P['IC1'] = (100.0, 93.5, 0, 'F.Cu')

# Bootstrap Caps (0603 at rot=0: width 2.96, height 1.46)
P['C1'] = (94.5, 89.8, 0, 'F.Cu')
P['C2'] = (94.5, 91.8, 0, 'F.Cu')
P['C3'] = (94.5, 93.8, 0, 'F.Cu')

# DRV charge pump & bypass caps
P['C12'] = (94.5, 96.0, 0, 'F.Cu') # 0805
P['C13'] = (94.5, 98.2, 0, 'F.Cu') # 0603

P['C15'] = (105.5, 89.5, 0, 'F.Cu') # 0603
P['C18'] = (105.5, 91.5, 0, 'F.Cu') # 0603
P['C19'] = (105.5, 93.5, 0, 'F.Cu') # 0603
P['C20'] = (105.5, 95.5, 0, 'F.Cu') # 0603
P['C21'] = (105.5, 97.2, 0, 'F.Cu') # 0402
P['C64'] = (105.5, 99.2, 0, 'F.Cu') # 0603

# DRV config resistors (0603 at rot=0)
P['R6']  = (91.5, 89.5, 0, 'F.Cu')
P['R8']  = (91.5, 91.3, 0, 'F.Cu')
P['R9']  = (91.5, 93.1, 0, 'F.Cu')
P['R10'] = (91.5, 94.9, 0, 'F.Cu')
P['R50'] = (91.5, 96.7, 0, 'F.Cu')
P['R51'] = (91.5, 98.5, 0, 'F.Cu')
P['R52'] = (91.5, 100.3, 0, 'F.Cu')

P['R55'] = (108.5, 89.5, 0, 'F.Cu')
P['R56'] = (108.5, 91.3, 0, 'F.Cu')
P['R57'] = (108.5, 93.1, 0, 'F.Cu')
P['R58'] = (108.5, 94.9, 0, 'F.Cu')
P['R59'] = (108.5, 96.7, 0, 'F.Cu')
P['R60'] = (108.5, 98.5, 0, 'F.Cu')

# Test Point TP1
P['TP1'] = (86.0, 92.0, 0, 'F.Cu')

# Current Sense RC Filters (0603 at y = 102.5)
P['R37'] = (93.5, 102.5, 0, 'F.Cu')
P['C54'] = (96.5, 102.5, 0, 'F.Cu')
P['R38'] = (99.5, 102.5, 0, 'F.Cu')
P['C55'] = (102.0, 102.5, 0, 'F.Cu')
P['R39'] = (104.5, 102.5, 0, 'F.Cu')
P['C56'] = (107.5, 102.5, 0, 'F.Cu')

# Test points TP2, TP3 (placed safely near sense traces)
P['TP2'] = (91.0, 102.5, 0, 'F.Cu')
P['TP3'] = (110.0, 102.5, 0, 'F.Cu')

# 5. POWER INPUT COLUMN (East edge: J11, F1, D6)
P['J11'] = (122.0, 99.5, 90, 'F.Cu') # rot=90 points East in KiCad
P['F1']  = (125.0, 111.0, 90, 'F.Cu')
P['D6']  = (124.0, 118.5, 90, 'F.Cu')

# Buck Converter (L1, D4, C16, C17, R53, R54)
P['L1']  = (114.5, 91.0, 0, 'F.Cu')
P['D4']  = (114.5, 96.0, 0, 'F.Cu')
P['C16'] = (114.5, 99.0, 90, 'F.Cu')
P['C17'] = (114.5, 101.8, 90, 'F.Cu')
P['R53'] = (118.0, 94.5, 0, 'F.Cu')
P['R54'] = (118.0, 96.5, 0, 'F.Cu')

# 6. MCU SUBSYSTEM (STM32F405 U1)
P['U1']  = (100.0, 111.0, 0, 'F.Cu')

# Decoupling caps
P['C4']  = (97.0, 103.0, 0, 'F.Cu')
P['C5']  = (103.0, 103.0, 0, 'F.Cu')
P['C10'] = (97.0, 119.0, 0, 'F.Cu')
P['C11'] = (103.0, 119.0, 0, 'F.Cu')

P['C51'] = (91.5, 107.0, 90, 'F.Cu')
P['C52'] = (91.5, 110.0, 90, 'F.Cu')
P['C53'] = (91.5, 113.0, 90, 'F.Cu')

P['C6']  = (108.5, 107.0, 90, 'F.Cu')
P['C7']  = (108.5, 110.0, 90, 'F.Cu')
P['C50'] = (108.5, 113.0, 90, 'F.Cu')

# 3.3V LDO U10
P['U10'] = (112.5, 106.0, 0, 'F.Cu')
P['C57'] = (116.0, 104.5, 90, 'F.Cu')
P['C58'] = (116.0, 107.5, 90, 'F.Cu')

# Crystal Y1 & passives
P['FB1'] = (88.5, 103.0, 0, 'F.Cu')
P['Y1']  = (86.0, 106.5, 0, 'F.Cu')
P['C8']  = (82.5, 105.0, 90, 'F.Cu')
P['C9']  = (82.5, 108.0, 90, 'F.Cu')
P['R44'] = (86.0, 109.5, 0, 'F.Cu')
P['R32'] = (86.0, 111.5, 0, 'F.Cu')
P['R34'] = (86.0, 113.5, 0, 'F.Cu')

# Status LEDs
P['D1']  = (108.0, 116.5, 0, 'F.Cu')
P['R33'] = (111.5, 116.5, 0, 'F.Cu')
P['D2']  = (108.0, 118.5, 0, 'F.Cu')
P['R35'] = (111.5, 118.5, 0, 'F.Cu')
P['D3']  = (108.0, 120.5, 0, 'F.Cu')
P['R36'] = (111.5, 120.5, 0, 'F.Cu')

# 7. SOUTH CONNECTORS BANK: J8, J9, J7, J10
# All facing South (rot=0), flush at y = 132.2 inside flat cut y = 132.5
P['J8']  = (78.5, 122.5, 0, 'F.Cu')  # CAN_IN (3-pin XH)
P['J9']  = (89.5, 122.5, 0, 'F.Cu')  # CAN_OUT (3-pin XH)
P['J7']  = (102.0, 128.0, 0, 'F.Cu') # USB Type-C
P['J10'] = (113.5, 122.5, 0, 'F.Cu') # SWD (5-pin XH)

# CAN Bus Passives (West area near J8)
P['U9']  = (72.0, 117.5, 0, 'F.Cu')
P['C60'] = (68.5, 116.0, 90, 'F.Cu')
P['C61'] = (68.5, 118.5, 90, 'F.Cu')
P['C62'] = (68.5, 121.0, 90, 'F.Cu')
P['R45'] = (72.0, 121.0, 0, 'F.Cu')
P['R46'] = (72.0, 123.0, 0, 'F.Cu')
P['JP1'] = (72.0, 113.5, 0, 'F.Cu')

# USB Circuit Passives (Near J7)
P['U8']  = (102.0, 121.5, 0, 'F.Cu')
P['Q7']  = (106.0, 121.5, 0, 'F.Cu')
P['R40'] = (98.0, 123.5, 0, 'F.Cu')
P['R41'] = (100.5, 123.5, 0, 'F.Cu')
P['R42'] = (103.5, 123.5, 0, 'F.Cu')
P['R43'] = (106.0, 123.5, 0, 'F.Cu')
P['C59'] = (102.0, 125.2, 0, 'F.Cu')

# 8. BOTTOM LAYER (B.Cu)
P['U2']  = (100.0, 100.0, 0, 'B.Cu')
P['C14'] = (100.0, 103.0, 0, 'B.Cu')
P['R61'] = (100.0, 97.0, 0, 'B.Cu')

print(f"Total defined placements: {len(P)} / 124")

# Compute bounding boxes
bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    box = get_world_bbox(ref, is_b, shapes, x, y, rot)
    bboxes[ref] = box

ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

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

print(f"\n==========================================")
print(f"OVERLAPS DETECTED: {len(overlaps)}")
print(f"==========================================")
for r1, r2, dx, dy, b1, b2 in overlaps:
    print(f"  {r1:8s} ({b1['cx']:.1f}, {b1['cy']:.1f}) <--> {r2:8s} ({b2['cx']:.1f}, {b2['cy']:.1f}) : dx={dx:.2f}, dy={dy:.2f}")

# Check Hole Keepout Collisions
HOLES = {
    "H3": (84.444, 84.444),
    "H4": (115.556, 84.444),
    "H2": (84.444, 115.556),
    "H1": (115.556, 115.556)
}
R_KO = 3.0
hole_errs = []
for hname, (hx, hy) in HOLES.items():
    for r, b in bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx - hx, cy - hy)
        if d < R_KO:
            hole_errs.append((hname, r, d))

print(f"\nHOLE COLLISIONS: {len(hole_errs)}")
for hname, r, d in hole_errs:
    print(f"  {hname} <--> {r:8s} : dist={d:.2f} < {R_KO:.2f} mm")
