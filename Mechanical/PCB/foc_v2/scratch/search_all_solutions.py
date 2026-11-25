import math

# Full search for 4 South connectors:
# J7: USB-C
# J8: 3-pin XH
# J9: 3-pin XH
# J10: 5-pin XH

# Circle: center (100, 100), R = 35.0 mm.
# Mounting holes: H2 = (84.444, 115.556), H1 = (115.556, 115.556), r = 2.95 mm.

# Bounding boxes / courtyards relative to footprint origin:
# J7: crtyd [-5.32, 5.32] x [-4.85, 4.18], front face at y = +3.79
# J8: crtyd [-2.95, 7.95] x [-2.81, 9.70], front face at y = +9.20
# J9: crtyd [-2.95, 7.95] x [-2.81, 9.70], front face at y = +9.20
# J10: crtyd [-2.95, 12.95] x [-2.81, 9.70], front face at y = +9.20

# Criteria:
# 1. Front faces aligned along y_front (within 0.5 mm of each other):
#    For J8, J9, J10: y_orig = y_front - 9.20
#    For J7: y_orig = y_front - 3.79
# 2. Entire courtyard inside Circle R = 35.0 centered at (100, 100)
# 3. y_crtyd_max <= y_cut (above flat cut)
# 4. Zero overlap with H1, H2
# 5. Zero overlap between adjacent connectors (gap >= 0.3 mm)

def rect_circle_col(rx1, ry1, rx2, ry2, cx, cy, r):
    qx = max(rx1, min(cx, rx2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

def rect_in_circle(rx1, ry1, rx2, ry2, R=35.0, cx=100.0, cy=100.0):
    for x in [rx1, rx2]:
        for y in [ry1, ry2]:
            if (x - cx)**2 + (y - cy)**2 > R**2:
                return False
    return True

H2 = (84.444, 115.556, 2.95)
H1 = (115.556, 115.556, 2.95)

fps_info = {
    'J7':  {'lx1': -5.32, 'lx2': 5.32,  'ly1': -4.85, 'ly2': 4.18, 'f_offset': 3.79},
    'J8':  {'lx1': -2.95, 'lx2': 7.95,  'ly1': -2.81, 'ly2': 9.70, 'f_offset': 9.20},
    'J9':  {'lx1': -2.95, 'lx2': 7.95,  'ly1': -2.81, 'ly2': 9.70, 'f_offset': 9.20},
    'J10': {'lx1': -2.95, 'lx2': 12.95, 'ly1': -2.81, 'ly2': 9.70, 'f_offset': 9.20},
}

import itertools

solutions = []

# Test y_front from 120.0 to 126.0 with step 0.5 mm
for y_front in [121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0]:
    y_cut = y_front + 0.3 # flat cut just 0.3mm in front of connectors
    
    # Pre-calculate valid x_orig for each connector type:
    valid_x = {}
    for c, info in fps_info.items():
        valid_x[c] = []
        y_orig = y_front - info['f_offset']
        ry1 = y_orig + info['ly1']
        ry2 = y_orig + info['ly2']
        # x_orig from 65.0 to 135.0 with step 0.25 mm
        for step in range(350):
            xo = 65.0 + step * 0.2
            rx1 = xo + info['lx1']
            rx2 = xo + info['lx2']
            if rx1 < 65.0 or rx2 > 135.0:
                continue
            if ry2 > y_cut:
                continue
            # Check inside circle
            if not rect_in_circle(rx1, ry1, rx2, ry2):
                continue
            # Check collision with H1, H2
            if rect_circle_col(rx1, ry1, rx2, ry2, H2[0], H2[1], H2[2]):
                continue
            if rect_circle_col(rx1, ry1, rx2, ry2, H1[0], H1[1], H1[2]):
                continue
            valid_x[c].append((xo, rx1, rx2, y_orig, ry1, ry2))

    # Now test permutations of orders:
    for order in itertools.permutations(['J8', 'J9', 'J7', 'J10']):
        c0, c1, c2, c3 = order
        for p0 in valid_x[c0]:
            for p1 in valid_x[c1]:
                if p1[1] < p0[2] + 0.3:
                    continue
                for p2 in valid_x[c2]:
                    if p2[1] < p1[2] + 0.3:
                        continue
                    for p3 in valid_x[c3]:
                        if p3[1] < p2[2] + 0.3:
                            continue
                        solutions.append({
                            'y_front': y_front,
                            'y_cut': y_cut,
                            'order': order,
                            'placed': {c0: p0, c1: p1, c2: p2, c3: p3}
                        })
                        break
                    if len(solutions) > 0 and solutions[-1]['placed'].get(c2) == p2:
                        break
                if len(solutions) > 0 and solutions[-1]['placed'].get(c1) == p1:
                    break
            if len(solutions) > 0 and solutions[-1]['placed'].get(c0) == p0:
                break

print(f"Total solutions found: {len(solutions)}")
for s in solutions[:10]:
    print(f"\ny_front={s['y_front']:.1f}, y_cut={s['y_cut']:.1f}, order={s['order']}:")
    for c in s['order']:
        p = s['placed'][c]
        print(f"  {c:4s}: at ({p[0]:.2f}, {p[3]:.2f}), crtyd X=[{p[1]:.2f}, {p[2]:.2f}], Y=[{p[4]:.2f}, {p[5]:.2f}]")
