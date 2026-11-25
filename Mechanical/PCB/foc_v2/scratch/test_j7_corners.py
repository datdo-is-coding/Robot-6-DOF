import math

x_j7 = 75.0
rx1, rx2 = x_j7 - 5.32, x_j7 + 5.32 # [69.68, 80.32]
y_cut = 120.0
y_front = y_cut - 0.2
y_orig_usb = y_front - 3.79 # 116.01
usb_y1 = y_orig_usb - 4.85 # 111.16
usb_y2 = y_orig_usb + 4.18 # 120.19

for x in [rx1, rx2]:
    for y in [usb_y1, usb_y2]:
        r = math.hypot(x - 100, y - 100)
        print(f"({x:.2f}, {y:.2f}) -> r = {r:.2f} <= 35? {r <= 35.0}")
