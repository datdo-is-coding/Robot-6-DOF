import math

cx, cy = 100.0, 100.0
r_board = 35.0

holes = [
    (115.556, 115.556, "H1"),
    (84.444, 115.556, "H2"),
    (84.444, 84.444, "H3"),
    (115.556, 84.444, "H4")
]
hole_r = 2.95 # keepout radius

def check_hole_collision(box):
    for hx, hy, name in holes:
        closest_x = max(box[0], min(hx, box[1]))
        closest_y = max(box[2], min(hy, box[3]))
        dist = math.sqrt((hx - closest_x)**2 + (hy - closest_y)**2)
        if dist < hole_r:
            return True, name
    return False, None

def check_inside_board(box, y_cut):
    for x in [box[0], box[1]]:
        for y in [box[2], box[3]]:
            if y > y_cut + 0.1: # tolerance
                return False
            if math.sqrt((x - cx)**2 + (y - cy)**2) > (r_board - 0.2):
                return False
    return True

# Let's test combinations of (order of connectors) and y_cut:
# Connectors: J8 (CAN_IN, w=10.51), J9 (CAN_OUT, w=10.51), J7 (Type-C, w=10.64), J10 (SWD, w=15.51)
# What if some connectors face South, or what if J8/J9 or J10 are vertical or what?
# Wait, user prompt:
# "các cổng kết nối hãy đặt thẳng hàng nhau, tránh để lung tung không có hàng lối"
# "thẳng hàng nhau" = aligned in a straight line!
# "đổi các header thành loại xh-2.54 cong"
# All facing South along the flat cut!

# Let's test different combinations of order, e.g.:
# [J8, J7, J9, J10]
# [J8, J9, J7, J10]
# [J10, J8, J7, J9]
# or what if the flat cut is at different y_cut?
# Let's check for various y_cut from 118 to 127:

for y_cut in [118.0, 119.0, 120.0, 121.0, 122.0, 123.0, 124.0, 125.0]:
    # chord width at y_cut:
    dy = y_cut - 100.0
    if dy >= r_board: continue
    dx_max = math.sqrt(r_board**2 - dy**2)
    x_min_chord = 100.0 - dx_max
    x_max_chord = 100.0 + dx_max
    chord_len = 2 * dx_max
    # print(f"y_cut={y_cut}: chord X in [{x_min_chord:.2f}, {x_max_chord:.2f}] (len={chord_len:.2f})")

# Let's test specific positions:
# Suppose J7 is at center x=100.0. J7 box:
# y_front = y_cut
# J7: x in [94.68, 105.32], y in [y_cut - 9.03, y_cut]
# What connectors can fit to the left and right?
# Space between H2 (84.444) and H1 (115.556):
# Left of J7 (x=94.68) to H2 right edge (84.444 + 2.95 = 87.394): space is 94.68 - 87.394 = 7.28 mm.
# Can a 10.5mm connector fit in 7.28mm? NO!
# So NO connector can sit between H2 and J7, or between J7 and H1 if J7 is at 100!

print("\nKey insight: If J7 is at x=100, the gap between J7 and H2 is 7.28 mm (too narrow for a 10.5 mm connector).")
print("What if J7 is NOT at x=100, or what if two connectors are in the center?")
# Corridor between H2 and H1: [87.40, 112.60] -> width = 25.20 mm.
# Can two connectors fit in 25.20 mm?
# J7 (10.64) + J8 (10.51) = 21.15 mm!
# 21.15 mm < 25.20 mm! YES! J7 + J8 FIT IN THE CENTER CORRIDOR TOGETHER!
# Margin = 25.20 - 21.15 = 4.05 mm!
