import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
from verify_all_clean import P

P_fix = dict(P)

# 1. C12 shifted left by 0.5 mm
P_fix['C12'] = (93.5, 96.5, 0, 'F.Cu')

# 2. USB passives on B.Cu placed in open zone Y in [116.0, 121.0] (outside J7 courtyard Y >= 123.15)
# J7 B.CrtYd is x in [94.68, 105.32], y in [123.15, 132.18]
# Let's arrange them neatly in a 2x3 grid:
P_fix['U8']  = (97.0, 118.0, 0, 'B.Cu')   # USBLC6-2SC6
P_fix['Q7']  = (103.0, 118.0, 0, 'B.Cu')  # MOSFET
P_fix['C59'] = (100.0, 118.0, 0, 'B.Cu')  # 0603 cap

P_fix['R40'] = (96.5, 120.5, 0, 'B.Cu')   # 0603
P_fix['R41'] = (99.0, 120.5, 0, 'B.Cu')   # 0603
P_fix['R42'] = (101.5, 120.5, 0, 'B.Cu')  # 0603
P_fix['R43'] = (104.0, 120.5, 0, 'B.Cu')  # 0603

# Check overlaps
all_bboxes = {}
for ref, (x, y, rot, layer) in P_fix.items():
    is_b = (layer == 'B.Cu')
    _, shapes = s.parse_shapes(s.fps[ref])
    all_bboxes[ref] = s.get_world_bbox(ref, is_b, shapes, x, y, rot)

# Add J7 on B.Cu as well for courtyard check
_, j7_shapes = s.parse_shapes(s.fps['J7'])
all_bboxes['J7_B'] = s.get_world_bbox('J7', True, j7_shapes, P_fix['J7'][0], P_fix['J7'][1], P_fix['J7'][2])

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

print(f"OVERLAPS DETECTED: {len(overlaps)}")
for r1, r2, dx, dy in overlaps:
    print(f"  OVERLAP: {r1} <--> {r2} : dx={dx:.2f}, dy={dy:.2f}")
