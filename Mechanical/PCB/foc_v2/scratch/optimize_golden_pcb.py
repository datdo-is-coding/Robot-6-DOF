import math, sys
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 120.0

ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

delta_h = 22.0 / math.sqrt(2) # 15.55635
HOLES = {
    "H3": (100.0 - delta_h, 100.0 - delta_h), # (84.444, 84.444)
    "H4": (100.0 + delta_h, 100.0 - delta_h), # (115.556, 84.444)
    "H2": (100.0 - delta_h, 100.0 + delta_h), # (84.444, 115.556)
    "H1": (100.0 + delta_h, 100.0 + delta_h)  # (115.556, 115.556)
}
R_KO = 2.45

def build_placement():
    P = {}

    # 1. MOUNTING HOLES (PCD 44mm)
    for h, (hx, hy) in HOLES.items():
        P[h] = (hx, hy, 0, 'F.Cu')

    # 2. MOTOR TERMINALS at Y = 71.2 (R <= 31.2 mm, generous > 3.8mm margin to top edge)
    P['J1'] = (88.0, 71.2, 0, 'F.Cu')
    P['J2'] = (100.0, 71.0, 0, 'F.Cu')
    P['J3'] = (112.0, 71.2, 0, 'F.Cu')

    # DC Bus Caps at Y = 68.0 (above FETs, between motor pads)
    # J1 is at 88.0, J2 at 100.0, J3 at 112.0
    P['C_BUS1'] = (82.0, 68.2, 0, 'F.Cu')
    P['C_BUS2'] = (94.0, 68.2, 0, 'F.Cu')
    P['C_BUS3'] = (106.0, 68.2, 0, 'F.Cu')

    # 3. 6 INVERTER MOSFETS at Y = 77.0 (Clean horizontal row)
    # FET width=7.16, height=5.66. At rot=90/270, width=5.66, height=7.16 (Y in [73.42, 80.58])
    P['Q1'] = (83.5, 77.0, 90, 'F.Cu')
    P['Q2'] = (90.1, 77.0, 270, 'F.Cu')
    P['Q3'] = (96.7, 77.0, 90, 'F.Cu')
    P['Q4'] = (103.3, 77.0, 270, 'F.Cu')
    P['Q5'] = (109.9, 77.0, 90, 'F.Cu')
    P['Q6'] = (116.5, 77.0, 270, 'F.Cu')

    # Gate resistors at Y = 72.5 (above FETs)
    # Resistor 0603: width 2.96, height 1.46 (Y in [71.77, 73.23])
    # J1..3 are at 88.0, 100.0, 112.0.
    P['R1'] = (83.5, 72.3, 0, 'F.Cu')
    P['R2'] = (90.1, 72.3, 0, 'F.Cu')
    P['R3'] = (96.7, 72.3, 0, 'F.Cu')
    P['R4'] = (103.3, 72.3, 0, 'F.Cu')
    P['R5'] = (109.9, 72.3, 0, 'F.Cu')
    P['R7'] = (116.5, 72.3, 0, 'F.Cu')

    # Shunts at Y = 82.5 (rot=90: width 7.66 along X, height 3.86 along Y -> Y in [80.57, 84.43])
    P['R47'] = (91.5, 82.5, 90, 'F.Cu')
    P['R48'] = (100.0, 82.5, 90, 'F.Cu')
    P['R49'] = (108.5, 82.5, 90, 'F.Cu')

    # Net ties (Kelvin sense)
    P['NT1'] = (91.5, 80.7, 90, 'F.Cu')
    P['NT2'] = (91.5, 84.3, 90, 'F.Cu')
    P['NT3'] = (100.0, 80.7, 90, 'F.Cu')
    P['NT4'] = (100.0, 84.3, 90, 'F.Cu')
    P['NT5'] = (108.5, 80.7, 90, 'F.Cu')
    P['NT6'] = (108.5, 84.3, 90, 'F.Cu')

    # Bulk caps: West at rot=0, East at rot=180
    # Cylinder center at (75.5, 84.0) and (124.5, 84.0)
    P['C_BULK1'] = (73.0, 84.0, 0, 'F.Cu')
    P['C63']     = (127.0, 84.0, 180, 'F.Cu')

    # 4. GATE DRIVER IC1 at (100.0, 89.5)
    # IC1: 8.26 x 8.26 -> Y in [85.37, 93.63]
    P['IC1'] = (100.0, 89.5, 0, 'F.Cu')

    # Bootstrap & DRV caps on West (X = 94.0) and East (X = 106.0)
    P['C1']  = (94.0, 86.2, 0, 'F.Cu')
    P['C2']  = (94.0, 88.0, 0, 'F.Cu')
    P['C3']  = (94.0, 89.8, 0, 'F.Cu')
    P['C12'] = (94.0, 91.8, 0, 'F.Cu')
    P['C13'] = (94.0, 93.8, 0, 'F.Cu')

    P['C15'] = (106.0, 86.2, 0, 'F.Cu')
    P['C18'] = (106.0, 88.0, 0, 'F.Cu')
    P['C19'] = (106.0, 89.8, 0, 'F.Cu')
    P['C20'] = (106.0, 91.8, 0, 'F.Cu')
    P['C21'] = (106.0, 93.8, 0, 'F.Cu')
    P['C64'] = (106.0, 95.8, 0, 'F.Cu')

    # DRV config resistors (West at X = 90.8, East at X = 109.2)
    P['R6']  = (90.8, 86.2, 0, 'F.Cu')
    P['R8']  = (90.8, 88.0, 0, 'F.Cu')
    P['R9']  = (90.8, 89.8, 0, 'F.Cu')
    P['R10'] = (90.8, 91.8, 0, 'F.Cu')
    P['R50'] = (90.8, 93.8, 0, 'F.Cu')
    P['R51'] = (87.5, 89.8, 0, 'F.Cu')
    P['R52'] = (87.5, 92.0, 0, 'F.Cu')

    P['R55'] = (109.2, 86.2, 0, 'F.Cu')
    P['R56'] = (109.2, 88.0, 0, 'F.Cu')
    P['R57'] = (109.2, 89.8, 0, 'F.Cu')
    P['R58'] = (109.2, 91.8, 0, 'F.Cu')
    P['R59'] = (109.2, 93.8, 0, 'F.Cu')
    P['R60'] = (109.2, 95.8, 0, 'F.Cu')
    P['TP1'] = (87.5, 87.5, 0, 'F.Cu')
    P['TP2'] = (87.5, 94.5, 0, 'F.Cu')
    P['TP3'] = (109.2, 97.8, 0, 'F.Cu')

    # Current sense filters at Y = 96.5
    P['R37'] = (91.0, 96.5, 0, 'F.Cu')
    P['C54'] = (94.0, 96.5, 0, 'F.Cu')
    P['R38'] = (97.0, 96.5, 0, 'F.Cu')
    P['C55'] = (100.0, 96.5, 0, 'F.Cu')
    P['R39'] = (103.0, 96.5, 0, 'F.Cu')
    P['C56'] = (106.0, 96.5, 0, 'F.Cu')

    # 5. Buck Converter & Power Input (East Wing: X in [114, 126])
    # H4 is at (115.556, 84.444).
    P['L1']  = (122.0, 90.0, 0, 'F.Cu')
    P['D4']  = (115.5, 90.0, 0, 'F.Cu')
    P['C16'] = (115.5, 93.0, 90, 'F.Cu')
    P['C17'] = (115.5, 95.5, 90, 'F.Cu')
    P['R53'] = (118.5, 93.0, 0, 'F.Cu')
    P['R54'] = (118.5, 95.0, 0, 'F.Cu')

    P['J11'] = (121.0, 102.0, 270, 'F.Cu')
    P['F1']  = (122.0, 110.0, 90, 'F.Cu')
    P['D6']  = (122.0, 115.5, 90, 'F.Cu')

    # 6. MCU U1 at (100.0, 103.5)
    # U1: 13.4 x 13.4 -> X in [93.3, 106.7], Y in [96.8, 110.2]
    P['U1']  = (100.0, 103.5, 0, 'F.Cu')

    # Decoupling caps around U1
    P['C4']  = (96.5, 96.0, 0, 'F.Cu')
    P['C5']  = (103.5, 96.0, 0, 'F.Cu')
    P['C10'] = (90.0, 108.5, 0, 'F.Cu')
    P['C11'] = (110.0, 108.5, 0, 'F.Cu')

    P['C51'] = (91.5, 101.0, 90, 'F.Cu')
    P['C52'] = (91.5, 103.5, 90, 'F.Cu')
    P['C53'] = (91.5, 106.0, 90, 'F.Cu')

    P['C6']  = (108.5, 101.0, 90, 'F.Cu')
    P['C7']  = (108.5, 103.5, 90, 'F.Cu')
    P['C50'] = (108.5, 106.0, 90, 'F.Cu')

    # 3.3V LDO U10 and caps
    P['U10'] = (114.0, 101.0, 0, 'F.Cu')
    P['C57'] = (114.0, 104.0, 0, 'F.Cu')
    P['C58'] = (114.0, 106.0, 0, 'F.Cu')

    # Crystal Y1 & passives
    P['FB1'] = (88.5, 99.0, 0, 'F.Cu')
    P['Y1']  = (86.0, 102.5, 0, 'F.Cu')
    P['C8']  = (82.5, 101.0, 90, 'F.Cu')
    P['C9']  = (82.5, 103.5, 90, 'F.Cu')
    P['R44'] = (85.5, 105.5, 0, 'F.Cu')
    P['R32'] = (88.5, 105.5, 0, 'F.Cu')
    P['R34'] = (88.5, 107.5, 0, 'F.Cu')

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

    # 7. SOUTH CONNECTORS (Y_front = 120.0 mm):
    P['J8']  = (73.5,   110.69, 0, 'F.Cu')
    P['J7']  = (92.25,  115.82, 0, 'F.Cu')
    P['J10'] = (100.25, 110.69, 0, 'F.Cu')
    P['J9']  = (121.0,  110.69, 0, 'F.Cu')

    # 8. Bottom layer items on B.Cu
    P['U2']  = (100.0, 100.0, 0, 'B.Cu') # Encoder centered at (100, 100)
    P['C14'] = (100.0, 103.5, 0, 'B.Cu')
    P['R61'] = (100.0, 96.5, 90, 'B.Cu')

    P['U8']  = (92.25, 108.5, 0, 'B.Cu')
    P['C59'] = (92.25, 111.5, 0, 'B.Cu')
    P['Q7']  = (92.25, 114.0, 0, 'B.Cu')
    P['R40'] = (87.5, 114.0, 0, 'B.Cu')
    P['R41'] = (89.0, 114.0, 0, 'B.Cu')
    P['R42'] = (95.5, 114.0, 0, 'B.Cu')
    P['R43'] = (97.0, 114.0, 0, 'B.Cu')

    return P

P = build_placement()
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
for r1, r2, dx, dy in overlaps:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in hole_errs:
    print(f"  HOLE: {h} <--> {r} : pen={pen:.2f}")
for r, msg in oob[:10]:
    print(f"  OOB: {r} : {msg}")
