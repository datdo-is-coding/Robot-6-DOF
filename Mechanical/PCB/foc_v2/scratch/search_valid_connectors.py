import math

# Let's write an optimizer / search script for the South connector bank
# Constraints:
# 1. Circle R = 35.0, center (100, 100).
# 2. Flat cut at Y = y_cut.
#    Chord endpoints: (100 - dx, y_cut) to (100 + dx, y_cut), where dx = sqrt(35^2 - (y_cut - 100)^2)
# 3. Mounting holes at PCD 44:
#    H2 = (84.444, 115.556), H1 = (115.556, 115.556).
#    Keepout radius = 2.8 mm around H1 and H2.
# 4. Connectors:
#    J7 (USB-C): width 8.94 (crtyd 10.64), front at y_origin + 3.79 (or +4.0)
#    J8 (CAN_IN, 3-pin XH): width 9.9, depth 11.5, front at y_origin + 9.20. Pads at (x_origin, y_origin).
#    J9 (CAN_OUT, 3-pin XH): width 9.9, depth 11.5, front at y_origin + 9.20.
#    J10 (SWD, 5-pin XH): width 14.9, depth 11.5, front at y_origin + 9.20.
# 5. Connectors aligned in a straight line:
#    Their front mating faces should all be at the flat cut (Y = y_cut) or within 0.5mm of y_cut!
#    "các cổng kết nối hãy đặt thẳng hàng nhau, tránh để lung tung không có hàng lối"
# 6. Zero courtyard overlap between any connectors and holes.
# 7. All pads and courtyards must be inside the board outline (inside chord and inside circle).

# Let's test combinations of order of (J8, J9, J7, J10)
# Permutations of [J8, J9, J7, J10]:
import itertools

connectors_info = {
    'J8': {'w': 9.9, 'pad_w': 5.0, 'depth': 11.5, 'front_offset': 9.2, 'x_pad_start': 0.0, 'x_pad_end': 5.0, 'x_body_min': -2.45, 'x_body_max': 7.45, 'y_body_min': -2.3, 'y_body_max': 9.2},
    'J9': {'w': 9.9, 'pad_w': 5.0, 'depth': 11.5, 'front_offset': 9.2, 'x_pad_start': 0.0, 'x_pad_end': 5.0, 'x_body_min': -2.45, 'x_body_max': 7.45, 'y_body_min': -2.3, 'y_body_max': 9.2},
    'J10': {'w': 14.9, 'pad_w': 10.0, 'depth': 11.5, 'front_offset': 9.2, 'x_pad_start': 0.0, 'x_pad_end': 10.0, 'x_body_min': -2.45, 'x_body_max': 12.45, 'y_body_min': -2.3, 'y_body_max': 9.2},
    'J7': {'w': 8.94, 'pad_w': 8.64, 'depth': 7.5, 'front_offset': 3.79, 'x_pad_start': -4.32, 'x_pad_end': 4.32, 'x_body_min': -4.47, 'x_body_max': 4.47, 'y_body_min': -3.67, 'y_body_max': 3.79, 'crtyd_x_min': -5.32, 'crtyd_x_max': 5.32, 'crtyd_y_min': -4.85, 'crtyd_y_max': 4.18}
}

H1 = (115.556, 115.556)
H2 = (84.444, 115.556)

print("Searching valid configurations...")
# Let's test y_cut from 122.0 to 127.0 with step 0.2
valid_configs = []

for y_cut in [122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0]:
    dy = y_cut - 100.0
    dx_max = math.sqrt(35.0**2 - dy**2)
    x_left_bound = 100.0 - dx_max
    x_right_bound = 100.0 + dx_max
    chord_w = 2 * dx_max
    
    # Try different orders:
    # Most natural orders:
    # [J8, J9, J7, J10] (CAN1, CAN2, USB, SWD)
    # [J10, J8, J7, J9]
    # [J8, J7, J9, J10]
    # [J10, J7, J8, J9]
    for order in itertools.permutations(['J8', 'J9', 'J7', 'J10']):
        # If J8 and J9 are separated, CAN in and CAN out aren't adjacent, which is less ideal, but let's check all
        # We prefer J8 and J9 adjacent:
        if abs(order.index('J8') - order.index('J9')) != 1:
            continue
            
        # Total minimum width needed with 1.0mm gap:
        total_w = sum(connectors_info[c]['w'] for c in order) + 3 * 1.0
        if total_w > chord_w - 0.5:
            continue
            
        # Let's slide X_start:
        # X spans [X_start, X_start + total_w]
        # We need X_start >= x_left_bound + 0.5 and X_start + total_w <= x_right_bound - 0.5
        min_start = x_left_bound + 0.5
        max_start = x_right_bound - 0.5 - total_w
        
        # Test 20 steps of X_start
        steps = 30
        for s in range(steps + 1):
            x_start = min_start + s * (max_start - min_start) / steps
            
            # Place connectors along X
            curr_x = x_start
            placed = {}
            collision = False
            
            for c in order:
                info = connectors_info[c]
                # x_origin:
                # c's body starts at curr_x.
                # Since x_body_min is info['x_body_min'], x_origin = curr_x - info['x_body_min']
                x_orig = curr_x - info['x_body_min']
                y_orig = y_cut - info['front_offset']
                
                # Check collision with H1 and H2:
                # For through-hole pads or SMT pads:
                # We check bounding box of this connector against H1, H2 with keepout radius 2.8mm
                # Connector world bounds:
                c_xmin = x_orig + info['x_body_min']
                c_xmax = x_orig + info['x_body_max']
                c_ymin = y_orig + info['y_body_min']
                c_ymax = y_orig + info['y_body_max']
                
                # Pad world bounds:
                p_xmin = x_orig + info['x_pad_start']
                p_xmax = x_orig + info['x_pad_end']
                p_ymin = y_orig - 1.0
                p_ymax = y_orig + 1.0
                
                # Distance of H1 and H2 to connector pads and body:
                for hx, hy in [H1, H2]:
                    # check if (hx, hy) circle of radius 2.8 overlaps with [c_xmin, c_xmax] x [c_ymin, c_ymax]
                    # closest point in box to (hx, hy)
                    qx = max(c_xmin, min(hx, c_xmax))
                    qy = max(c_ymin, min(hy, c_ymax))
                    dist = math.hypot(hx - qx, hy - qy)
                    if dist < 2.8: # keepout radius 2.8mm
                        collision = True
                        break
                if collision:
                    break
                    
                placed[c] = (x_orig, y_orig, curr_x, curr_x + info['w'])
                curr_x += info['w'] + 1.0
                
            if not collision:
                valid_configs.append({
                    'y_cut': y_cut,
                    'order': order,
                    'x_start': x_start,
                    'placed': placed,
                    'chord_w': chord_w
                })

print(f"Total valid collision-free configurations found: {len(valid_configs)}")
if valid_configs:
    # Print sample best configurations
    for vc in valid_configs[:10]:
        print(f"\ny_cut={vc['y_cut']:.1f}, order={vc['order']}, chord_w={vc['chord_w']:.2f}:")
        for c in vc['order']:
            xo, yo, x1, x2 = vc['placed'][c]
            print(f"  {c:4s}: pos=({xo:.2f}, {yo:.2f}), X in [{x1:.2f}, {x2:.2f}]")
