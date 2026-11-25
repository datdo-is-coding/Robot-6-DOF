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

y_cut = 122.0
y_front = y_cut - 0.50

for c, info in fps_info.items():
    y_orig = y_front - info['f_offset']
    ry1 = y_orig + info['ly1']
    ry2 = y_orig + info['ly2']
    valid_x = []
    for step in range(350):
        xo = 65.0 + step * 0.2
        rx1 = xo + info['lx1']
        rx2 = xo + info['lx2']
        if not rect_in_circle(rx1, ry1, rx2, ry2):
            continue
        if rect_circle_col(rx1, ry1, rx2, ry2, H2[0], H2[1], H2[2]):
            continue
        if rect_circle_col(rx1, ry1, rx2, ry2, H1[0], H1[1], H1[2]):
            continue
        valid_x.append(xo)
    print(f"{c:4s}: {len(valid_x)} valid positions. Min={min(valid_x) if valid_x else None}, Max={max(valid_x) if valid_x else None}")
