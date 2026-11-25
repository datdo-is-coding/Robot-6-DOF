import math, sys
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

P = {}

# 1. MOUNTING HOLES (PCD Ø44.0 mm)
delta_h = 22.0 / math.sqrt(2)
HOLES = {
    "H3": (100.0 - delta_h, 100.0 - delta_h),
    "H4": (100.0 + delta_h, 100.0 - delta_h),
    "H2": (100.0 - delta_h, 100.0 + delta_h),
    "H1": (100.0 + delta_h, 100.0 + delta_h)
}
for h, (hx, hy) in HOLES.items():
    P[h] = (hx, hy, 0, 'F.Cu')

# 2. MOTOR TERMINALS (Tier 1: Y = 69.5)
P['J1'] = (89.5, 69.5, 0, 'F.Cu')
P['J2'] = (100.0, 69.5, 0, 'F.Cu')
P['J3'] = (110.5, 69.5, 0, 'F.Cu')

# DC Bus Ceramic Caps (1206)
P['C_BUS1'] = (94.0, 69.5, 0, 'F.Cu')
P['C_BUS2'] = (106.0, 69.5, 0, 'F.Cu')
P['C_BUS3'] = (100.0, 66.2, 0, 'F.Cu')

# 3. GATE RESISTORS (Tier 1.5: Y = 73.0)
P['R1'] = (81.85, 73.0, 0, 'F.Cu')
P['R2'] = (89.10, 73.0, 0, 'F.Cu')
P['R3'] = (96.35, 73.0, 0, 'F.Cu')
P['R4'] = (103.65, 73.0, 0, 'F.Cu')
P['R5'] = (110.90, 73.0, 0, 'F.Cu')
P['R7'] = (118.15, 73.0, 0, 'F.Cu')

# 4. 6 MOSFETS (Tier 2: Y = 77.0)
P['Q1'] = (81.85, 77.0, 0, 'F.Cu')
P['Q2'] = (89.10, 77.0, 0, 'F.Cu')
P['Q3'] = (96.35, 77.0, 0, 'F.Cu')
P['Q4'] = (103.65, 77.0, 0, 'F.Cu')
P['Q5'] = (110.90, 77.0, 0, 'F.Cu')
P['Q6'] = (118.15, 77.0, 0, 'F.Cu')

# 5. SHUNTS (Tier 3: Y = 82.0)
P['R47'] = (91.5, 82.0, 0, 'F.Cu')
P['R48'] = (100.0, 82.0, 0, 'F.Cu')
P['R49'] = (108.5, 82.0, 0, 'F.Cu')

P['NT1'] = (89.5, 82.0, 0, 'F.Cu')
P['NT2'] = (93.5, 82.0, 0, 'F.Cu')
P['NT3'] = (98.0, 82.0, 0, 'F.Cu')
P['NT4'] = (102.0, 82.0, 0, 'F.Cu')
P['NT5'] = (106.5, 82.0, 0, 'F.Cu')
P['NT6'] = (110.5, 82.0, 0, 'F.Cu')

# Bulk Electrolytic Caps (D10mm: can center at Y = 86.0)
P['C_BULK1'] = (76.5, 86.0, 180, 'F.Cu')
P['C63']     = (123.5, 86.0, 0, 'F.Cu')

# 6. GATE DRIVER IC1 (Tier 4: Y = 87.5)
P['IC1'] = (100.0, 87.5, 0, 'F.Cu')

# Passives on Left Flank of IC1:
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

P['TP1'] = (87.5, 87.0, 0, 'F.Cu')
P['R51'] = (87.5, 89.5, 0, 'F.Cu')
P['R52'] = (87.5, 91.5, 0, 'F.Cu')
P['TP2'] = (87.5, 93.5, 0, 'F.Cu')

# Passives on Right Flank of IC1:
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

# 7. MCU U1 (Tier 5: Y = 101.0)
P['U1'] = (100.0, 101.0, 0, 'F.Cu')

# MCU Top Decoupling caps (in corridor Y = 93.0):
P['C4']  = (96.5, 93.0, 0, 'F.Cu')
P['C5']  = (103.5, 93.0, 0, 'F.Cu')

# Current Sense Filters (Y = 93.0..94.0):
P['R37'] = (88.5, 94.5, 0, 'F.Cu')
P['C54'] = (91.5, 94.5, 0, 'F.Cu')
P['R38'] = (97.0, 94.5, 0, 'F.Cu')
P['C55'] = (100.0, 94.5, 0, 'F.Cu')
P['R39'] = (103.0, 94.5, 0, 'F.Cu')
P['C56'] = (106.0, 94.5, 0, 'F.Cu')
P['C64'] = (107.5, 93.0, 0, 'F.Cu')

# MCU Left/Right Decoupling caps:
P['C51'] = (92.5, 98.0, 90, 'F.Cu')
P['C52'] = (92.5, 101.0, 90, 'F.Cu')
P['C53'] = (92.5, 104.0, 90, 'F.Cu')

P['C6']  = (107.5, 98.5, 90, 'F.Cu')
P['C7']  = (107.5, 101.5, 90, 'F.Cu')
P['C50'] = (107.5, 104.5, 90, 'F.Cu')

# MCU Bottom Decoupling caps:
P['C10'] = (94.0, 107.5, 0, 'F.Cu')
P['C11'] = (106.0, 107.5, 0, 'F.Cu')

# MCU Crystal & Reset:
P['FB1'] = (88.5, 97.0, 0, 'F.Cu')
P['Y1']  = (85.5, 100.0, 0, 'F.Cu')
P['C8']  = (82.5, 98.5, 90, 'F.Cu')
P['C9']  = (82.5, 101.5, 90, 'F.Cu')
P['R44'] = (85.5, 103.5, 0, 'F.Cu')
P['R32'] = (88.5, 103.5, 0, 'F.Cu')
P['R34'] = (88.5, 106.0, 0, 'F.Cu')

# 8. STATUS LEDS & CAN SUBSYSTEM (Far West Wing):
P['D1']  = (75.0, 89.0, 0, 'F.Cu')
P['R33'] = (79.0, 89.0, 0, 'F.Cu')
P['D2']  = (75.0, 91.5, 0, 'F.Cu')
P['R35'] = (79.0, 91.5, 0, 'F.Cu')
P['D3']  = (75.0, 94.0, 0, 'F.Cu')
P['R36'] = (79.0, 94.0, 0, 'F.Cu')

P['U9']  = (76.0, 98.0, 0, 'F.Cu')
P['JP1'] = (76.0, 101.5, 0, 'F.Cu')
P['R45'] = (76.0, 104.0, 0, 'F.Cu')
P['R46'] = (76.0, 106.0, 0, 'F.Cu')
P['C60'] = (72.0, 95.5, 90, 'F.Cu')
P['C61'] = (72.0, 99.0, 90, 'F.Cu')
P['C62'] = (72.0, 102.5, 90, 'F.Cu')

# 9. POWER INPUT & BUCK CONVERTER (Far East Wing):
# XT30 J11 (rot=270, outer East):
P['J11'] = (117.0, 101.0, 270, 'F.Cu')
# TVS Diode D6:
P['D6']  = (124.0, 105.0, 0, 'F.Cu')
# Fuse F1 (rot=90, vertical between MCU and J11):
P['F1']  = (123.5, 114.0, 90, 'F.Cu')

# Buck Converter:
P['L1']  = (123.0, 93.0, 0, 'F.Cu')
P['D4']  = (117.0, 89.0, 0, 'F.Cu')
P['C16'] = (115.5, 91.5, 90, 'F.Cu')
P['C17'] = (118.0, 91.5, 90, 'F.Cu')
P['R53'] = (122.0, 86.5, 0, 'F.Cu')
P['R54'] = (122.0, 88.5, 0, 'F.Cu')

# 3.3V LDO:
P['U10'] = (113.0, 96.5, 0, 'F.Cu')
P['C57'] = (113.0, 99.5, 0, 'F.Cu')
P['C58'] = (116.0, 99.5, 0, 'F.Cu')

# 10. SOUTH CONNECTORS (Tier 6: Flush along flat cut Y = 120.00):
P['J8']  = (74.0,  110.30, 0, 'F.Cu')
P['J7']  = (92.25, 115.82, 0, 'F.Cu')
P['J10'] = (100.25, 110.30, 0, 'F.Cu')
P['J9']  = (121.0, 110.30, 0, 'F.Cu')

# 11. BOTTOM LAYER COMPONENTS (B.Cu):
P['U2']  = (100.0, 100.0, 0, 'B.Cu')
P['C14'] = (100.0, 103.5, 0, 'B.Cu')
P['R61'] = (100.0, 96.0, 90, 'B.Cu')

# USB Circuit on B.Cu:
P['U8']  = (92.25, 107.5, 0, 'B.Cu')
P['C59'] = (92.25, 110.5, 0, 'B.Cu')
P['Q7']  = (92.25, 113.5, 0, 'B.Cu')
P['R40'] = (86.0,  118.0, 0, 'B.Cu')
P['R41'] = (89.5,  118.0, 0, 'B.Cu')
P['R42'] = (95.0,  118.0, 0, 'B.Cu')
P['R43'] = (98.5,  118.0, 0, 'B.Cu')

ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

def get_custom_bbox(ref, is_bottom, shapes, x, y, rot):
    if ref in ['H1', 'H2', 'H3', 'H4']:
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.40, 'x2': x + 2.40, 'y1': y - 2.40, 'y2': y + 2.40, 'cx': x, 'cy': y, 'w': 4.80, 'h': 4.80}
    elif ref == 'J7':
        return {'ref': ref, 'layer': 'top', 'x1': x - 4.70, 'x2': x + 4.70, 'y1': y - 4.85, 'y2': y + 4.18, 'cx': x, 'cy': y - 0.335, 'w': 9.40, 'h': 9.03}
    elif ref in ['J8', 'J9']:
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 7.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 2.5, 'cy': y + 3.425, 'w': 10.40, 'h': 12.05}
    elif ref == 'J10':
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 12.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 5.0, 'cy': y + 3.425, 'w': 15.40, 'h': 12.05}
    else:
        return get_world_bbox(ref, is_bottom, shapes, x, y, rot)

def eval_zero(P_curr):
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
                overlaps.append((r1, r2, dx, dy))

    hole_errs = []
    for hname, (hx, hy) in HOLES.items():
        for r, b in bboxes.items():
            if r in ['H1', 'H2', 'H3', 'H4']: continue
            cx_box = max(b['x1'], min(hx, b['x2']))
            cy_box = max(b['y1'], min(hy, b['y2']))
            d = math.hypot(cx_box - hx, cy_box - hy)
            if d < 2.40:
                hole_errs.append((hname, r, 2.40 - d))

    oob = []
    for r, b in bboxes.items():
        if r in ['C_BULK1', 'C63']: continue
        for px in [b['x1'], b['x2']]:
            for py in [b['y1'], b['y2']]:
                if py > 120.05:
                    oob.append((r, f"Y={py:.2f} > 120.0"))
                d = math.hypot(px - 100.0, py - 100.0)
                if d > 34.95:
                    oob.append((r, f"dist={d:.2f} > 34.95"))

    return overlaps, hole_errs, oob, bboxes

ov, he, oob, _ = eval_zero(P)
print(f"==========================================")
print(f"TOTAL COMPONENTS: {len(P)} / 124")
print(f"OVERLAPS DETECTED: {len(ov)}")
print(f"HOLE COLLISIONS: {len(he)}")
print(f"OUT OF BOUNDS: {len(oob)}")
print(f"==========================================")
for r1, r2, dx, dy in ov:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in he:
    print(f"  HOLE: {h:8s} <--> {r:8s} : pen={pen:.2f}")
for r, msg in oob[:10]:
    print(f"  OOB: {r:8s} : {msg}")
