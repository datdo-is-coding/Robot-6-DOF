import math

# Circle: center = (100.0, 100.0), R = 35.0
# Mounting holes: H2 = (84.44, 115.56), H1 = (115.56, 115.56), radius with clearance = 2.90 mm
# MCU U1: center = (100.0, 100.0), bottom edge = 107.0 mm

# J8: 3-pin XH (width 9.9 mm, depth 11.5 mm: Y in [y-2.7, y+8.8])
# J9: 3-pin XH
# J10: 5-pin XH (width 14.9 mm, depth 11.5 mm: X in [-2.45, 12.45])
# J7: Type-C (width 8.94 mm, depth 7.3 mm: X in [-4.47, 4.47], Y in [-5.5, 1.8])

# Let's test if they can be placed in a row facing South (rot = 0):
# Suppose front face is at Y_front:
# For XH: y_pad = Y_front - 8.8.
# For J7: y_pad = Y_front - 1.8.

def test_row(y_front, xs):
    print(f"\n--- Testing Y_front = {y_front} ---")
    items = [
        ('J8', xs[0], y_front - 8.8, 9.9, 11.5, -2.45, 7.45, -2.7, 8.8),
        ('J7', xs[1], y_front - 1.8, 8.94, 7.3, -4.47, 4.47, -5.5, 1.8),
        ('J10', xs[2], y_front - 8.8, 14.9, 11.5, -2.45, 12.45, -2.7, 8.8),
        ('J9', xs[3], y_front - 8.8, 9.9, 11.5, -2.45, 7.45, -2.7, 8.8),
    ]
    all_ok = True
    for name, px, py, w, h, x1, x2, y1, y2 in items:
        # 4 corners
        corners = [
            (px + x1, py + y1),
            (px + x2, py + y1),
            (px + x1, py + y2),
            (px + x2, py + y2),
        ]
        max_r = max(math.hypot(x - 100.0, y - 100.0) for x, y in corners)
        
        # check H2 and H1
        dist_h2 = min(math.hypot(x - 84.4437, y - 115.5563) for x, y in corners)
        dist_h1 = min(math.hypot(x - 115.5563, y - 115.5563) for x, y in corners)
        
        # check overlap with MCU (Y < 107.0)
        min_y = min(y for x, y in corners)
        
        oob = max_r > 34.8
        mcu_col = min_y < 107.5
        h2_col = dist_h2 < 2.9
        h1_col = dist_h1 < 2.9
        
        status = "OK"
        if oob: status = f"OOB (R={max_r:.2f} > 34.8)"
        elif mcu_col: status = f"MCU collision (Y={min_y:.2f} < 107.5)"
        elif h2_col: status = f"H2 collision (dist={dist_h2:.2f} < 2.9)"
        elif h1_col: status = f"H1 collision (dist={dist_h1:.2f} < 2.9)"
        
        print(f"  {name:<4} at ({px:6.2f}, {py:6.2f}): Max_R={max_r:5.2f} mm | Min_Y={min_y:5.2f} mm | Status: {status}")
        if status != "OK": all_ok = False
    return all_ok

test_row(124.0, [75.0, 88.0, 97.0, 116.0])
test_row(122.0, [76.0, 89.0, 98.0, 115.0])
test_row(120.0, [77.0, 89.0, 98.0, 114.0])
