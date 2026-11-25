import math, random, sys
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

LOCKED = {'H1', 'H2', 'H3', 'H4', 'U2', 'J1', 'J2', 'J3', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'J7', 'J8', 'J9', 'J10'}

from optimize_zero_drc import P

# Ensure locked items have proven coordinates:
for h, (hx, hy) in HOLES.items():
    P[h] = (hx, hy, 0, 'F.Cu')

P['J1'] = (88.5, 71.0, 0, 'F.Cu')
P['J2'] = (100.0, 70.5, 0, 'F.Cu')
P['J3'] = (111.5, 71.0, 0, 'F.Cu')

P['Q1'] = (82.0, 77.5, 0, 'F.Cu')
P['Q2'] = (89.2, 77.5, 0, 'F.Cu')
P['Q3'] = (96.4, 77.5, 0, 'F.Cu')
P['Q4'] = (103.6, 77.5, 0, 'F.Cu')
P['Q5'] = (110.8, 77.5, 0, 'F.Cu')
P['Q6'] = (118.0, 77.5, 0, 'F.Cu')

# South connectors flush along Y = 120.0
P['J8']  = (74.0,   110.69, 0, 'F.Cu')
P['J7']  = (92.25,  115.82, 0, 'F.Cu')
P['J10'] = (100.25, 110.69, 0, 'F.Cu')
P['J9']  = (121.0,  110.69, 0, 'F.Cu')

P['U2']  = (100.0, 100.0, 0, 'B.Cu')

# Adjust bulk caps slightly to (72.0, 83.5) and (128.0, 83.5)
P['C_BULK1'] = (72.0, 83.5, 0, 'F.Cu')
P['C63']     = (128.0, 83.5, 180, 'F.Cu')

# Shunts at Y = 82.5, rot = 0
P['R47'] = (91.5, 82.5, 0, 'F.Cu')
P['R48'] = (100.0, 82.5, 0, 'F.Cu')
P['R49'] = (108.5, 82.5, 0, 'F.Cu')

P['NT1'] = (89.5, 82.5, 0, 'F.Cu')
P['NT2'] = (93.5, 82.5, 0, 'F.Cu')
P['NT3'] = (98.0, 82.5, 0, 'F.Cu')
P['NT4'] = (102.0, 82.5, 0, 'F.Cu')
P['NT5'] = (106.5, 82.5, 0, 'F.Cu')
P['NT6'] = (110.5, 82.5, 0, 'F.Cu')

P['IC1'] = (100.0, 89.0, 0, 'F.Cu')
P['U1']  = (100.0, 102.0, 0, 'F.Cu')

# Now let's fix known overlaps manually before running the optimizer:
# 1. Gate resistors:
P['R1'] = (82.0, 73.8, 0, 'F.Cu')
P['R2'] = (88.5, 73.8, 0, 'F.Cu')
P['R3'] = (95.0, 73.8, 0, 'F.Cu')
P['R4'] = (105.0, 73.8, 0, 'F.Cu')
P['R5'] = (111.5, 73.8, 0, 'F.Cu')
P['R7'] = (118.0, 73.8, 0, 'F.Cu')

# 2. C_BUS caps:
P['C_BUS1'] = (94.25, 70.8, 0, 'F.Cu')
P['C_BUS2'] = (105.75, 70.8, 0, 'F.Cu')
P['C_BUS3'] = (100.0, 66.2, 0, 'F.Cu')

# 3. Status LEDs (West Wing below bulk cap):
P['D1']  = (76.0, 88.5, 0, 'F.Cu')
P['R33'] = (79.0, 88.5, 0, 'F.Cu')
P['D2']  = (76.0, 91.0, 0, 'F.Cu')
P['R35'] = (79.0, 91.0, 0, 'F.Cu')
P['D3']  = (76.0, 93.5, 0, 'F.Cu')
P['R36'] = (79.0, 93.5, 0, 'F.Cu')

# 4. CAN subsystem:
P['U9']  = (76.0, 98.0, 0, 'F.Cu')
P['JP1'] = (76.0, 101.5, 0, 'F.Cu')
P['R45'] = (76.0, 104.0, 0, 'F.Cu')
P['R46'] = (76.0, 106.0, 0, 'F.Cu')
P['C60'] = (72.0, 96.0, 90, 'F.Cu')
P['C61'] = (72.0, 98.8, 90, 'F.Cu')
P['C62'] = (72.0, 101.6, 90, 'F.Cu')

# 5. Crystal & MCU West passives:
P['FB1'] = (88.5, 96.5, 0, 'F.Cu')
P['Y1']  = (86.0, 100.0, 0, 'F.Cu')
P['C8']  = (82.5, 98.5, 90, 'F.Cu')
P['C9']  = (82.5, 101.5, 90, 'F.Cu')
P['R44'] = (85.5, 103.5, 0, 'F.Cu')
P['R32'] = (88.5, 103.5, 0, 'F.Cu')
P['R34'] = (88.5, 105.8, 0, 'F.Cu')

# 6. MCU decoupling caps:
P['C51'] = (91.5, 99.0, 90, 'F.Cu')
P['C52'] = (91.5, 101.8, 90, 'F.Cu')
P['C53'] = (91.5, 104.6, 90, 'F.Cu')

P['C6']  = (108.5, 99.0, 90, 'F.Cu')
P['C7']  = (108.5, 101.8, 90, 'F.Cu')
P['C50'] = (108.5, 104.6, 90, 'F.Cu')

P['C4']  = (95.0, 93.8, 0, 'F.Cu')
P['C5']  = (105.0, 93.8, 0, 'F.Cu')
P['C10'] = (90.0, 107.5, 0, 'F.Cu')
P['C11'] = (110.0, 107.5, 0, 'F.Cu')

# 7. DRV caps:
P['C1']  = (94.0, 85.5, 0, 'F.Cu')
P['C2']  = (94.0, 87.2, 0, 'F.Cu')
P['C3']  = (94.0, 88.9, 0, 'F.Cu')
P['C12'] = (93.5, 90.7, 0, 'F.Cu')
P['C13'] = (93.5, 92.4, 0, 'F.Cu')

P['C15'] = (106.0, 85.5, 0, 'F.Cu')
P['C18'] = (106.0, 87.2, 0, 'F.Cu')
P['C19'] = (106.0, 88.9, 0, 'F.Cu')
P['C20'] = (106.5, 90.7, 0, 'F.Cu')
P['C21'] = (106.5, 92.4, 0, 'F.Cu')
P['C64'] = (106.5, 95.5, 0, 'F.Cu')

# DRV resistors:
P['R6']  = (90.8, 85.5, 0, 'F.Cu')
P['R8']  = (90.8, 87.2, 0, 'F.Cu')
P['R9']  = (90.8, 88.9, 0, 'F.Cu')
P['R10'] = (90.8, 90.7, 0, 'F.Cu')
P['R50'] = (90.8, 92.4, 0, 'F.Cu')
P['R51'] = (87.5, 88.9, 0, 'F.Cu')
P['R52'] = (87.5, 91.0, 0, 'F.Cu')

P['R55'] = (109.2, 85.5, 0, 'F.Cu')
P['R56'] = (109.2, 87.2, 0, 'F.Cu')
P['R57'] = (109.2, 88.9, 0, 'F.Cu')
P['R58'] = (109.2, 90.7, 0, 'F.Cu')
P['R59'] = (109.2, 92.4, 0, 'F.Cu')
P['R60'] = (109.2, 94.4, 0, 'F.Cu')
P['TP1'] = (88.0, 86.8, 0, 'F.Cu')
P['TP2'] = (87.5, 93.0, 0, 'F.Cu')
P['TP3'] = (109.2, 97.0, 0, 'F.Cu')

# Current sense filters:
P['R37'] = (90.5, 95.0, 0, 'F.Cu')
P['C54'] = (93.0, 95.0, 0, 'F.Cu')
P['R38'] = (97.0, 95.0, 0, 'F.Cu')
P['C55'] = (100.0, 95.0, 0, 'F.Cu')
P['R39'] = (103.0, 95.0, 0, 'F.Cu')
P['C56'] = (106.0, 97.0, 0, 'F.Cu')

# 8. East Wing:
# XT30 J11 at (120.0, 97.5, rot=270)
P['J11'] = (120.0, 97.5, 270, 'F.Cu')
# Fuseholder F1: horizontal at (114.0, 92.5, rot=0)
P['F1']  = (114.0, 92.5, 0, 'F.Cu')
# TVS Diode D6: at (121.5, 105.0, rot=90)
P['D6']  = (121.5, 105.0, 90, 'F.Cu')

# Buck converter:
P['L1']  = (122.5, 89.5, 0, 'F.Cu')
P['D4']  = (116.5, 87.0, 0, 'F.Cu')
P['C16'] = (116.5, 84.5, 90, 'F.Cu')
P['C17'] = (119.0, 84.5, 90, 'F.Cu')
P['R53'] = (121.5, 84.5, 0, 'F.Cu')
P['R54'] = (121.5, 86.5, 0, 'F.Cu')

# 3.3V LDO:
P['U10'] = (114.0, 100.0, 0, 'F.Cu')
P['C57'] = (114.0, 103.0, 0, 'F.Cu')
P['C58'] = (114.0, 105.5, 0, 'F.Cu')

# 9. B.Cu USB passives:
P['U8']  = (92.25, 108.0, 0, 'B.Cu')
P['C59'] = (92.25, 111.0, 0, 'B.Cu')
P['Q7']  = (92.25, 113.8, 0, 'B.Cu')
P['R40'] = (87.5, 113.8, 0, 'B.Cu')
P['R41'] = (89.5, 113.8, 0, 'B.Cu')
P['R42'] = (95.0, 113.8, 0, 'B.Cu')
P['R43'] = (97.0, 113.8, 0, 'B.Cu')

# Encoder passives:
P['C14'] = (100.0, 103.5, 0, 'B.Cu')
P['R61'] = (100.0, 96.5, 90, 'B.Cu')

def eval_placement(P_curr):
    bboxes = {}
    for ref, (x, y, rot, layer) in P_curr.items():
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
        if r in ['C_BULK1', 'C63']: continue
        for px in [b['x1'], b['x2']]:
            for py in [b['y1'], b['y2']]:
                if py > y_cut + 0.05:
                    oob.append((r, f"Y={py:.2f} > {y_cut}"))
                d = math.hypot(px - 100.0, py - 100.0)
                if d > 34.95:
                    oob.append((r, f"dist={d:.2f} > 34.95"))

    return overlaps, hole_errs, oob, bboxes

ov, he, oob, _ = eval_placement(P)
print(f"==========================================")
print(f"TOTAL COMPONENTS: {len(P)} / 124")
print(f"OVERLAPS DETECTED: {len(ov)}")
print(f"HOLE COLLISIONS: {len(he)}")
print(f"OUT OF BOUNDS: {len(oob)}")
print(f"==========================================")
for r1, r2, dx, dy in ov:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in he:
    print(f"  HOLE: {h} <--> {r} : pen={pen:.2f}")
for r, msg in oob[:10]:
    print(f"  OOB: {r} : {msg}")
