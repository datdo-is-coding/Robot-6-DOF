import math

def rect_circle_overlap(rx1, ry1, rx2, ry2, cx, cy, r):
    qx = max(rx1, min(cx, rx2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

H2 = (84.444, 115.556, 2.95)
H1 = (115.556, 115.556, 2.95)

y_cut = 124.0
dy = y_cut - 100.0
dx_max = math.sqrt(35.0**2 - dy**2)
x_left_edge = 100.0 - dx_max
x_right_edge = 100.0 + dx_max

for c in ['J8', 'J9', 'J7', 'J10']:
    if c in ['J8', 'J9']:
        y_orig = y_cut - 9.20
        lx1, lx2 = -2.95, 7.95
        ly1, ly2 = y_orig - 2.81, y_orig + 9.70
    elif c == 'J10':
        y_orig = y_cut - 9.20
        lx1, lx2 = -2.95, 12.95
        ly1, ly2 = y_orig - 2.81, y_orig + 9.70
    elif c == 'J7':
        y_orig = y_cut - 3.79
        lx1, lx2 = -5.32, 5.32
        ly1, ly2 = y_orig - 4.85, y_orig + 4.18
        
    x_test = x_left_edge - lx1 + 0.2
    valid = []
    while x_test + lx2 <= x_right_edge - 0.2:
        rx1, rx2 = x_test + lx1, x_test + lx2
        ry1, ry2 = ly1, ly2
        if not rect_circle_overlap(rx1, ry1, rx2, ry2, H2[0], H2[1], H2[2]) and \
           not rect_circle_overlap(rx1, ry1, rx2, ry2, H1[0], H1[1], H1[2]):
            valid.append((x_test, rx1, rx2))
        x_test += 0.5
    print(f"{c}: {len(valid)} valid positions. Valid ranges:")
    # print contiguous ranges
    if valid:
        r_start = valid[0]
        r_prev = valid[0]
        for v in valid[1:]:
            if v[0] - r_prev[0] > 0.6:
                print(f"   pos [{r_start[0]:.2f} .. {r_prev[0]:.2f}], rx [{r_start[1]:.2f} .. {r_prev[2]:.2f}]")
                r_start = v
            r_prev = v
        print(f"   pos [{r_start[0]:.2f} .. {r_prev[0]:.2f}], rx [{r_start[1]:.2f} .. {r_prev[2]:.2f}]")
