import math

def point_inside_board(x, y, y_cut):
    if y > y_cut:
        return False
    return (x - 100.0)**2 + (y - 100.0)**2 <= 35.0**2

y_cut = 124.0
y_orig = y_cut - 9.70
y1 = y_orig - 2.81
y2 = y_cut
for x_orig in [73.0, 74.0, 75.0]:
    x1 = x_orig - 2.95
    x2 = x_orig + 7.95
    print(f"x_orig={x_orig}: x1={x1:.2f}, x2={x2:.2f}, y1={y1:.2f}, y2={y2:.2f}")
    for px, py, name in [(x1, y1, 'TL'), (x2, y1, 'TR'), (x1, y2, 'BL'), (x2, y2, 'BR')]:
        r = math.hypot(px - 100, py - 100)
        print(f"  {name}: ({px:.2f}, {py:.2f}) -> r={r:.2f} <= 35? {r <= 35.0}")
