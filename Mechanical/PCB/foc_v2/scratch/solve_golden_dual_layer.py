import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

def get_custom_bbox(ref, is_bottom, shapes, x, y, rot):
    layer_str = 'bottom' if is_bottom else 'top'
    if ref in ['H1', 'H2', 'H3', 'H4']:
        return {'ref': ref, 'layer': layer_str, 'x1': x - 2.40, 'x2': x + 2.40, 'y1': y - 2.40, 'y2': y + 2.40, 'cx': x, 'cy': y, 'w': 4.80, 'h': 4.80}
    elif ref == 'J7':
        return {'ref': ref, 'layer': layer_str, 'x1': x - 4.80, 'x2': x + 4.80, 'y1': y - 4.85, 'y2': y + 4.18, 'cx': x, 'cy': y - 0.335, 'w': 9.60, 'h': 9.03}
    elif ref in ['J8', 'J9']:
        return {'ref': ref, 'layer': layer_str, 'x1': x - 2.70, 'x2': x + 7.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 2.5, 'cy': y + 3.425, 'w': 10.40, 'h': 12.05}
    elif ref == 'J10':
        return {'ref': ref, 'layer': layer_str, 'x1': x - 2.70, 'x2': x + 12.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 5.0, 'cy': y + 3.425, 'w': 15.40, 'h': 12.05}
    elif ref == 'C_BULK1':
        ccx = x - 2.5
        return {'ref': ref, 'layer': layer_str, 'x1': ccx - 5.25, 'x2': ccx + 5.25, 'y1': y - 5.25, 'y2': y + 5.25, 'cx': ccx, 'cy': y, 'w': 10.50, 'h': 10.50, 'is_circle': True, 'cr': 5.25}
    elif ref == 'C63':
        ccx = x + 2.5
        return {'ref': ref, 'layer': layer_str, 'x1': ccx - 5.25, 'x2': ccx + 5.25, 'y1': y - 5.25, 'y2': y + 5.25, 'cx': ccx, 'cy': y, 'w': 10.50, 'h': 10.50, 'is_circle': True, 'cr': 5.25}
    else:
        return get_world_bbox(ref, is_bottom, shapes, x, y, rot)

ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

delta_h = 22.0 / math.sqrt(2) # 15.55635
HOLES = {
    "H3": (100.0 - delta_h, 100.0 - delta_h),
    "H4": (100.0 + delta_h, 100.0 - delta_h),
    "H2": (100.0 - delta_h, 100.0 + delta_h),
    "H1": (100.0 + delta_h, 100.0 + delta_h)
}

def eval_full(P_curr):
    bboxes = {}
    for ref, (x, y, rot, layer) in P_curr.items():
        is_b = (layer == 'B.Cu')
        _, shapes = parse_shapes(fps[ref])
        bboxes[ref] = get_custom_bbox(ref, is_b, shapes, x, y, rot)

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
                overlaps.append((r1, r2, dx, dy, b1['layer']))

    hole_errs = []
    for hname, (hx, hy) in HOLES.items():
        for r, b in bboxes.items():
            if r in ['H1', 'H2', 'H3', 'H4']: continue
            if b.get('is_circle'):
                dist = math.hypot(b['cx'] - hx, b['cy'] - hy)
                if dist < b['cr'] + 2.40:
                    hole_errs.append((hname, r, b['cr'] + 2.40 - dist))
            else:
                cx_box = max(b['x1'], min(hx, b['x2']))
                cy_box = max(b['y1'], min(hy, b['y2']))
                dist = math.hypot(cx_box - hx, cy_box - hy)
                if dist < 2.40:
                    hole_errs.append((hname, r, 2.40 - dist))

    oob_errs = []
    for r, b in bboxes.items():
        if b.get('is_circle'):
            max_d = math.hypot(b['cx'] - 100.0, b['cy'] - 100.0) + b['cr']
        else:
            corners = [
                (b['x1'], b['y1']), (b['x1'], b['y2']),
                (b['x2'], b['y1']), (b['x2'], b['y2'])
            ]
            max_d = max(math.hypot(cx - 100.0, cy - 100.0) for cx, cy in corners)
        if max_d > 34.95:
            oob_errs.append((r, max_d))

    return overlaps, hole_errs, oob_errs

P = {}

# 1. MOUNTING HOLES PCD Ø44 mm
for h, (hx, hy) in HOLES.items():
    P[h] = (hx, hy, 0, 'F.Cu')

# 2. MOTOR TERMINALS (Tier 1: Y = 70.0..70.8)
P['J1'] = (87.0, 70.8, 0, 'F.Cu')
P['J2'] = (100.0, 68.2, 0, 'F.Cu')
P['J3'] = (113.0, 70.8, 0, 'F.Cu')

# DC Bus Ceramic Caps (1206: horizontal rot=0)
P['C_BUS1'] = (93.0, 69.5, 0, 'F.Cu')
P['C_BUS2'] = (107.0, 69.5, 0, 'F.Cu')
P['C_BUS3'] = (100.0, 71.8, 0, 'F.Cu')

# 3. GATE RESISTORS (Tier 1.5: Y = 72.8)
P['R1'] = (82.50, 72.8, 0, 'F.Cu')
P['R2'] = (89.10, 72.8, 0, 'F.Cu')
P['R3'] = (96.00, 72.8, 0, 'F.Cu')
P['R4'] = (104.00, 72.8, 0, 'F.Cu')
P['R5'] = (110.90, 72.8, 0, 'F.Cu')
P['R7'] = (117.50, 72.8, 0, 'F.Cu')

# 4. 6 MOSFETS (Tier 2: Y = 76.5)
P['Q1'] = (81.85, 76.5, 0, 'F.Cu')
P['Q2'] = (89.10, 76.5, 0, 'F.Cu')
P['Q3'] = (96.35, 76.5, 0, 'F.Cu')
P['Q4'] = (103.65, 76.5, 0, 'F.Cu')
P['Q5'] = (110.90, 76.5, 0, 'F.Cu')
P['Q6'] = (118.15, 76.5, 0, 'F.Cu')

# 5. SHUNTS (Tier 3: Y = 81.2)
P['R47'] = (91.5, 81.2, 0, 'F.Cu')
P['R48'] = (100.0, 81.2, 0, 'F.Cu')
P['R49'] = (108.5, 81.2, 0, 'F.Cu')

P['NT1'] = (89.5, 81.2, 0, 'F.Cu')
P['NT2'] = (93.5, 81.2, 0, 'F.Cu')
P['NT3'] = (98.0, 81.2, 0, 'F.Cu')
P['NT4'] = (102.0, 81.2, 0, 'F.Cu')
P['NT5'] = (106.5, 81.2, 0, 'F.Cu')
P['NT6'] = (110.5, 81.2, 0, 'F.Cu')

# Bulk Electrolytic Caps (D10mm):
P['C_BULK1'] = (77.5, 86.5, 180, 'F.Cu')
P['C63']     = (122.5, 86.5, 0, 'F.Cu')

# 6. GATE DRIVER IC1 (Tier 4: Y = 87.5)
P['IC1'] = (100.0, 87.5, 0, 'F.Cu')

# Left flank passives (IC1):
# rot=90 for C1..C13 (w=1.96, h=3.76), X=94.5 (x in [93.52, 95.48])
P['C1']  = (94.5, 84.0, 90, 'F.Cu')
P['C2']  = (94.5, 86.0, 90, 'F.Cu')
P['C3']  = (94.5, 88.0, 90, 'F.Cu')
P['C12'] = (94.5, 90.0, 90, 'F.Cu')
P['C13'] = (94.5, 92.0, 90, 'F.Cu')

P['R6']  = (91.0, 84.0, 0, 'F.Cu')
P['R8']  = (91.0, 86.0, 0, 'F.Cu')
P['R9']  = (91.0, 88.0, 0, 'F.Cu')
P['R10'] = (91.0, 90.0, 0, 'F.Cu')
P['R50'] = (91.0, 92.0, 0, 'F.Cu')

P['TP1'] = (88.5, 84.0, 0, 'F.Cu')
P['R51'] = (88.5, 86.0, 0, 'F.Cu')
P['R52'] = (88.5, 88.0, 0, 'F.Cu')
P['TP2'] = (88.5, 90.0, 0, 'F.Cu')

# Right flank passives (IC1):
# rot=90 for C15..C21, X=105.5
P['C15'] = (105.5, 84.0, 90, 'F.Cu')
P['C18'] = (105.5, 86.0, 90, 'F.Cu')
P['C19'] = (105.5, 88.0, 90, 'F.Cu')
P['C20'] = (105.5, 90.0, 90, 'F.Cu')
P['C21'] = (105.5, 92.0, 90, 'F.Cu')

P['R55'] = (109.0, 84.0, 0, 'F.Cu')
P['R56'] = (109.0, 86.0, 0, 'F.Cu')
P['R57'] = (109.0, 88.0, 0, 'F.Cu')
P['R58'] = (109.0, 90.0, 0, 'F.Cu')
P['R59'] = (109.0, 92.0, 0, 'F.Cu')
P['R60'] = (109.0, 94.0, 0, 'F.Cu')
P['TP3'] = (109.0, 96.0, 0, 'F.Cu')

# 7. MCU U1 (Tier 5: Y = 101.0, x in [93.3, 106.7], y in [94.3, 107.7])
P['U1'] = (100.0, 101.0, 0, 'F.Cu')

# Top Decoupling caps (Y = 93.2):
P['C4']  = (96.5, 93.2, 0, 'F.Cu')
P['C5']  = (103.5, 93.2, 0, 'F.Cu')

# Current Sense Filters (Y = 93.2, X shifted):
P['R37'] = (88.5, 93.2, 0, 'F.Cu')
P['C54'] = (91.5, 93.2, 0, 'F.Cu')
P['R38'] = (94.0, 93.2, 0, 'F.Cu')
P['C55'] = (99.0, 93.2, 0, 'F.Cu')
P['R39'] = (101.0, 93.2, 0, 'F.Cu')
P['C56'] = (106.0, 93.2, 0, 'F.Cu')
P['C64'] = (107.5, 94.8, 0, 'F.Cu')

# Left Decoupling caps:
P['C51'] = (92.5, 98.0, 90, 'F.Cu')
P['C52'] = (92.5, 101.0, 90, 'F.Cu')
P['C53'] = (92.5, 104.0, 90, 'F.Cu')

# Right Decoupling caps:
P['C6']  = (107.5, 98.5, 90, 'F.Cu')
P['C7']  = (107.5, 101.5, 90, 'F.Cu')
P['C50'] = (107.5, 104.5, 90, 'F.Cu')
P['C11'] = (107.5, 106.8, 90, 'F.Cu')

# Bottom Decoupling caps:
P['C10'] = (94.0, 109.0, 0, 'F.Cu')

# Crystal & Reset (West of U1):
P['FB1'] = (88.5, 97.0, 0, 'F.Cu')
P['Y1']  = (85.5, 99.5, 0, 'F.Cu')
P['C8']  = (82.5, 98.0, 90, 'F.Cu')
P['C9']  = (82.5, 101.0, 90, 'F.Cu')
P['R44'] = (85.5, 103.0, 0, 'F.Cu')
P['R32'] = (88.5, 103.0, 0, 'F.Cu')
P['R34'] = (88.5, 105.5, 0, 'F.Cu')

# 8. STATUS LEDS & CAN SUBSYSTEM (West Wing):
P['D1']  = (75.5, 103.5, 0, 'F.Cu')
P['R33'] = (79.0, 103.5, 0, 'F.Cu')
P['D2']  = (75.5, 105.8, 0, 'F.Cu')
P['R35'] = (79.0, 105.8, 0, 'F.Cu')
P['D3']  = (75.5, 108.0, 0, 'F.Cu')
P['R36'] = (79.0, 108.0, 0, 'F.Cu')

P['U9']  = (75.5, 93.0, 0, 'F.Cu')
P['JP1'] = (75.5, 96.5, 0, 'F.Cu')
P['R45'] = (75.5, 99.0, 0, 'F.Cu')
P['R46'] = (75.5, 101.2, 0, 'F.Cu')
P['C60'] = (71.5, 93.0, 90, 'F.Cu')
P['C61'] = (71.5, 96.5, 90, 'F.Cu')
P['C62'] = (71.5, 100.0, 90, 'F.Cu')

# 9. POWER INPUT (XT30 J11 on F.Cu at East):
# XT30 J11 at (115.5, 100.5, rot=270):
P['J11'] = (115.5, 100.5, 270, 'F.Cu')

# 10. SOUTH CONNECTORS (Tier 6: In a neat row inside circle):
# J8 CAN_IN, J7 USB-C, J10 SWD, J9 CAN_OUT
P['J8']  = (74.0,  110.30, 0, 'F.Cu')
P['J7']  = (92.25, 115.82, 0, 'F.Cu')
P['J10'] = (100.25, 110.30, 0, 'F.Cu')
P['J9']  = (121.0, 110.30, 0, 'F.Cu')

# 11. BUCK CONVERTER & 3.3V LDO on F.Cu or B.Cu:
# Let's place Buck and LDO neatly:
P['L1']  = (123.5, 95.0, 0, 'F.Cu')
P['D4']  = (115.0, 91.0, 0, 'F.Cu')
P['C16'] = (112.5, 94.0, 90, 'F.Cu')
P['C17'] = (115.0, 94.0, 90, 'F.Cu')
P['R53'] = (112.5, 96.5, 0, 'F.Cu')
P['R54'] = (115.0, 96.5, 0, 'F.Cu')

P['U10'] = (112.5, 99.5, 0, 'F.Cu')
P['C57'] = (112.0, 102.5, 0, 'F.Cu')
P['C58'] = (114.5, 102.5, 0, 'F.Cu')

# 12. BOTTOM LAYER COMPONENTS (B.Cu):
P['U2']  = (100.0, 100.0, 0, 'B.Cu')
P['C14'] = (100.0, 103.5, 0, 'B.Cu')
P['R61'] = (100.0, 96.0, 90, 'B.Cu')

# Fuse F1 and TVS D6 on B.Cu right under J11:
P['F1']  = (118.0, 104.5, 0, 'B.Cu')
P['D6']  = (125.0, 104.5, 0, 'B.Cu')

# USB Circuit on B.Cu right under J7:
P['U8']  = (92.25, 110.0, 0, 'B.Cu')
P['C59'] = (92.25, 112.5, 0, 'B.Cu')
P['Q7']  = (92.25, 115.0, 0, 'B.Cu')
P['R40'] = (88.5,  118.0, 0, 'B.Cu')
P['R41'] = (96.0,  118.0, 0, 'B.Cu')
P['R42'] = (88.5,  115.5, 0, 'B.Cu')
P['R43'] = (96.0,  115.5, 0, 'B.Cu')

overlaps, hole_errs, oob_errs = eval_full(P)
print(f"Results: Overlaps={len(overlaps)}, Holes={len(hole_errs)}, OOB={len(oob_errs)}")
for r1, r2, dx, dy, layer in overlaps:
    print(f"  OVERLAP ({layer}): {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in hole_errs:
    print(f"  HOLE: {h:8s} <--> {r:8s} : pen={pen:.2f}")
for r, d in oob_errs:
    print(f"  OOB: {r:8s} : dist={d:.2f} > 34.95")
