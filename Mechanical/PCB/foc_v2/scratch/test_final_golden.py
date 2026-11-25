import math

# Golden layout verification:
# Connectors front face at Y_front = 120.0 mm.
# Flat cut at Y_cut = 120.2 mm.

# J8: CAN_IN (3-pin XH), at (74.0, y_orig)
# J7: USB-C, at (92.5, y_orig)
# J10: SWD (5-pin XH), at (100.0, y_orig)
# J9: CAN_OUT (3-pin XH), at (121.0, y_orig)

# y_orig for XH: y_front - 9.20 = 120.0 - 9.20 = 110.80 mm.
# y_orig for USB: y_front - 3.79 = 120.0 - 3.79 = 116.21 mm.

H2 = (84.444, 115.556)
H1 = (115.556, 115.556)

conns = {
    'J8':  {'x': 74.0,  'y': 110.80, 'w_left': 2.45, 'w_right': 7.45,  'd_back': 2.30, 'd_front': 9.20, 'pads': [0.0, 2.5, 5.0]},
    'J7':  {'x': 92.5,  'y': 116.21, 'w_left': 4.47, 'w_right': 4.47,  'd_back': 3.67, 'd_front': 3.79, 'pads': [-4.32, 4.32]},
    'J10': {'x': 100.0, 'y': 110.80, 'w_left': 2.45, 'w_right': 12.45, 'd_back': 2.30, 'd_front': 9.20, 'pads': [0.0, 2.5, 5.0, 7.5, 10.0]},
    'J9':  {'x': 121.0, 'y': 110.80, 'w_left': 2.45, 'w_right': 7.45,  'd_back': 2.30, 'd_front': 9.20, 'pads': [0.0, 2.5, 5.0]},
}

print("Checking connector bounds:")
all_pass = True
for name, c in conns.items():
    x1 = c['x'] - c['w_left']
    x2 = c['x'] + c['w_right']
    y1 = c['y'] - c['d_back']
    y2 = c['y'] + c['d_front']
    
    # check 4 corners inside circle R = 35.0
    corners = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
    in_circle = all(math.hypot(px - 100, py - 100) <= 35.05 for px, py in corners)
    
    # check distances to H2 and H1
    dist_h2 = math.hypot(H2[0] - max(x1, min(H2[0], x2)), H2[1] - max(y1, min(H2[1], y2)))
    dist_h1 = math.hypot(H1[0] - max(x1, min(H1[0], x2)), H1[1] - max(y1, min(H1[1], y2)))
    
    print(f"  {name:4s}: X in [{x1:.2f}, {x2:.2f}], Y in [{y1:.2f}, {y2:.2f}], front Y={y2:.2f}")
    print(f"        in_circle={in_circle}, dist_H2={dist_h2:.2f}mm, dist_H1={dist_h1:.2f}mm")
    if not in_circle or min(dist_h2, dist_h1) < 2.5:
        all_pass = False

print(f"\nALL CONSTRAINTS PASSED: {all_pass}")
