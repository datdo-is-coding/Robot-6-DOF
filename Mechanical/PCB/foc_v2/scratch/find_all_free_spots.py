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

P['R55'] = (109.5, 90.0, 0, 'F.Cu')
P['R56'] = (109.5, 91.8, 0, 'F.Cu')
P['R57'] = (109.5, 93.6, 0, 'F.Cu')
P['R58'] = (109.5, 95.4, 0, 'F.Cu')
P['R59'] = (109.5, 97.2, 0, 'F.Cu')
P['R60'] = (109.5, 99.0, 0, 'F.Cu')
P['TP3'] = (109.5, 101.5, 0, 'F.Cu')

P['L1'] = (114.5, 92.5, 0, 'F.Cu')
P['D4'] = (114.5, 98.0, 0, 'F.Cu')

# Precompute all static obstacles (120 components)
targets = ['C16', 'C17', 'R53', 'R54']
static_boxes = {}
for ref, (x, y, rot, layer) in P.items():
    if ref in targets: continue
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

_, c16_shapes = s.parse_shapes(s.fps['C16'])
_, c17_shapes = s.parse_shapes(s.fps['C17'])
_, r53_shapes = s.parse_shapes(s.fps['R53'])
_, r54_shapes = s.parse_shapes(s.fps['R54'])

# Let's find all free grid points for a 0805 cap (C16)
free_spots = []
for rot in [0, 90]:
    for x_i in range(1100, 1220, 5):
        x = x_i / 10.0
        for y_i in range(860, 1080, 5):
            y = y_i / 10.0
            box = s.get_world_bbox('C16', False, c16_shapes, x, y, rot)
            if check_hole(box): continue
            if any(sbox['layer'] == 'top' and check_box_overlap(box, sbox) for sbox in static_boxes.values()):
                continue
            free_spots.append((x, y, rot))

print(f"Total free spots found for 0805: {len(free_spots)}")
# Group free spots by region
by_x = {}
for x, y, rot in free_spots:
    by_x.setdefault(x, []).append((y, rot))

for x in sorted(by_x.keys()):
    y_list = [p[0] for p in by_x[x]]
    print(f"  x={x:5.1f}: y in [{min(y_list):.1f}, {max(y_list):.1f}] ({len(y_list)} spots)")
