import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

# Copy P
P = dict(s.P)

def evaluate(P_cand):
    bboxes = {}
    for ref, (x, y, rot, layer) in P_cand.items():
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

    return bboxes, overlaps, hole_errs

# Let's test adjustments:
# 1. L1
P['L1'] = (123.5, 89.0, 0, 'F.Cu')

# 2. D4 (SMA diode)
# Let's try rot = 90 or rot = 0 with adjusted y
P['D4'] = (115.0, 92.5, 0, 'F.Cu')

# 3. C16, C17 (0805 caps)
P['C16'] = (114.5, 96.2, 90, 'F.Cu')
P['C17'] = (114.5, 100.2, 90, 'F.Cu')

# 4. R53, R54 (0603)
P['R53'] = (118.0, 96.2, 0, 'F.Cu')
P['R54'] = (118.0, 98.5, 0, 'F.Cu')

# 5. J11 (XT30)
P['J11'] = (122.0, 103.5, 270, 'F.Cu')

# 6. F1
P['F1'] = (127.0, 111.0, 270, 'F.Cu')

# 7. D6
P['D6'] = (125.0, 126.5, 90, 'F.Cu')

bboxes, overlaps, hole_errs = evaluate(P)
print(f"OVERLAPS: {len(overlaps)}")
for r1, r2, dx, dy in overlaps:
    print(f"  {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
print(f"HOLES: {len(hole_errs)}")
for h, r, d in hole_errs:
    print(f"  {h} <--> {r} : dist={d:.2f}")
