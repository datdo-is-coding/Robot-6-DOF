import math

H2 = (84.44365, 115.55635)
H1 = (115.55635, 115.55635)
R_KO = 3.0

def box_collides_with_hole(xmin, xmax, ymin, ymax, hx, hy, r_ko=3.0):
    closest_x = max(xmin, min(hx, xmax))
    closest_y = max(ymin, min(hy, ymax))
    d = math.hypot(closest_x - hx, closest_y - hy)
    return d < r_ko

for y_front_int in range(120, 135):
    y_front = float(y_front_int)
    y_pin = y_front - 9.70
    ymin_xh = y_front - 12.51
    ymax_xh = y_front
    
    blocked_h2 = []
    blocked_h1 = []
    for x_step in range(650, 1350):
        x = x_step / 10.0
        if box_collides_with_hole(x, x+0.1, ymin_xh, ymax_xh, H2[0], H2[1]):
            blocked_h2.append(x)
        if box_collides_with_hole(x, x+0.1, ymin_xh, ymax_xh, H1[0], H1[1]):
            blocked_h1.append(x)
            
    h2_str = f"[{min(blocked_h2):.1f}, {max(blocked_h2):.1f}]" if blocked_h2 else "None"
    h1_str = f"[{min(blocked_h1):.1f}, {max(blocked_h1):.1f}]" if blocked_h1 else "None"
    
    dy = y_front - 100.0
    cw = 2 * math.sqrt(35.0**2 - dy**2) if dy < 35.0 else 0
    print(f"Y_front={y_front:5.1f} | Y_pin={y_pin:5.2f} | H2 blocked: {h2_str:14s} | H1 blocked: {h1_str:14s} | Width at front: {cw:5.1f}")
