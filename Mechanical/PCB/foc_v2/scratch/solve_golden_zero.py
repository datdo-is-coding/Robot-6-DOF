import math, sys
sys.path.insert(0, 'scratch')
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 120.2

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
R_KO = 2.95

P = {}

# 1. MOUNTING HOLES (PCD 44mm)
for h, (hx, hy) in HOLES.items():
    P[h] = (hx, hy, 0, 'F.Cu')

# 2. MOTOR TERMINALS (Generous > 3.0mm margin to top edge)
P['J1'] = (88.0, 71.0, 0, 'F.Cu')
P['J2'] = (100.0, 70.0, 0, 'F.Cu')
P['J3'] = (112.0, 71.0, 0, 'F.Cu')

# 3. 6 INVERTER MOSFETS at Y = 76.5 (Clean row)
P['Q1'] = (83.5, 76.5, 90, 'F.Cu')
P['Q2'] = (90.1, 76.5, 270, 'F.Cu')
P['Q3'] = (96.7, 76.5, 90, 'F.Cu')
P['Q4'] = (103.3, 76.5, 270, 'F.Cu')
P['Q5'] = (109.9, 76.5, 90, 'F.Cu')
P['Q6'] = (116.5, 76.5, 270, 'F.Cu')

# Gate resistors at Y = 72.8 (above FETs)
P['R1'] = (83.5, 72.8, 0, 'F.Cu')
P['R2'] = (89.5, 72.8, 0, 'F.Cu')
P['R3'] = (96.0, 72.8, 0, 'F.Cu')
P['R4'] = (102.5, 72.8, 0, 'F.Cu')
P['R5'] = (109.5, 72.8, 0, 'F.Cu')
P['R7'] = (116.5, 72.8, 0, 'F.Cu')

# DC Bus Caps
P['C_BUS1'] = (82.5, 69.2, 0, 'F.Cu')
P['C_BUS2'] = (94.0, 69.2, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 69.2, 0, 'F.Cu')

# Shunts at Y = 81.8
P['R47'] = (93.0, 81.8, 90, 'F.Cu')
P['R48'] = (100.0, 81.8, 90, 'F.Cu')
P['R49'] = (107.0, 81.8, 90, 'F.Cu')

# Net ties
P['NT1'] = (93.0, 80.0, 90, 'F.Cu')
P['NT2'] = (93.0, 83.6, 90, 'F.Cu')
P['NT3'] = (100.0, 80.0, 90, 'F.Cu')
P['NT4'] = (100.0, 83.6, 90, 'F.Cu')
P['NT5'] = (107.0, 80.0, 90, 'F.Cu')
P['NT6'] = (107.0, 83.6, 90, 'F.Cu')

# Bulk caps (D10mm cylinder): rot=0 on West, rot=180 on East
P['C_BULK1'] = (76.0, 84.0, 0, 'F.Cu')
P['C63']     = (124.0, 84.0, 180, 'F.Cu')

# 4. GATE DRIVER IC1 at (100.0, 89.0)
P['IC1'] = (100.0, 89.0, 0, 'F.Cu')

# Bootstrap & DRV caps
P['C1']  = (94.0, 86.5, 0, 'F.Cu')
P['C2']  = (94.0, 88.5, 0, 'F.Cu')
P['C3']  = (94.0, 90.5, 0, 'F.Cu')
P['C12'] = (94.0, 92.8, 0, 'F.Cu')
P['C13'] = (94.0, 95.0, 0, 'F.Cu')

P['C15'] = (106.0, 86.5, 0, 'F.Cu')
P['C18'] = (106.0, 88.5, 0, 'F.Cu')
P['C19'] = (106.0, 90.5, 0, 'F.Cu')
P['C20'] = (106.0, 92.5, 0, 'F.Cu')
P['C21'] = (106.0, 94.5, 0, 'F.Cu')
P['C64'] = (106.0, 96.5, 0, 'F.Cu')

# DRV config resistors
P['R6']  = (91.0, 86.5, 0, 'F.Cu')
P['R8']  = (91.0, 88.3, 0, 'F.Cu')
P['R9']  = (91.0, 90.1, 0, 'F.Cu')
P['R10'] = (91.0, 91.9, 0, 'F.Cu')
P['R50'] = (91.0, 93.7, 0, 'F.Cu')
P['R51'] = (88.0, 90.1, 0, 'F.Cu')
P['R52'] = (88.0, 92.5, 0, 'F.Cu')

P['R55'] = (109.0, 86.5, 0, 'F.Cu')
P['R56'] = (109.0, 88.3, 0, 'F.Cu')
P['R57'] = (109.0, 90.1, 0, 'F.Cu')
P['R58'] = (109.0, 91.9, 0, 'F.Cu')
P['R59'] = (109.0, 93.7, 0, 'F.Cu')
P['R60'] = (109.0, 95.5, 0, 'F.Cu')
P['TP1'] = (86.0, 88.0, 0, 'F.Cu')
P['TP2'] = (88.0, 96.0, 0, 'F.Cu')
P['TP3'] = (109.0, 97.5, 0, 'F.Cu')

# Current sense filters
P['R37'] = (91.0, 96.5, 0, 'F.Cu')
P['C54'] = (93.5, 96.5, 0, 'F.Cu')
P['R38'] = (97.0, 96.5, 0, 'F.Cu')
P['C55'] = (99.5, 96.5, 0, 'F.Cu')
P['R39'] = (103.0, 96.5, 0, 'F.Cu')
P['C56'] = (105.5, 96.5, 0, 'F.Cu')

# 5. Buck Converter & Power Input (East Wing)
P['J11'] = (120.5, 97.0, 270, 'F.Cu')
P['L1']  = (121.0, 89.0, 0, 'F.Cu')
P['D4']  = (115.0, 89.5, 0, 'F.Cu')
P['C16'] = (115.0, 92.5, 90, 'F.Cu')
P['C17'] = (115.0, 95.0, 90, 'F.Cu')
P['R53'] = (118.0, 92.0, 0, 'F.Cu')
P['R54'] = (118.0, 94.0, 0, 'F.Cu')

P['F1']  = (122.0, 108.0, 90, 'F.Cu')
P['D6']  = (122.0, 114.5, 90, 'F.Cu')

# 6. MCU U1 at (100.0, 102.5)
P['U1']  = (100.0, 102.5, 0, 'F.Cu')

P['C4']  = (96.5, 95.5, 0, 'F.Cu')
P['C5']  = (103.5, 95.5, 0, 'F.Cu')
P['C10'] = (90.0, 107.5, 0, 'F.Cu')
P['C11'] = (110.0, 107.5, 0, 'F.Cu')

P['C51'] = (91.5, 100.0, 90, 'F.Cu')
P['C52'] = (91.5, 102.5, 90, 'F.Cu')
P['C53'] = (91.5, 105.0, 90, 'F.Cu')

P['C6']  = (108.5, 100.0, 90, 'F.Cu')
P['C7']  = (108.5, 102.5, 90, 'F.Cu')
P['C50'] = (108.5, 105.0, 90, 'F.Cu')

P['U10'] = (114.0, 101.0, 0, 'F.Cu')
P['C57'] = (114.0, 104.0, 0, 'F.Cu')
P['C58'] = (114.0, 106.0, 0, 'F.Cu')

P['FB1'] = (88.5, 98.0, 0, 'F.Cu')
P['Y1']  = (86.0, 101.5, 0, 'F.Cu')
P['C8']  = (82.5, 100.0, 90, 'F.Cu')
P['C9']  = (82.5, 102.5, 90, 'F.Cu')
P['R44'] = (85.5, 104.0, 0, 'F.Cu')
P['R32'] = (88.5, 104.0, 0, 'F.Cu')
P['R34'] = (88.5, 106.0, 0, 'F.Cu')

# CAN Subsystem (West Wing)
P['U9']  = (76.0, 98.0, 0, 'F.Cu')
P['JP1'] = (76.0, 101.5, 0, 'F.Cu')
P['R45'] = (76.0, 104.0, 0, 'F.Cu')
P['R46'] = (76.0, 106.0, 0, 'F.Cu')
P['C60'] = (72.0, 96.0, 90, 'F.Cu')
P['C61'] = (72.0, 98.5, 90, 'F.Cu')
P['C62'] = (72.0, 101.0, 90, 'F.Cu')

# Status LEDs
P['D1']  = (76.0, 88.0, 0, 'F.Cu')
P['R33'] = (79.0, 88.0, 0, 'F.Cu')
P['D2']  = (76.0, 90.5, 0, 'F.Cu')
P['R35'] = (79.0, 90.5, 0, 'F.Cu')
P['D3']  = (76.0, 93.0, 0, 'F.Cu')
P['R36'] = (79.0, 93.0, 0, 'F.Cu')

# 7. SOUTH CONNECTORS BANK (Y_front = 120.0 mm):
P['J8']  = (74.0,  110.80, 0, 'F.Cu')
P['J7']  = (92.5,  116.21, 0, 'F.Cu')
P['J10'] = (100.0, 110.80, 0, 'F.Cu')
P['J9']  = (121.0, 110.80, 0, 'F.Cu')

# Bottom layer passives
P['U8']  = (92.5, 109.0, 0, 'B.Cu')
P['C59'] = (92.5, 112.0, 0, 'B.Cu')
P['Q7']  = (100.0, 115.0, 0, 'B.Cu')
P['U2']  = (92.5, 115.0, 0, 'B.Cu')
P['R40'] = (88.0, 115.0, 0, 'B.Cu')
P['R41'] = (89.5, 115.0, 0, 'B.Cu')
P['R42'] = (95.5, 115.0, 0, 'B.Cu')
P['R43'] = (97.0, 115.0, 0, 'B.Cu')

# Encoder
P['C14'] = (100.0, 102.5, 0, 'B.Cu')
P['R61'] = (100.0, 96.5, 90, 'B.Cu')

bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    bboxes[ref] = get_world_bbox(ref, is_b, shapes, x, y, rot)

overlaps = []
refs = list(bboxes.keys())
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        r1, r2 = refs[i], refs[j]
        if (r1, r2) in ALLOWED or (r2, r1) in ALLOWED: continue
        b1, b2 = bboxes[r1], bboxes[r2]
        if b1['layer'] != b2['layer']: continue
        if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
            dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
            dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
            overlaps.append((r1, r2, dx, dy))

hole_errs = []
for hname, (hx, hy) in HOLES.items():
    for r, b in bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx_box = max(b['x1'], min(hx, b['x2']))
        cy_box = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx_box - hx, cy_box - hy)
        if d < R_KO:
            hole_errs.append((hname, r, R_KO - d))

oob = []
for r, b in bboxes.items():
    for px in [b['x1'], b['x2']]:
        for py in [b['y1'], b['y2']]:
            if py > y_cut + 0.05:
                oob.append((r, f"Y={py:.2f} > {y_cut}"))
            d = math.hypot(px - 100.0, py - 100.0)
            if d > 34.95:
                oob.append((r, f"dist={d:.2f} > 34.95"))

print(f"==========================================")
print(f"TOTAL COMPONENTS: {len(P)} / 124")
print(f"OVERLAPS DETECTED: {len(overlaps)}")
print(f"HOLE COLLISIONS: {len(hole_errs)}")
print(f"OUT OF BOUNDS: {len(oob)}")
print(f"==========================================")
for r1, r2, dx, dy in overlaps[:15]:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in hole_errs:
    print(f"  HOLE: {h} <--> {r} : pen={pen:.2f}")
for r, msg in oob[:10]:
    print(f"  OOB: {r} : {msg}")
