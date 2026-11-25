import math, sys
sys.path.insert(0, 'scratch')
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Center and radius
cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 123.5 # Flat cut at Y = 123.5 mm

# Allowed overlaps
ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

# 4 Mounting holes at PCD 44mm (r = 22.0mm)
HOLES = {
    "H3": (84.444, 84.444),
    "H4": (115.556, 84.444),
    "H2": (84.444, 115.556),
    "H1": (115.556, 115.556)
}
R_KO = 2.95

# Let's start from a clean architecture:
P = {}

# 1. MOUNTING HOLES
for h, coord in HOLES.items():
    P[h] = (coord[0], coord[1], 0, 'F.Cu')

# 2. MOTOR PHASE TERMINALS (North: deep inside, perfectly circular pads)
P['J1'] = (88.0, 71.0, 0, 'F.Cu')
P['J2'] = (100.0, 70.0, 0, 'F.Cu')
P['J3'] = (112.0, 71.0, 0, 'F.Cu')

# 3. 6 INVERTER MOSFETS at Y = 77.0
# Y extent with rot=90/270: 77.0 +/- 3.58 = [73.42, 80.58]
# Margin to J1..J3 at Y=71.0 (bottom 72.88): 73.42 - 72.88 = 0.54 mm
# Margin to H3, H4 at Y=84.444 (top 81.49): 81.49 - 80.58 = 0.91 mm!
P['Q1'] = (83.5, 77.0, 90, 'F.Cu')
P['Q2'] = (90.1, 77.0, 270, 'F.Cu')
P['Q3'] = (96.7, 77.0, 90, 'F.Cu')
P['Q4'] = (103.3, 77.0, 270, 'F.Cu')
P['Q5'] = (109.9, 77.0, 90, 'F.Cu')
P['Q6'] = (116.5, 77.0, 270, 'F.Cu')

# Gate resistors at Y = 73.5 (placed above MOSFETs)
P['R1'] = (83.5, 73.2, 0, 'F.Cu')
P['R2'] = (89.5, 73.2, 0, 'F.Cu')
P['R3'] = (96.0, 73.2, 0, 'F.Cu')
P['R4'] = (102.5, 73.2, 0, 'F.Cu')
P['R5'] = (109.5, 73.2, 0, 'F.Cu')
P['R7'] = (116.5, 73.2, 0, 'F.Cu')

# DC Bus Caps (1210: 3.5 x 2.8 at rot=0) - placed above gate resistors
P['C_BUS1'] = (82.5, 69.5, 0, 'F.Cu')
P['C_BUS2'] = (94.0, 69.5, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 69.5, 0, 'F.Cu')

# 3 Shunts (2512 at rot=90: width 7.66, height 3.86) at Y = 82.5
P['R47'] = (93.0, 82.5, 90, 'F.Cu')
P['R48'] = (100.0, 82.5, 90, 'F.Cu')
P['R49'] = (107.0, 82.5, 90, 'F.Cu')

# Net ties
P['NT1'] = (93.0, 81.0, 90, 'F.Cu')
P['NT2'] = (93.0, 84.0, 90, 'F.Cu')
P['NT3'] = (100.0, 81.0, 90, 'F.Cu')
P['NT4'] = (100.0, 84.0, 90, 'F.Cu')
P['NT5'] = (107.0, 81.0, 90, 'F.Cu')
P['NT6'] = (107.0, 84.0, 90, 'F.Cu')

# Bulk caps (D10mm cylinder): rot=0 on West (extends +X), rot=180 on East (extends -X)
P['C_BULK1'] = (74.0, 85.0, 0, 'F.Cu')
P['C63']     = (126.0, 85.0, 180, 'F.Cu')

# 4. GATE DRIVER IC1 at (100.0, 90.0)
P['IC1'] = (100.0, 90.0, 0, 'F.Cu')

# Bootstrap Caps
P['C1'] = (94.0, 87.5, 0, 'F.Cu')
P['C2'] = (94.0, 89.5, 0, 'F.Cu')
P['C3'] = (94.0, 91.5, 0, 'F.Cu')
P['C12'] = (94.0, 93.8, 0, 'F.Cu')
P['C13'] = (94.0, 96.0, 0, 'F.Cu')

P['C15'] = (106.0, 87.5, 0, 'F.Cu')
P['C18'] = (106.0, 89.5, 0, 'F.Cu')
P['C19'] = (106.0, 91.5, 0, 'F.Cu')
P['C20'] = (106.0, 93.5, 0, 'F.Cu')
P['C21'] = (106.0, 95.5, 0, 'F.Cu')
P['C64'] = (106.0, 97.5, 0, 'F.Cu')

# DRV config resistors
P['R6']  = (91.0, 87.5, 0, 'F.Cu')
P['R8']  = (91.0, 89.3, 0, 'F.Cu')
P['R9']  = (91.0, 91.1, 0, 'F.Cu')
P['R10'] = (91.0, 92.9, 0, 'F.Cu')
P['R50'] = (91.0, 94.7, 0, 'F.Cu')
P['R51'] = (88.0, 91.1, 0, 'F.Cu')
P['R52'] = (88.0, 93.5, 0, 'F.Cu')

P['R55'] = (109.0, 87.5, 0, 'F.Cu')
P['R56'] = (109.0, 89.3, 0, 'F.Cu')
P['R57'] = (109.0, 91.1, 0, 'F.Cu')
P['R58'] = (109.0, 92.9, 0, 'F.Cu')
P['R59'] = (109.0, 94.7, 0, 'F.Cu')
P['R60'] = (109.0, 96.5, 0, 'F.Cu')
P['TP1'] = (86.0, 89.0, 0, 'F.Cu')
P['TP2'] = (88.0, 98.0, 0, 'F.Cu')
P['TP3'] = (109.0, 98.5, 0, 'F.Cu')

# Current sense filters
P['R37'] = (91.0, 98.0, 0, 'F.Cu')
P['C54'] = (93.5, 98.0, 0, 'F.Cu')
P['R38'] = (97.0, 98.0, 0, 'F.Cu')
P['C55'] = (99.5, 98.0, 0, 'F.Cu')
P['R39'] = (103.0, 98.0, 0, 'F.Cu')
P['C56'] = (105.5, 98.0, 0, 'F.Cu')

# 5. Buck Converter & Power Input (East Wing)
P['J11'] = (120.5, 96.0, 270, 'F.Cu')
P['L1']  = (122.0, 88.0, 0, 'F.Cu')
P['D4']  = (115.0, 90.0, 0, 'F.Cu')
P['C16'] = (115.0, 93.0, 90, 'F.Cu')
P['C17'] = (115.0, 95.5, 90, 'F.Cu')
P['R53'] = (118.0, 92.5, 0, 'F.Cu')
P['R54'] = (118.0, 94.5, 0, 'F.Cu')

P['F1']  = (122.0, 108.0, 90, 'F.Cu')
P['D6']  = (122.0, 114.5, 90, 'F.Cu')

# 6. MCU U1 at (100.0, 103.5)
P['U1']  = (100.0, 103.5, 0, 'F.Cu')

P['C4']  = (96.5, 97.0, 0, 'F.Cu')
P['C5']  = (103.5, 97.0, 0, 'F.Cu')
P['C10'] = (90.0, 108.5, 0, 'F.Cu')
P['C11'] = (110.0, 108.5, 0, 'F.Cu')

P['C51'] = (91.5, 101.0, 90, 'F.Cu')
P['C52'] = (91.5, 103.5, 90, 'F.Cu')
P['C53'] = (91.5, 106.0, 90, 'F.Cu')

P['C6']  = (108.5, 101.0, 90, 'F.Cu')
P['C7']  = (108.5, 103.5, 90, 'F.Cu')
P['C50'] = (108.5, 106.0, 90, 'F.Cu')

P['U10'] = (114.0, 102.0, 0, 'F.Cu')
P['C57'] = (114.0, 105.0, 0, 'F.Cu')
P['C58'] = (114.0, 107.0, 0, 'F.Cu')

P['FB1'] = (88.5, 99.0, 0, 'F.Cu')
P['Y1']  = (86.0, 102.5, 0, 'F.Cu')
P['C8']  = (82.5, 101.0, 90, 'F.Cu')
P['C9']  = (82.5, 103.5, 90, 'F.Cu')
P['R44'] = (85.5, 105.0, 0, 'F.Cu')
P['R32'] = (88.5, 105.0, 0, 'F.Cu')
P['R34'] = (88.5, 107.0, 0, 'F.Cu')

# CAN Subsystem (West Wing)
P['U9']  = (76.0, 99.0, 0, 'F.Cu')
P['JP1'] = (76.0, 102.5, 0, 'F.Cu')
P['R45'] = (76.0, 105.0, 0, 'F.Cu')
P['R46'] = (76.0, 107.0, 0, 'F.Cu')
P['C60'] = (72.0, 97.0, 90, 'F.Cu')
P['C61'] = (72.0, 99.5, 90, 'F.Cu')
P['C62'] = (72.0, 102.0, 90, 'F.Cu')

# Status LEDs
P['D1']  = (76.0, 89.0, 0, 'F.Cu')
P['R33'] = (79.0, 89.0, 0, 'F.Cu')
P['D2']  = (76.0, 91.5, 0, 'F.Cu')
P['R35'] = (79.0, 91.5, 0, 'F.Cu')
P['D3']  = (76.0, 94.0, 0, 'F.Cu')
P['R36'] = (79.0, 94.0, 0, 'F.Cu')

# 7. SOUTH CONNECTORS BANK (Clean line at Y_front = 120.0 mm):
# J8: CAN_IN (3-pin XH)
P['J8']  = (74.0,  110.80, 0, 'F.Cu')
# J7: Type-C (Center-left)
P['J7']  = (92.5,  116.21, 0, 'F.Cu')
# J10: SWD (5-pin XH, Center-right)
P['J10'] = (100.0, 110.80, 0, 'F.Cu')
# J9: CAN_OUT (3-pin XH)
P['J9']  = (121.0, 110.80, 0, 'F.Cu')

# Bottom layer passives
P['U8']  = (92.5, 110.0, 0, 'B.Cu')
P['C59'] = (92.5, 113.0, 0, 'B.Cu')
P['Q7']  = (100.0, 116.0, 0, 'B.Cu')
P['U2']  = (92.5, 116.0, 0, 'B.Cu')
P['R40'] = (88.0, 116.0, 0, 'B.Cu')
P['R41'] = (89.5, 116.0, 0, 'B.Cu')
P['R42'] = (95.5, 116.0, 0, 'B.Cu')
P['R43'] = (97.0, 116.0, 0, 'B.Cu')

# Encoder
P['C14'] = (100.0, 103.0, 0, 'B.Cu')
P['R61'] = (100.0, 97.0, 90, 'B.Cu')

print(f"Total components defined: {len(P)}")

# Calculate exact bounding boxes
bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    bboxes[ref] = get_world_bbox(ref, is_b, shapes, x, y, rot)

# Overlap check
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

# Hole collision check
hole_errs = []
for hname, (hx, hy) in HOLES.items():
    for r, b in bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx_box = max(b['x1'], min(hx, b['x2']))
        cy_box = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx_box - hx, cy_box - hy)
        if d < R_KO:
            hole_errs.append((hname, r, d))

# Out of bounds check
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
for r1, r2, dx, dy, b1, b2 in overlaps:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, d in hole_errs:
    print(f"  HOLE: {h} <--> {r} : dist={d:.2f}")
for r, msg in oob[:10]:
    print(f"  OOB: {r} : {msg}")
