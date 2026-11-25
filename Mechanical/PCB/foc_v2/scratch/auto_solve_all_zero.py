import math, random
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

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

def eval_state(P):
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

    return overlaps, hole_errs, bboxes

# Import current base placements
from optimize_clean_layout import P

# Locked anchors that MUST NOT MOVE:
LOCKED = {
    'H1', 'H2', 'H3', 'H4', # Mounting holes
    'U2',                   # Encoder locked at 100, 100
    'J1', 'J2', 'J3',       # Motor wire pads
    'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', # 6 MOSFETs
    'J8', 'J9', 'J7', 'J10', # South connector bank
    'J11',                  # Power connector
    'U1', 'IC1'             # MCU & Gate Driver
}

# Initial manual fixes for the known issues:
P['J11'] = (121.0, 99.5, 270, 'F.Cu')
P['F1']  = (125.0, 112.5, 90, 'F.Cu')
P['D6']  = (124.0, 120.0, 90, 'F.Cu')

# Place L1 in safe clear zone:
# (111.0, 89.0) has dist to H4(115.556, 84.444): sqrt(4.55^2 + 4.55^2) = 6.44 mm!
P['L1']  = (111.0, 89.0, 0, 'F.Cu')
P['D4']  = (111.0, 94.5, 0, 'F.Cu')
P['C16'] = (111.0, 98.0, 90, 'F.Cu')
P['C17'] = (111.0, 100.8, 90, 'F.Cu')
P['R53'] = (116.0, 90.0, 0, 'F.Cu')
P['R54'] = (116.0, 92.0, 0, 'F.Cu')

# Connectors bank adjustments:
P['J8']  = (76.5, 122.5, 0, 'F.Cu')  # CAN_IN
P['J9']  = (88.0, 122.5, 0, 'F.Cu')  # CAN_OUT
P['J7']  = (99.5, 128.0, 0, 'F.Cu')  # Type-C
P['J10'] = (109.0, 122.5, 0, 'F.Cu') # SWD

# Decoupling caps around U1:
P['C10'] = (96.5, 118.8, 0, 'F.Cu')
P['C11'] = (103.5, 118.8, 0, 'F.Cu')

# Shunts R47..R49:
P['R47'] = (93.0, 84.8, 90, 'F.Cu')
P['R48'] = (100.0, 84.8, 90, 'F.Cu')
P['R49'] = (107.0, 84.8, 90, 'F.Cu')
P['NT1'] = (93.0, 83.0, 90, 'F.Cu')
P['NT2'] = (93.0, 86.6, 90, 'F.Cu')
P['NT3'] = (100.0, 83.0, 90, 'F.Cu')
P['NT4'] = (100.0, 86.6, 90, 'F.Cu')
P['NT5'] = (107.0, 83.0, 90, 'F.Cu')
P['NT6'] = (107.0, 86.6, 90, 'F.Cu')

# Gate resistors:
P['R1'] = (84.0, 80.0, 0, 'F.Cu')
P['R2'] = (89.5, 80.0, 0, 'F.Cu')
P['R3'] = (96.0, 80.0, 0, 'F.Cu')
P['R4'] = (102.5, 80.0, 0, 'F.Cu')
P['R5'] = (109.5, 80.0, 0, 'F.Cu')
P['R7'] = (115.5, 80.0, 0, 'F.Cu')

# DRV resistors:
P['R6']  = (90.5, 89.8, 0, 'F.Cu')
P['R8']  = (90.5, 91.8, 0, 'F.Cu')
P['R9']  = (90.5, 93.8, 0, 'F.Cu')
P['R10'] = (90.5, 95.8, 0, 'F.Cu')
P['R50'] = (90.5, 97.8, 0, 'F.Cu')
P['R51'] = (88.0, 93.5, 0, 'F.Cu')
P['R52'] = (88.0, 95.5, 0, 'F.Cu')

P['R55'] = (109.5, 89.8, 0, 'F.Cu')
P['R56'] = (109.5, 91.8, 0, 'F.Cu')
P['R57'] = (109.5, 93.8, 0, 'F.Cu')
P['R58'] = (109.5, 95.8, 0, 'F.Cu')
P['R59'] = (109.5, 97.8, 0, 'F.Cu')
P['R60'] = (109.5, 99.8, 0, 'F.Cu')

# Sense RC filters (at y = 101.5):
P['R37'] = (92.0, 101.5, 0, 'F.Cu')
P['C54'] = (95.0, 101.5, 0, 'F.Cu')
P['R38'] = (98.0, 101.5, 0, 'F.Cu')
P['C55'] = (101.0, 101.5, 0, 'F.Cu')
P['R39'] = (104.0, 101.5, 0, 'F.Cu')
P['C56'] = (107.0, 101.5, 0, 'F.Cu')

# Test points:
P['TP2'] = (89.5, 101.5, 0, 'F.Cu')
P['TP3'] = (112.5, 101.5, 0, 'F.Cu')

# Crystal passives:
P['R44'] = (86.0, 110.0, 0, 'F.Cu')
P['R32'] = (88.5, 110.0, 0, 'F.Cu')
P['R34'] = (88.5, 112.0, 0, 'F.Cu')

# LEDs and resistors:
P['D1']  = (108.0, 118.0, 0, 'F.Cu')
P['R33'] = (111.5, 118.0, 0, 'F.Cu')
P['D2']  = (108.0, 120.0, 0, 'F.Cu')
P['R35'] = (111.5, 120.0, 0, 'F.Cu')
P['D3']  = (108.0, 122.0, 0, 'F.Cu')
P['R36'] = (111.5, 122.0, 0, 'F.Cu')

# USB passives on B.Cu (spaced cleanly):
P['U8']  = (99.5, 121.5, 0, 'B.Cu')
P['Q7']  = (105.0, 121.5, 0, 'B.Cu')
P['R40'] = (96.5, 124.0, 0, 'B.Cu')
P['R41'] = (96.5, 126.0, 0, 'B.Cu')
P['R42'] = (103.0, 124.0, 0, 'B.Cu')
P['R43'] = (103.0, 126.0, 0, 'B.Cu')
P['C59'] = (99.5, 127.5, 0, 'B.Cu')

overlaps, hole_errs, bboxes = eval_state(P)
print(f"After manual tuning: overlaps={len(overlaps)}, hole_errs={len(hole_errs)}")
for r1, r2, dx, dy, b1, b2 in overlaps:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, d in hole_errs:
    print(f"  HOLE: {h} <--> {r} : dist={d:.2f}")
