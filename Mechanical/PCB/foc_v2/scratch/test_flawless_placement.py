import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)

# 1. South Connectors Bank (Y = 132.2)
P['J8']  = (74.5, 122.5, 0, 'F.Cu')  # CAN_IN
P['J9']  = (86.0, 122.5, 0, 'F.Cu')  # CAN_OUT
P['J7']  = (100.0, 128.0, 0, 'F.Cu') # Type-C
P['J10'] = (109.5, 122.5, 0, 'F.Cu') # SWD

# 2. Motor pads: complete circular pads inside board
P['J1'] = (88.0, 69.5, 0, 'F.Cu')
P['J2'] = (100.0, 69.0, 0, 'F.Cu')
P['J3'] = (112.0, 69.5, 0, 'F.Cu')

# 3. Bus caps
P['C_BUS1'] = (82.5, 70.0, 0, 'F.Cu')
P['C_BUS2'] = (94.0, 70.0, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 70.0, 0, 'F.Cu')

# 4. MOSFETs: 6 in a row at Y = 75.8
P['Q1'] = (83.5, 75.8, 90, 'F.Cu')
P['Q2'] = (90.1, 75.8, 270, 'F.Cu')
P['Q3'] = (96.7, 75.8, 90, 'F.Cu')
P['Q4'] = (103.3, 75.8, 270, 'F.Cu')
P['Q5'] = (109.9, 75.8, 90, 'F.Cu')
P['Q6'] = (116.5, 75.8, 270, 'F.Cu')

# 5. Gate Resistors R1..R7
P['R1'] = (83.5, 80.6, 0, 'F.Cu')
P['R2'] = (90.1, 80.6, 0, 'F.Cu')
P['R3'] = (96.7, 80.6, 0, 'F.Cu')
P['R4'] = (103.3, 80.6, 0, 'F.Cu')
P['R5'] = (109.9, 80.6, 0, 'F.Cu')
P['R7'] = (116.5, 80.6, 0, 'F.Cu')

# 6. Bulk Capacitors with outward body rotation:
# C_BULK1 at rot 180 (body extends to -X, clear of R1):
P['C_BULK1'] = (77.0, 85.0, 180, 'F.Cu')
# C63 at rot 0 (body extends to +X, clear of R7):
P['C63']     = (123.0, 85.0, 0, 'F.Cu')

# 7. Shunt Resistors & Net Ties
P['R47'] = (93.0, 85.3, 90, 'F.Cu')
P['R48'] = (100.0, 85.3, 90, 'F.Cu')
P['R49'] = (107.0, 85.3, 90, 'F.Cu')

P['NT1'] = (92.5, 85.3, 90, 'F.Cu')
P['NT2'] = (93.5, 85.3, 90, 'F.Cu')
P['NT3'] = (99.5, 85.3, 90, 'F.Cu')
P['NT4'] = (100.5, 85.3, 90, 'F.Cu')
P['NT5'] = (106.5, 85.3, 90, 'F.Cu')
P['NT6'] = (107.5, 85.3, 90, 'F.Cu')

# Gate bleeder resistors R55..R60 placed near IC1
P['R55'] = (109.5, 90.0, 0, 'F.Cu')
P['R56'] = (109.5, 91.8, 0, 'F.Cu')
P['R57'] = (109.5, 93.6, 0, 'F.Cu')
P['R58'] = (109.5, 95.4, 0, 'F.Cu')
P['R59'] = (109.5, 97.2, 0, 'F.Cu')
P['R60'] = (109.5, 99.0, 0, 'F.Cu')

# 8. Buck Converter & IC1
P['IC1'] = (100.0, 93.5, 0, 'F.Cu')
P['L1']  = (123.5, 93.0, 0, 'F.Cu')
P['D4']  = (115.0, 92.5, 0, 'F.Cu')
P['C16'] = (114.5, 96.2, 90, 'F.Cu')
P['C17'] = (114.5, 100.2, 90, 'F.Cu')
P['R53'] = (118.0, 96.2, 0, 'F.Cu')
P['R54'] = (118.0, 98.5, 0, 'F.Cu')

# 9. East Power Input
P['J11'] = (122.0, 103.5, 270, 'F.Cu')
P['F1']  = (124.5, 121.5, 90, 'F.Cu')
P['D6']  = (126.5, 127.5, 0, 'F.Cu')

# Evaluate
all_bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = s.parse_shapes(s.fps[ref])
    all_bboxes[ref] = s.get_world_bbox(ref, is_b, shapes, x, y, rot)

def check_box_overlap(b1, b2):
    return (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01)

overlaps = []
refs = list(all_bboxes.keys())
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        r1, r2 = refs[i], refs[j]
        if (r1, r2) in s.ALLOWED or (r2, r1) in s.ALLOWED: continue
        b1, b2 = all_bboxes[r1], all_bboxes[r2]
        if b1['layer'] != b2['layer']: continue
        if check_box_overlap(b1, b2):
            dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
            dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
            overlaps.append((r1, r2, dx, dy))

holes = []
for hname, (hx, hy) in s.HOLES.items():
    for r, b in all_bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx - hx, cy - hy)
        if d < s.R_KO:
            holes.append((hname, r, d))

print(f"==========================================")
print(f"TOTAL COMPONENTS: {len(P)} / 124")
print(f"OVERLAPS DETECTED: {len(overlaps)}")
print(f"HOLE COLLISIONS: {len(holes)}")
print(f"==========================================")
for r1, r2, dx, dy in overlaps:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, d in holes:
    print(f"  HOLE: {h:8s} <--> {r:8s} : dist={d:.2f}")
