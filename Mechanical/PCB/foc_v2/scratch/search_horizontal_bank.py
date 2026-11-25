import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

delta = 22.0 / math.sqrt(2)
HOLES = {
    "H3": (100 - delta, 100 - delta), # (84.444, 84.444)
    "H4": (100 + delta, 100 - delta), # (115.556, 84.444)
    "H2": (100 - delta, 100 + delta), # (84.444, 115.556)
    "H1": (100 + delta, 100 + delta), # (115.556, 115.556)
}
R_KO = 3.2

# Let's test if 3 XH connectors (J8, J9, J10) + J7 (Type-C) can fit in:
# Case 1: Horizontal row at South
# What if J7 (Type-C) is in the South flat cut (width 9mm), and J8, J9, J10 are also there?
# We already found: total width of (J8: 10.9, J9: 10.9, J7: 9.0, J10: 15.9) = 46.7 mm.
# What if J8 and J9 (CAN_IN, CAN_OUT) and J7 (Type-C) are at South? Width = 10.9 + 10.9 + 9.0 = 30.8 mm!
# 30.8 mm fits into the South flat cut (width 36 mm at y=130)!
# And where is J10 (SWD)?
# Wait, can J10 ALSO fit?
# Let's check: what if the connectors are NOT all at the same Y?
# Wait, the user said: "các cổng kết nối hãy đặt thẳng hàng nhau, tránh để lung tung không có hàng lối"
# Can ALL 4 connectors be in a straight line?
# Let's test EVERY possible line:
# 1. Horizontal line: Y = const.
# 2. Vertical line: X = const.

# Let's test horizontal line:
# If connectors are:
# C1, C2, C3, C4 in some order.
# Let's test all 24 permutations of (J8, J9, J7, J10) along a horizontal line Y!
import itertools

conns = {
    "J8": (10.9, 12.51, 0, 9.70), # w, h, x_offset_from_pad1, y_front_from_pad1
    "J9": (10.9, 12.51, 0, 9.70),
    "J10": (15.9, 12.51, 0, 9.70),
    "J7": (9.0, 8.5, 0, 3.75) # Type-C
}

print("Searching for valid horizontal configurations...")
valid_configs = []
for perm in itertools.permutations(["J8", "J9", "J7", "J10"]):
    # We want to place them along X with some spacing gap >= 1.0 mm
    # Try Y_front from 120.0 to 134.0 in steps of 0.5 mm:
    for y_front in [122.0, 123.0, 124.0, 125.0, 126.0, 127.0, 128.0, 129.0, 130.0, 131.0, 132.0]:
        # Center the bank around X=100 or test X_offset
        total_w = sum(conns[c][0] for c in perm) + 3 * 1.5
        for x_center in [98.0, 99.0, 100.0, 101.0, 102.0]:
            x_start = x_center - total_w / 2.0
            
            # Place each connector
            cur_x = x_start
            all_ok = True
            placed = {}
            for c_name in perm:
                w, h, _, y_front_rel = conns[c_name]
                xmin = cur_x
                xmax = cur_x + w
                ymax = y_front
                ymin = y_front - h
                
                # Check corners
                corners = [(xmin, ymin), (xmin, ymax), (xmax, ymin), (xmax, ymax)]
                for px, py in corners:
                    if math.hypot(px - CX, py - CY) > 34.5: # 0.5mm inside 35mm
                        all_ok = False
                        break
                    for h_name, (hx, hy) in HOLES.items():
                        if math.hypot(px - hx, py - hy) < R_KO:
                            all_ok = False
                            break
                    if not all_ok:
                        break
                if not all_ok:
                    break
                placed[c_name] = (xmin, xmax, ymin, ymax)
                cur_x += w + 1.5
            
            if all_ok:
                valid_configs.append((y_front, x_center, perm, placed))

print(f"Found {len(valid_configs)} valid horizontal configurations with all 4 connectors inside circle & clearing holes!")
for cfg in valid_configs[:5]:
    print("  Y_front:", cfg[0], "X_center:", cfg[1], "Order:", cfg[2])
