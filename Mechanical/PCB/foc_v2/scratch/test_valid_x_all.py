import math

# Let's test where J8, J9, J10 can sit along Y_front = 123.2:
# We know J7 is at (100.0, 119.41). Its courtyard in X is [94.68, 105.32].
# H2 is at (84.444, 115.556), keepout r = 2.95 mm.
# H1 is at (115.556, 115.556), keepout r = 2.95 mm.

# Let's inspect the available X space:
# Circle boundary at flat cut Y = 123.5:
# dy = 23.5 => dx = sqrt(35^2 - 23.5^2) = 25.94 mm.
# Left corner: X = 74.06. Right corner: X = 125.94.

# What if:
# Can J9 sit between H2 and J7?
# Space between H2 (84.444 + 2.95 = 87.39) and J7 (94.68):
# Width = 94.68 - 87.39 = 7.29 mm.
# But J9 courtyard is 10.90 mm wide!
# So J9 cannot fit entirely between H2 and J7 without either:
# a) touching H2 courtyard, or
# b) touching J7 courtyard!
# BUT WAIT: What if J7 is shifted slightly to the right, e.g. X = 102 or 103?
# Or what if J8 and J9 are on the OTHER side?
# Or what if J10 is on the left?

# Let's test ALL valid positions of (c1, c2, c3, c4) along X in [74.06, 125.94]
# where any connector can have its front face at 123.2!

print("Testing all combinations...")
def rect_circle_col(rx1, ry1, rx2, ry2, cx, cy, r):
    qx = max(rx1, min(cx, rx2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

# Let's check for each connector:
# What x_orig positions have NO collision with H2 and H1?
for name, w_left, w_right in [('3pin', 2.95, 7.95), ('5pin', 2.95, 12.95), ('usb', 5.32, 5.32)]:
    if name == 'usb':
        y1, y2 = 119.41 - 4.85, 119.41 + 4.18
    else:
        y1, y2 = 114.00 - 2.81, 114.00 + 9.70
    valid_x = []
    for x in [val * 0.1 for val in range(700, 1300)]:
        rx1 = x - w_left
        rx2 = x + w_right
        # check H2 and H1
        if not rect_circle_col(rx1, y1, rx2, y2, 84.444, 115.556, 2.95) and \
           not rect_circle_col(rx1, y1, rx2, y2, 115.556, 115.556, 2.95):
            valid_x.append(x)
    if valid_x:
        # group into ranges
        ranges = []
        r_start = valid_x[0]
        r_prev = valid_x[0]
        for v in valid_x[1:]:
            if v - r_prev > 0.15:
                ranges.append((r_start, r_prev))
                r_start = v
            r_prev = v
        ranges.append((r_start, r_prev))
        print(f"{name:5s} valid x_orig ranges:")
        for r in ranges:
            print(f"   [{r[0]:.2f} .. {r[1]:.2f}] (width: {r[1]-r[0]:.2f})")
    else:
        print(f"{name:5s}: NO valid positions!")
