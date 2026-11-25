import math

# Test the golden arrangement:
# J8 (3-pin) on West: X in [71.4 .. 81.3]
# H2 at (84.444, 115.556), r = 2.95
# Center: J7 (USB-C) and J10 (SWD 5-pin) in X in [87.4 .. 112.5]
# H1 at (115.556, 115.556), r = 2.95
# J9 (3-pin) on East: X in [118.7 .. 128.6]

# Let's test exact coordinates:
# Let y_cut be in [120.0 .. 123.0]
# Connectors front face at y_front = y_cut - 0.3

def rect_circle_overlap(rx1, ry1, rx2, ry2, cx, cy, r):
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

print("Testing golden connector layout...")

for y_cut in [120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0]:
    y_front = y_cut - 0.3
    # J8, J9: y_orig = y_front - 9.20. Crtyd: [x-2.95, x+7.95] x [y_orig-2.81, y_orig+9.70]
    # J10: y_orig = y_front - 9.20. Crtyd: [x-2.95, x+12.95] x [y_orig-2.81, y_orig+9.70]
    # J7: y_orig = y_front - 3.79. Crtyd: [x-5.32, x+5.32] x [y_orig-4.85, y_orig+4.18]
    
    y_orig_xh = y_front - 9.20
    xh_y1 = y_orig_xh - 2.81
    xh_y2 = y_orig_xh + 9.70
    
    y_orig_usb = y_front - 3.79
    usb_y1 = y_orig_usb - 4.85
    usb_y2 = y_orig_usb + 4.18
    
    # Try J8 at x_j8:
    # We want J8 crtyd x2 <= 84.444 - 2.95 = 81.49 => x_j8 + 7.95 <= 81.49 => x_j8 <= 73.54
    # And J8 crtyd x1 = x_j8 - 2.95.
    x_j8 = 73.50
    j8_x1, j8_x2 = x_j8 - 2.95, x_j8 + 7.95
    j8_in_circle = rect_in_circle(j8_x1, xh_y1, j8_x2, xh_y2)
    j8_col_h2 = rect_circle_overlap(j8_x1, xh_y1, j8_x2, xh_y2, H2[0], H2[1], H2[2])
    
    # Try J9 at x_j9:
    # J9 crtyd x1 >= 115.556 + 2.95 = 118.51 => x_j9 - 2.95 >= 118.51 => x_j9 >= 121.46
    x_j9 = 121.50
    j9_x1, j9_x2 = x_j9 - 2.95, x_j9 + 7.95
    j9_in_circle = rect_in_circle(j9_x1, xh_y1, j9_x2, xh_y2)
    j9_col_h1 = rect_circle_overlap(j9_x1, xh_y1, j9_x2, xh_y2, H1[0], H1[1], H1[2])
    
    # Center: J7 and J10 in [87.4 .. 112.5] (width 25.1)
    # Order: J7 on left, J10 on right, or J10 on left, J7 on right
    # Let's test J7 left:
    # J7 crtyd [x_j7 - 5.32, x_j7 + 5.32]
    # J10 crtyd [x_j10 - 2.95, x_j10 + 12.95]
    # We want x_j7 - 5.32 >= 87.44 => x_j7 >= 92.76
    # x_j10 + 12.95 <= 112.56 => x_j10 <= 99.61
    # gap between J7 and J10: (x_j10 - 2.95) - (x_j7 + 5.32) >= 0.5
    # => x_j10 - x_j7 >= 8.77
    x_j7 = 93.0
    x_j10 = 93.0 + 8.8 = 101.8 # wait, if x_j10 = 99.6, x_j7 = 90.8 < 92.76!
    # Wait, 10.64 + 15.9 = 26.54 mm!
    # 26.54 > 25.12 mm!
    # By 1.4 mm!
    print(f"y_cut={y_cut:.1f}: j8_in={j8_in_circle}, j8_col_h2={j8_col_h2}, j9_in={j9_in_circle}, j9_col_h1={j9_col_h1}")
