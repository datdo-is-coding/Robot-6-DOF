import math, re
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

def get_custom_bbox(ref, is_bottom, shapes, x, y, rot):
    if ref in ['H1', 'H2', 'H3', 'H4']:
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.40, 'x2': x + 2.40, 'y1': y - 2.40, 'y2': y + 2.40, 'cx': x, 'cy': y, 'w': 4.80, 'h': 4.80}
    elif ref == 'J7':
        # GT-USB-7010ASV USB-C
        return {'ref': ref, 'layer': 'top', 'x1': x - 4.80, 'x2': x + 4.80, 'y1': y - 4.85, 'y2': y + 4.18, 'cx': x, 'cy': y - 0.335, 'w': 9.60, 'h': 9.03}
    elif ref in ['J8', 'J9']:
        # JST-XH 3-pin horizontal: at rot=0, pins at y=0, body extends x in [-2.7, 7.7], y in [-2.6, 9.45]
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 7.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 2.5, 'cy': y + 3.425, 'w': 10.40, 'h': 12.05}
    elif ref == 'J10':
        # JST-XH 5-pin horizontal: at rot=0, pins at y=0, body extends x in [-2.7, 12.7], y in [-2.6, 9.45]
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 12.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 5.0, 'cy': y + 3.425, 'w': 15.40, 'h': 12.05}
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

P = {}

# 1. MOUNTING HOLES PCD Ø44 mm
for h, (hx, hy) in HOLES.items():
    P[h] = (hx, hy, 0, 'F.Cu')

# 2. MOTOR TERMINALS (Tier 1: Y = 70.0..70.5, dist <= 33.0 mm < 35.0 mm)
P['J1'] = (85.5, 70.5, 0, 'F.Cu')
P['J2'] = (100.0, 68.0, 0, 'F.Cu')
P['J3'] = (114.5, 70.5, 0, 'F.Cu')

# DC Bus Ceramic Caps (1206: horizontal rot=0: w=3.2, h=1.6)
P['C_BUS1'] = (92.5, 70.5, 0, 'F.Cu')
P['C_BUS2'] = (107.5, 70.5, 0, 'F.Cu')
P['C_BUS3'] = (100.0, 71.5, 0, 'F.Cu')

# 3. GATE RESISTORS (Tier 1.5: Y = 71.8)
P['R1'] = (81.85, 71.8, 0, 'F.Cu')
P['R2'] = (89.10, 71.8, 0, 'F.Cu')
P['R3'] = (96.00, 71.8, 0, 'F.Cu')
P['R4'] = (104.00, 71.8, 0, 'F.Cu')
P['R5'] = (110.90, 71.8, 0, 'F.Cu')
P['R7'] = (118.15, 71.8, 0, 'F.Cu')

# 4. 6 MOSFETS (Tier 2: Y = 76.0)
P['Q1'] = (81.85, 76.0, 0, 'F.Cu')
P['Q2'] = (89.10, 76.0, 0, 'F.Cu')
P['Q3'] = (96.35, 76.0, 0, 'F.Cu')
P['Q4'] = (103.65, 76.0, 0, 'F.Cu')
P['Q5'] = (110.90, 76.0, 0, 'F.Cu')
P['Q6'] = (118.15, 76.0, 0, 'F.Cu')

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

# Bulk Electrolytic Caps (D10mm: center at Y = 86.5)
P['C_BULK1'] = (76.5, 86.5, 180, 'F.Cu')
P['C63']     = (123.5, 86.5, 0, 'F.Cu')

# 6. GATE DRIVER IC1 (Tier 4: Y = 87.5)
P['IC1'] = (100.0, 87.5, 0, 'F.Cu')

# Left flank passives (IC1):
P['C1']  = (94.0, 84.5, 0, 'F.Cu')
P['C2']  = (94.0, 86.2, 0, 'F.Cu')
P['C3']  = (94.0, 87.9, 0, 'F.Cu')
P['C12'] = (94.0, 89.7, 0, 'F.Cu')
P['C13'] = (94.0, 91.5, 0, 'F.Cu')

P['R6']  = (90.5, 84.5, 0, 'F.Cu')
P['R8']  = (90.5, 86.2, 0, 'F.Cu')
P['R9']  = (90.5, 87.9, 0, 'F.Cu')
P['R10'] = (90.5, 89.7, 0, 'F.Cu')
P['R50'] = (90.5, 91.5, 0, 'F.Cu')

P['TP1'] = (87.5, 86.5, 0, 'F.Cu')
P['R51'] = (87.5, 88.5, 0, 'F.Cu')
P['R52'] = (87.5, 90.5, 0, 'F.Cu')
P['TP2'] = (87.5, 92.5, 0, 'F.Cu')

# Right flank passives (IC1):
P['C15'] = (106.0, 84.5, 0, 'F.Cu')
P['C18'] = (106.0, 86.2, 0, 'F.Cu')
P['C19'] = (106.0, 87.9, 0, 'F.Cu')
P['C20'] = (106.0, 89.7, 0, 'F.Cu')
P['C21'] = (106.0, 91.5, 0, 'F.Cu')

P['R55'] = (109.5, 84.5, 0, 'F.Cu')
P['R56'] = (109.5, 86.2, 0, 'F.Cu')
P['R57'] = (109.5, 87.9, 0, 'F.Cu')
P['R58'] = (109.5, 89.7, 0, 'F.Cu')
P['R59'] = (109.5, 91.5, 0, 'F.Cu')
P['R60'] = (109.5, 93.2, 0, 'F.Cu')
P['TP3'] = (109.5, 95.2, 0, 'F.Cu')

# 7. MCU U1 (Tier 5: Y = 101.5)
P['U1'] = (100.0, 101.5, 0, 'F.Cu')

# Top Decoupling caps (Y = 93.5):
P['C4']  = (96.5, 93.5, 0, 'F.Cu')
P['C5']  = (103.5, 93.5, 0, 'F.Cu')

# Current Sense Filters (Y = 95.5):
P['R37'] = (88.5, 95.5, 0, 'F.Cu')
P['C54'] = (91.5, 95.5, 0, 'F.Cu')
P['R38'] = (96.5, 95.2, 0, 'F.Cu')
P['C55'] = (99.0, 95.2, 0, 'F.Cu')
P['R39'] = (101.5, 95.2, 0, 'F.Cu')
P['C56'] = (104.0, 95.2, 0, 'F.Cu')
P['C64'] = (106.5, 95.2, 0, 'F.Cu')

# Left Decoupling caps:
P['C51'] = (92.5, 98.5, 90, 'F.Cu')
P['C52'] = (92.5, 101.5, 90, 'F.Cu')
P['C53'] = (92.5, 104.5, 90, 'F.Cu')

# Right Decoupling caps:
P['C6']  = (107.5, 98.5, 90, 'F.Cu')
P['C7']  = (107.5, 101.5, 90, 'F.Cu')
P['C50'] = (107.5, 104.5, 90, 'F.Cu')

# Bottom Decoupling caps:
P['C10'] = (94.0, 108.5, 0, 'F.Cu')
P['C11'] = (106.0, 108.5, 0, 'F.Cu')

# Crystal & Reset (West of U1):
P['FB1'] = (88.5, 98.5, 0, 'F.Cu')
P['Y1']  = (85.5, 101.5, 0, 'F.Cu')
P['C8']  = (82.5, 100.0, 90, 'F.Cu')
P['C9']  = (82.5, 103.0, 90, 'F.Cu')
P['R44'] = (85.5, 105.0, 0, 'F.Cu')
P['R32'] = (88.5, 105.0, 0, 'F.Cu')
P['R34'] = (88.5, 107.2, 0, 'F.Cu')

# 8. STATUS LEDS & CAN SUBSYSTEM (West Wing):
P['D1']  = (75.5, 106.5, 0, 'F.Cu')
P['R33'] = (79.0, 106.5, 0, 'F.Cu')
P['D2']  = (75.5, 109.0, 0, 'F.Cu')
P['R35'] = (79.0, 109.0, 0, 'F.Cu')
P['D3']  = (75.5, 111.5, 0, 'F.Cu')
P['R36'] = (79.0, 111.5, 0, 'F.Cu')

P['U9']  = (76.0, 95.0, 0, 'F.Cu')
P['JP1'] = (76.0, 98.5, 0, 'F.Cu')
P['R45'] = (76.0, 101.0, 0, 'F.Cu')
P['R46'] = (76.0, 103.5, 0, 'F.Cu')
P['C60'] = (72.0, 96.0, 90, 'F.Cu')
P['C61'] = (72.0, 99.5, 90, 'F.Cu')
P['C62'] = (72.0, 103.0, 90, 'F.Cu')

# 9. POWER INPUT & BUCK CONVERTER (Far East Wing):
P['J11'] = (118.5, 101.5, 270, 'F.Cu')
P['F1']  = (126.5, 103.5, 90, 'F.Cu')
P['D6']  = (124.0, 111.5, 0, 'F.Cu')

# Buck Converter (East of IC1):
P['L1']  = (122.5, 94.0, 0, 'F.Cu')
P['D4']  = (116.5, 94.0, 0, 'F.Cu')
P['C16'] = (113.5, 96.5, 90, 'F.Cu')
P['C17'] = (116.0, 96.5, 90, 'F.Cu')
P['R53'] = (113.5, 99.0, 0, 'F.Cu')
P['R54'] = (116.0, 99.0, 0, 'F.Cu')

# 3.3V LDO:
P['U10'] = (113.5, 102.5, 0, 'F.Cu')
P['C57'] = (113.0, 105.5, 0, 'F.Cu')
P['C58'] = (115.5, 105.5, 0, 'F.Cu')

# 10. SOUTH CONNECTORS (Tier 6: In a neat row inside circle):
# J8 CAN_IN, J7 USB-C, J10 SWD, J9 CAN_OUT
P['J8']  = (74.0,  110.30, 0, 'F.Cu')
P['J7']  = (92.25, 115.82, 0, 'F.Cu')
P['J10'] = (100.25, 110.30, 0, 'F.Cu')
P['J9']  = (121.0, 110.30, 0, 'F.Cu')

# USB Circuit components:
P['U8']  = (86.5, 111.5, 0, 'F.Cu')
P['C59'] = (86.5, 108.5, 0, 'F.Cu')
P['Q7']  = (92.25, 110.5, 0, 'F.Cu')
P['R40'] = (89.5, 112.5, 0, 'F.Cu')
P['R41'] = (95.0, 112.5, 0, 'F.Cu')
P['R42'] = (89.5, 110.5, 0, 'F.Cu')
P['R43'] = (95.0, 110.5, 0, 'F.Cu')

# 11. BOTTOM LAYER COMPONENTS (B.Cu):
P['U2']  = (100.0, 100.0, 0, 'B.Cu')
P['C14'] = (100.0, 103.5, 0, 'B.Cu')
P['R61'] = (100.0, 96.0, 90, 'B.Cu')

print(f"Total placed components: {len(P)} / 124")

# Evaluate overlaps, holes, and out-of-bounds
bboxes = {}
for ref, (x, y, rot, layer) in P.items():
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
            overlaps.append((r1, r2, dx, dy))

hole_errs = []
for hname, (hx, hy) in HOLES.items():
    for r, b in bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx_box = max(b['x1'], min(hx, b['x2']))
        cy_box = max(b['y1'], min(hy, b['y2']))
        dist = math.hypot(cx_box - hx, cy_box - hy)
        if dist < 2.40:
            hole_errs.append((hname, r, 2.40 - dist))

oob_errs = []
for r, b in bboxes.items():
    corners = [
        (b['x1'], b['y1']), (b['x1'], b['y2']),
        (b['x2'], b['y1']), (b['x2'], b['y2'])
    ]
    max_d = max(math.hypot(cx - 100.0, cy - 100.0) for cx, cy in corners)
    if max_d > 34.95:
        oob_errs.append((r, max_d))

print("==========================================")
print(f"OVERLAPS DETECTED: {len(overlaps)}")
print(f"HOLE COLLISIONS:   {len(hole_errs)}")
print(f"OUT OF BOUNDS:     {len(oob_errs)}")
print("==========================================")

for r1, r2, dx, dy in overlaps:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in hole_errs:
    print(f"  HOLE: {h:8s} <--> {r:8s} : pen={pen:.2f}")
for r, d in oob_errs:
    print(f"  OOB: {r:8s} : dist={d:.2f} > 34.95")
