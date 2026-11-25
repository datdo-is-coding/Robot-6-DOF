import math

def rect_circle_overlap(rx1, ry1, rx2, ry2, cx, cy, r):
    qx = max(rx1, min(cx, ry2)) # wait, bug in my previous test! qy = max(ry1, min(cy, ry2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

H2 = (84.444, 115.556, 2.95)
H1 = (115.556, 115.556, 2.95)

for y_cut in [126.0, 127.0, 127.5, 128.0, 128.5, 129.0]:
    dy = y_cut - 100.0
    dx_max = math.sqrt(35.0**2 - dy**2)
    x_left_edge = 100.0 - dx_max
    x_right_edge = 100.0 + dx_max
    
    print(f"\n=== Y_cut = {y_cut:.1f}: X in [{x_left_edge:.2f}, {x_right_edge:.2f}], width={2*dx_max:.2f} ===")
    
    for c in ['J8', 'J10', 'J7']:
        if c == 'J8':
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
            
        x_test = x_left_edge - lx1 + 0.1
        valid = []
        while x_test + lx2 <= x_right_edge - 0.1:
            rx1, rx2 = x_test + lx1, x_test + lx2
            ry1, ry2 = ly1, ly2
            # Proper rect-circle overlap
            qx = max(rx1, min(H2[0], rx2))
            qy = max(ry1, min(H2[1], ry2))
            d2 = math.hypot(H2[0] - qx, H2[1] - qy)
            
            qx1 = max(rx1, min(H1[0], rx2))
            qy1 = max(ry1, min(H1[1], ry2))
            d1 = math.hypot(H1[0] - qx1, H1[1] - qy1)
            
            if d2 >= H2[2] and d1 >= H1[2]:
                valid.append((x_test, rx1, rx2))
            x_test += 0.25
            
        if valid:
            print(f"  {c:4s}: valid range rx [{valid[0][1]:.2f} .. {valid[-1][2]:.2f}] (span: {valid[-1][2] - valid[0][1]:.2f})")
        else:
            print(f"  {c:4s}: NO valid positions!")
