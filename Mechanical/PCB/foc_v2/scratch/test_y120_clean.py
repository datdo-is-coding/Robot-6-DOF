import math

# Test connector placement with front face at Y_front = 119.5 mm:
# Flat cut at Y_cut = 120.0 mm!
# Circle: (100, 100), R = 35.0 mm.

H2 = (84.444, 115.556, 2.95)
H1 = (115.556, 115.556, 2.95)

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

y_cut = 120.0
y_front = 119.5

# Connectors:
# For JST-XH: y_orig = y_front - 9.20 = 110.30.
#   Crtyd Y: [110.30 - 2.81, 110.30 + 9.70] = [107.49, 120.00]
# For USB-C J7: y_orig = y_front - 3.79 = 115.71.
#   Crtyd Y: [115.71 - 4.85, 115.71 + 4.18] = [110.86, 119.89]

xh_y1, xh_y2 = 107.49, 120.00
usb_y1, usb_y2 = 110.86, 119.89

print(f"Y-spans: XH [{xh_y1:.2f}, {xh_y2:.2f}], USB [{usb_y1:.2f}, {usb_y2:.2f}]")

# Let's test the 4 positions:
# Position 1 (West of H2): J8 (3-pin XH)
# Crtyd: [x - 2.95, x + 7.95]
# We want x + 7.95 <= 84.444 - 2.95 = 81.49 => x <= 73.54. Let x = 73.50.
rx1, rx2 = 73.50 - 2.95, 73.50 + 7.95 # [70.55, 81.45]
j8_in = rect_in_circle(rx1, xh_y1, rx2, xh_y2)
j8_col = rect_circle_overlap(rx1, xh_y1, rx2, xh_y2, H2[0], H2[1], H2[2])
print(f"J8 at 73.50: X=[{rx1:.2f}, {rx2:.2f}] in_circle={j8_in}, col_H2={j8_col}")

# Position 2 (Center Left): J7 (USB-C)
# Crtyd: [x - 5.32, x + 5.32]
# We want x - 5.32 >= 84.444 + 2.95 = 87.39 => x >= 92.71. Let x = 93.50.
rx1, rx2 = 93.50 - 5.32, 93.50 + 5.32 # [88.18, 98.82]
j7_in = rect_in_circle(rx1, usb_y1, rx2, usb_y2)
j7_col = rect_circle_overlap(rx1, usb_y1, rx2, usb_y2, H2[0], H2[1], H2[2])
print(f"J7 at 93.50: X=[{rx1:.2f}, {rx2:.2f}] in_circle={j7_in}, col_H2={j7_col}")

# Position 3 (Center Right): J9 (CAN_OUT 3-pin XH)
# Crtyd: [x - 2.95, x + 7.95]
# Gap to J7: x - 2.95 >= 98.82 + 0.5 = 99.32 => x >= 102.27. Let x = 103.0.
rx1, rx2 = 103.0 - 2.95, 103.0 + 7.95 # [100.05, 110.95]
# Distance to H1: 115.556 - 2.95 = 112.61 => 110.95 <= 112.61 (1.66mm margin!)
j9_in = rect_in_circle(rx1, xh_y1, rx2, xh_y2)
j9_col = rect_circle_overlap(rx1, xh_y1, rx2, xh_y2, H1[0], H1[1], H1[2])
print(f"J9 at 103.00: X=[{rx1:.2f}, {rx2:.2f}] in_circle={j9_in}, col_H1={j9_col}")

# Position 4 (East of H1): J10 (SWD 5-pin XH)
# Crtyd: [x - 2.95, x + 12.95]
# We want x - 2.95 >= 115.556 + 2.95 = 118.51 => x >= 121.46. Let x = 121.50.
rx1, rx2 = 121.50 - 2.95, 121.50 + 12.95 # [118.55, 134.45]
j10_in = rect_in_circle(rx1, xh_y1, rx2, xh_y2)
j10_col = rect_circle_overlap(rx1, xh_y1, rx2, xh_y2, H1[0], H1[1], H1[2])
print(f"J10 at 121.50: X=[{rx1:.2f}, {rx2:.2f}] in_circle={j10_in}, col_H1={j10_col}")
