import math
import sys
sys.path.append('scratch')
from verify_exact_boxes import boxes

CX, CY = 100.0, 100.0
R = 35.0

poly = []
# North arc samples:
th_start = math.atan2(89.8634 - CY, 66.5 - CX)
th_end = math.atan2(89.8634 - CY, 133.5 - CX)
for i in range(50):
    th = th_start + (th_end - th_start) * (i / 49)
    poly.append((CX + R * math.cos(th), CY + R * math.sin(th)))

# East flat cut at x = 135.0:
poly.append((135.0, 91.5))
poly.append((135.0, 110.0))

# South-East transition to (122.5, 132.5):
poly.append((130.0, 122.0))
poly.append((122.5, 132.5))

# South flat cut at y = 132.5:
poly.append((82.5, 132.5))

# South-West transition around (70.0, 122.0):
poly.append((70.0, 122.0))
poly.append((66.5, 110.0))

# West flat cut at x = 66.5:
poly.append((66.5, 89.8634))

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

outside_pts = []
for k, b in boxes.items():
    if k in ['C_BULK1', 'C63']:
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            px = b['x'] + 5.0 * math.cos(rad)
            py = b['y'] + 5.0 * math.sin(rad)
            if not point_in_poly(px, py, poly):
                outside_pts.append(f"{k} cylinder point ({px:.2f}, {py:.2f}) outside")
        continue
    for px, py in [(b['x1'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y1']), (b['x2'], b['y2'])]:
        if not point_in_poly(px, py, poly):
            outside_pts.append(f"{k} point ({px:.2f}, {py:.2f}) outside")

print(f"Total points outside exact Edge.Cuts loop: {len(outside_pts)}")
for p in outside_pts:
    print(" ", p)
