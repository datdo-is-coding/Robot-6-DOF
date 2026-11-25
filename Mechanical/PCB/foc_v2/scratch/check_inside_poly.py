import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)
P['C63'] = (124.5, 76.0, 0, 'F.Cu')
P['L1']  = (123.5, 89.0, 0, 'F.Cu')
P['D4']  = (115.0, 92.5, 0, 'F.Cu')
P['C16'] = (114.5, 96.2, 90, 'F.Cu')
P['C17'] = (114.5, 100.2, 90, 'F.Cu')
P['R53'] = (118.0, 96.2, 0, 'F.Cu')
P['R54'] = (118.0, 98.5, 0, 'F.Cu')
P['J11'] = (122.0, 103.5, 270, 'F.Cu')
P['F1']  = (124.5, 121.5, 90, 'F.Cu')
P['D6']  = (126.5, 127.5, 0, 'F.Cu')

all_bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = s.parse_shapes(s.fps[ref])
    all_bboxes[ref] = s.get_world_bbox(ref, is_b, shapes, x, y, rot)

# Approximate polygon of the board outline
# Sample the arc (from 134.0712, 92.0) over (100, 65) to (65.9288, 92.0)
poly_pts = [
    (69.0, 132.5),
    (131.0, 132.5),
    (135.5, 125.0),
    (135.5, 92.0),
    (134.0712, 92.0)
]

# Arc center (100, 100), R=35.
# Angle at (134.0712, 92.0): atan2(92-100, 134.0712-100) = atan2(-8, 34.0712) = -13.2 deg (or 346.8 deg)
# Midpoint at (100, 65): atan2(65-100, 0) = -90 deg
# End at (65.9288, 92.0): atan2(92-100, -34.0712) = -166.8 deg
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

outside_corners = []
for ref, b in all_bboxes.items():
    corners = [
        (b['x1'], b['y1']),
        (b['x2'], b['y1']),
        (b['x1'], b['y2']),
        (b['x2'], b['y2'])
    ]
    for cx, cy in corners:
        if not point_in_poly(cx, cy, poly_pts):
            outside_corners.append((ref, cx, cy))

print(f"Total corner checks on 124 components: {len(all_bboxes) * 4}")
print(f"Corners outside boundary: {len(outside_corners)}")
for ref, cx, cy in outside_corners[:10]:
    print(f"  {ref:6s} corner at ({cx:.2f}, {cy:.2f})")
