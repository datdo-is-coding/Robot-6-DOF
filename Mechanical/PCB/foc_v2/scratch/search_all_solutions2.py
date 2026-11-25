import math

fps_info = {
    'J7':  {'lx1': -5.32, 'lx2': 5.32,  'ly1': -4.85, 'ly2': 4.18, 'f_offset': 3.79},
    'J8':  {'lx1': -2.95, 'lx2': 7.95,  'ly1': -2.81, 'ly2': 9.70, 'f_offset': 9.20},
    'J9':  {'lx1': -2.95, 'lx2': 7.95,  'ly1': -2.81, 'ly2': 9.70, 'f_offset': 9.20},
    'J10': {'lx1': -2.95, 'lx2': 12.95, 'ly1': -2.81, 'ly2': 9.70, 'f_offset': 9.20},
}

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

import itertools
solutions = []

# When front face is at y_front, courtyard extends to y_front + 0.50 (for JST-XH) or y_front + 0.39 (for USB).
# So the flat cut should be at y_cut >= y_front + 0.50!
# Let y_cut be in [122.0 .. 126.0]
for y_cut in [122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0]:
    y_front = y_cut - 0.50 # courtyard stays <= y_cut!
    
    valid_x = {}
    for c, info in fps_info.items():
        valid_x[c] = []
        y_orig = y_front - info['f_offset']
        ry1 = y_orig + info['ly1']
        ry2 = y_orig + info['ly2']
        for step in range(350):
            xo = 65.0 + step * 0.2
            rx1 = xo + info['lx1']
            rx2 = xo + info['lx2']
            if rx1 < 65.0 or rx2 > 135.0:
                continue
            if not rect_in_circle(rx1, ry1, rx2, ry2):
                continue
            if rect_circle_col(rx1, ry1, rx2, ry2, H2[0], H2[1], H2[2]):
                continue
            if rect_circle_col(rx1, ry1, rx2, ry2, H1[0], H1[1], H1[2]):
                continue
            valid_x[c].append((xo, rx1, rx2, y_orig, ry1, ry2))

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
        if len(solutions) > 20:
            break
    if len(solutions) > 20:
        break

print(f"Total solutions found: {len(solutions)}")
for s in solutions[:5]:
    print(f"\ny_front={s['y_front']:.2f}, y_cut={s['y_cut']:.2f}, order={s['order']}:")
    for c in s['order']:
        p = s['placed'][c]
        print(f"  {c:4s}: at ({p[0]:.2f}, {p[3]:.2f}), crtyd X=[{p[1]:.2f}, {p[2]:.2f}], Y=[{p[4]:.2f}, {p[5]:.2f}]")
