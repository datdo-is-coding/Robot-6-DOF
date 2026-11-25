import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)
P['J8']  = (74.5, 122.5, 0, 'F.Cu')
P['J9']  = (86.0, 122.5, 0, 'F.Cu')
P['J7']  = (100.0, 128.0, 0, 'F.Cu')
P['J10'] = (109.5, 122.5, 0, 'F.Cu')

P['J1'] = (88.0, 69.5, 0, 'F.Cu')
P['J2'] = (100.0, 69.0, 0, 'F.Cu')
P['J3'] = (112.0, 69.5, 0, 'F.Cu')

P['C_BUS1'] = (82.5, 70.0, 0, 'F.Cu')
P['C_BUS2'] = (94.0, 70.0, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 70.0, 0, 'F.Cu')

P['Q1'] = (83.5, 75.8, 90, 'F.Cu')
P['Q2'] = (90.1, 75.8, 270, 'F.Cu')
P['Q3'] = (96.7, 75.8, 90, 'F.Cu')
P['Q4'] = (103.3, 75.8, 270, 'F.Cu')
P['Q5'] = (109.9, 75.8, 90, 'F.Cu')
P['Q6'] = (116.5, 75.8, 270, 'F.Cu')

P['R1'] = (83.5, 80.6, 0, 'F.Cu')
P['R2'] = (90.1, 80.6, 0, 'F.Cu')
P['R3'] = (96.7, 80.6, 0, 'F.Cu')
P['R4'] = (103.3, 80.6, 0, 'F.Cu')
P['R5'] = (109.9, 80.6, 0, 'F.Cu')
P['R7'] = (116.5, 80.6, 0, 'F.Cu')

P['C_BULK1'] = (77.0, 85.0, 180, 'F.Cu')
P['C63']     = (123.0, 85.0, 0, 'F.Cu')

P['R47'] = (93.0, 85.3, 90, 'F.Cu')
P['R48'] = (100.0, 85.3, 90, 'F.Cu')
P['R49'] = (107.0, 85.3, 90, 'F.Cu')

P['NT1'] = (92.5, 85.3, 90, 'F.Cu')
P['NT2'] = (93.5, 85.3, 90, 'F.Cu')
P['NT3'] = (99.5, 85.3, 90, 'F.Cu')
P['NT4'] = (100.5, 85.3, 90, 'F.Cu')
P['NT5'] = (106.5, 85.3, 90, 'F.Cu')
P['NT6'] = (107.5, 85.3, 90, 'F.Cu')

P['IC1'] = (100.0, 93.5, 0, 'F.Cu')

P['J11'] = (122.0, 103.5, 270, 'F.Cu')
P['F1']  = (124.5, 121.5, 90, 'F.Cu')
P['D6']  = (126.5, 127.5, 0, 'F.Cu')

# Precompute static boxes (all components except L1, D4, C16, C17, R53, R54, R55..R60, TP3)
dyn_refs = ['L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'R55', 'R56', 'R57', 'R58', 'R59', 'R60', 'TP3']
static_boxes = {}
for ref, (x, y, rot, layer) in P.items():
    if ref in dyn_refs: continue
    is_b = (layer == 'B.Cu')
    _, shapes = s.parse_shapes(s.fps[ref])
    box = s.get_world_bbox(ref, is_b, shapes, x, y, rot)
    static_boxes[ref] = box

def check_box_overlap(b1, b2):
    return (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01)

def check_hole(b):
    for hname, (hx, hy) in s.HOLES.items():
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        if math.hypot(cx - hx, cy - hy) < s.R_KO:
            return True
    return False

# Let's test a clean structured arrangement of dyn_refs:
# Column 1 (x = 108.5): R55..R60 vertically spaced by 1.7 mm
# Column 2 (x = 113.5): L1, D4
# Column 3 (x = 118.0): C16, C17, R53, R54
test_dyn = {}

# R55..R60 at x = 108.0
for idx, rname in enumerate(['R55', 'R56', 'R57', 'R58', 'R59', 'R60']):
    test_dyn[rname] = (108.0, 89.5 + idx * 1.8, 0, 'F.Cu')

test_dyn['TP3'] = (108.0, 101.5, 0, 'F.Cu')

# L1 at (114.0, 91.5)
test_dyn['L1'] = (114.0, 91.5, 0, 'F.Cu')

# D4 at (114.0, 97.5, 0)
test_dyn['D4'] = (114.0, 97.5, 0, 'F.Cu')

# C16, C17 at (118.5, 92.5) and (118.5, 95.5)
test_dyn['C16'] = (118.0, 92.5, 90, 'F.Cu')
test_dyn['C17'] = (118.0, 95.5, 90, 'F.Cu')
test_dyn['R53'] = (118.0, 98.0, 0, 'F.Cu')
test_dyn['R54'] = (118.0, 100.0, 0, 'F.Cu')

# Check dyn boxes against static and each other
dyn_boxes = {}
for ref, (x, y, rot, layer) in test_dyn.items():
    _, shapes = s.parse_shapes(s.fps[ref])
    dyn_boxes[ref] = s.get_world_bbox(ref, False, shapes, x, y, rot)

overlaps = []
holes = []
for ref, b in dyn_boxes.items():
    if check_hole(b):
        holes.append(('HOLE', ref))
    for sref, sbox in static_boxes.items():
        if sbox['layer'] == 'top' and check_box_overlap(b, sbox):
            overlaps.append((ref, sref))

drefs = list(dyn_boxes.keys())
for i in range(len(drefs)):
    for j in range(i + 1, len(drefs)):
        r1, r2 = drefs[i], drefs[j]
        if check_box_overlap(dyn_boxes[r1], dyn_boxes[r2]):
            overlaps.append((r1, r2))

print(f"Dyn overlaps: {len(overlaps)}")
for r1, r2 in overlaps: print(" ", r1, "<-->", r2)
print(f"Dyn holes: {len(holes)}")
for h, r in holes: print(" ", h, "<-->", r)
