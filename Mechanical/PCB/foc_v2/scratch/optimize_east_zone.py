import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)

# Let's inspect original positions and check what conflicts existed in the original layout
# and solve them cleanly.

def test_config(p_mods):
    P_test = dict(P)
    P_test.update(p_mods)
    
    bboxes = {}
    for ref, (x, y, rot, layer) in P_test.items():
        is_b = (layer == 'B.Cu')
        _, shapes = s.parse_shapes(s.fps[ref])
        box = s.get_world_bbox(ref, is_b, shapes, x, y, rot)
        bboxes[ref] = box

    overlaps = []
    refs = list(bboxes.keys())
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            if (r1, r2) in s.ALLOWED or (r2, r1) in s.ALLOWED:
                continue
            b1, b2 = bboxes[r1], bboxes[r2]
            if b1['layer'] != b2['layer']:
                continue
            if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
                b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
                dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
                dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
                overlaps.append((r1, r2, dx, dy))

    hole_errs = []
    for hname, (hx, hy) in s.HOLES.items():
        for r, b in bboxes.items():
            if r in ['H1', 'H2', 'H3', 'H4']: continue
            cx = max(b['x1'], min(hx, b['x2']))
            cy = max(b['y1'], min(hy, b['y2']))
            d = math.hypot(cx - hx, cy - hy)
            if d < s.R_KO:
                hole_errs.append((hname, r, d))

    return len(overlaps), overlaps, len(hole_errs), hole_errs, bboxes

# Let's write an optimizer / grid search over the East zone components
# The components to optimize are:
# C63, L1, D4, C16, C17, R53, R54, J11, F1, D6, U10, C57, C58, R55..R60, TP3
print("Starting grid search / optimizer...")
