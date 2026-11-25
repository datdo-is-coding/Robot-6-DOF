import math

# Test arrangement:
# West: J7 (USB-C)
# Hole: H2 (84.444, 115.556)
# Center: J8 (CAN_IN 3-pin) and J9 (CAN_OUT 3-pin)
# Hole: H1 (115.556, 115.556)
# East: J10 (SWD 5-pin)

# Or West: J10, East: J7
# Let's test both!

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

# Flat cut at y_cut in [120.0 .. 124.0]
for y_cut in [120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5]:
    y_front = y_cut - 0.2
    
    y_orig_xh = y_front - 9.20
    xh_y1 = y_orig_xh - 2.81
    xh_y2 = y_orig_xh + 9.70
    
    y_orig_usb = y_front - 3.79
    usb_y1 = y_orig_usb - 4.85
    usb_y2 = y_orig_usb + 4.18
    
    # Center: J8 and J9
    # J8 crtyd: [x_j8 - 2.95, x_j8 + 7.95]
    # J9 crtyd: [x_j9 - 2.95, x_j9 + 7.95]
    # We want x_j8 - 2.95 >= 84.444 + 2.95 = 87.39 => x_j8 >= 90.34. Let x_j8 = 91.0
    # J8 crtyd: [88.05, 98.95]
    # J9: x_j9 - 2.95 >= 98.95 + 0.5 = 99.45 => x_j9 >= 102.40. Let x_j9 = 103.0
    # J9 crtyd: [100.05, 110.95]
    # Check J9 distance to H1: 115.556 - 2.95 = 112.61 => 110.95 <= 112.61 (CLEAN with 1.66 mm margin!)
    
    # Now check J8 and J9 inside circle:
    j8_in = rect_in_circle(88.05, xh_y1, 98.95, xh_y2)
    j9_in = rect_in_circle(100.05, xh_y1, 110.95, xh_y2)
    
    # Now test West and East connectors:
    # Option A: West = J7 (USB), East = J10 (SWD)
    # J7 crtyd: [x_j7 - 5.32, x_j7 + 5.32] x [usb_y1, usb_y2]
    # We want x_j7 + 5.32 <= 84.444 - 2.95 = 81.49 => x_j7 <= 76.17
    # Test x_j7 in [72 .. 76]:
    j7_found = None
    for x_j7 in [72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0]:
        rx1, rx2 = x_j7 - 5.32, x_j7 + 5.32
        if rect_in_circle(rx1, usb_y1, rx2, usb_y2) and not rect_circle_overlap(rx1, usb_y1, rx2, usb_y2, H2[0], H2[1], H2[2]):
            j7_found = x_j7
            break
            
    # J10 (5-pin) on East:
    # J10 crtyd: [x_j10 - 2.95, x_j10 + 12.95] x [xh_y1, xh_y2]
    # We want x_j10 - 2.95 >= 115.556 + 2.95 = 118.51 => x_j10 >= 121.46
    # Test x_j10:
    j10_found = None
    for x_j10 in [121.5, 122.0, 122.5, 123.0]:
        rx1, rx2 = x_j10 - 2.95, x_j10 + 12.95
        if rect_in_circle(rx1, xh_y1, rx2, xh_y2) and not rect_circle_overlap(rx1, xh_y1, rx2, xh_y2, H1[0], H1[1], H1[2]):
            j10_found = x_j10
            break
            
    print(f"y_cut={y_cut:.1f}: J8_in={j8_in}, J9_in={j9_in}, J7_found={j7_found}, J10_found={j10_found}")
