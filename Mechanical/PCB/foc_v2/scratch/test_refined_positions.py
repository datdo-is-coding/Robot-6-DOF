import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)

# 1. Motor wire pads lowered slightly so corners are well inside R=35mm circle
P['J1'] = (89.0, 70.5, 0, 'F.Cu')
P['J2'] = (100.0, 70.0, 0, 'F.Cu')
P['J3'] = (111.0, 70.5, 0, 'F.Cu')

# 2. Phase bus caps C_BUS1, C_BUS2, C_BUS3
P['C_BUS1'] = (84.0, 71.0, 0, 'F.Cu')
P['C_BUS2'] = (95.0, 71.0, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 71.0, 0, 'F.Cu')

# 3. Bulk caps: C_BULK1 at (76.0, 82.5) and C63 at (124.0, 82.5)
P['C_BULK1'] = (76.0, 82.5, 0, 'F.Cu')
P['C63']     = (124.0, 82.5, 0, 'F.Cu')

# 4. Buck components
P['L1']  = (114.0, 91.5, 0, 'F.Cu')
P['D4']  = (121.0, 91.5, 0, 'F.Cu')
P['C16'] = (114.5, 96.2, 90, 'F.Cu')
P['C17'] = (114.5, 100.2, 90, 'F.Cu')
P['R53'] = (118.0, 96.2, 0, 'F.Cu')
P['R54'] = (118.0, 98.5, 0, 'F.Cu')

# 5. East power input
P['J11'] = (122.0, 103.5, 270, 'F.Cu')
P['F1']  = (124.5, 121.5, 90, 'F.Cu')
P['D6']  = (126.5, 127.5, 0, 'F.Cu')

# Check overlaps and holes
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
            overlaps.append((r1, r2, b1, b2))

holes = []
for hname, (hx, hy) in s.HOLES.items():
    for r, b in all_bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx - hx, cy - hy)
        if d < s.R_KO:
            holes.append((hname, r, d))

print(f"OVERLAPS: {len(overlaps)}")
for r1, r2, b1, b2 in overlaps:
    print(f"  {r1} <--> {r2}")
print(f"HOLES: {len(holes)}")
for h, r, d in holes:
    print(f"  {h} <--> {r}: dist={d:.2f}")

# Outline polygon:
poly_pts = [
    (69.0, 132.5),
    (131.0, 132.5),
    (136.0, 125.0),
    (136.0, 92.0),
    (134.0712, 92.0)
]
for a_deg in range(-14, -168, -5):
    rad = math.radians(a_deg)
    poly_pts.append((100.0 + 35.0 * math.cos(rad), 100.0 + 35.0 * math.sin(rad)))
poly_pts.extend([
    (65.9288, 92.0),
    (65.5, 92.0),
    (65.5, 125.0)
])

def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

outside = []
for ref, b in all_bboxes.items():
    corners = [(b['x1'], b['y1']), (b['x2'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y2'])]
    for cx, cy in corners:
        if not point_in_poly(cx, cy, poly_pts):
            outside.append((ref, cx, cy))

print(f"OUTSIDE CORNERS: {len(outside)}")
for ref, cx, cy in outside:
    print(f"  {ref:6s} at ({cx:.2f}, {cy:.2f})")
