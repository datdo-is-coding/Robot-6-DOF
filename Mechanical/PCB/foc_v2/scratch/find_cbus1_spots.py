import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
from apply_p_final import P_final
import math

P_test = dict(P_final)
del P_test['C_BUS1']

static_boxes = {}
for ref, (x, y, rot, layer) in P_test.items():
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

# Check if inside R=34.5 (allowing 0.5mm copper edge clearance to 35mm circle)
def inside_board(b):
    corners = [(b['x1'], b['y1']), (b['x2'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y2'])]
    for x, y in corners:
        # if in top half (y < 92)
        if y < 92.0:
            if math.hypot(x - 100.0, y - 100.0) > 34.3:
                return False
        else:
            if x < 65.5 or x > 135.5 or y > 132.0:
                return False
    return True

_, c_bus1_shapes = s.parse_shapes(s.fps['C_BUS1'])

valid_cbus1 = []
for rot in [0, 90]:
    for x_i in range(700, 1100, 2):
        x = x_i / 10.0
        for y_i in range(680, 850, 2):
            y = y_i / 10.0
            box = s.get_world_bbox('C_BUS1', False, c_bus1_shapes, x, y, rot)
            if not inside_board(box): continue
            if check_hole(box): continue
            if any(sbox['layer'] == 'top' and check_box_overlap(box, sbox) for sbox in static_boxes.values()):
                continue
            valid_cbus1.append((x, y, rot))

print(f"Total valid positions for C_BUS1: {len(valid_cbus1)}")
for x, y, rot in valid_cbus1[:10]:
    print(f"  C_BUS1 at ({x:.1f}, {y:.1f}, {rot})")
