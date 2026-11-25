import math

# Circle: center (100, 100), R = 35.0 mm
# H2 = (84.444, 115.556), radius 2.95
# H1 = (115.556, 115.556), radius 2.95

# Let's test if an exact placement exists for any y_cut in [122.0 .. 126.0]
# Connectors:
# J8 (3-pin XH): crtyd x in [-2.95, 7.95], y in [-2.81, 9.70]
# J9 (3-pin XH): crtyd x in [-2.95, 7.95], y in [-2.81, 9.70]
# J10 (5-pin XH): crtyd x in [-2.95, 12.95], y in [-2.81, 9.70]
# J7 (USB-C): crtyd x in [-5.32, 5.32], y in [-4.85, 4.18]

def rect_circle_overlap(rx1, ry1, rx2, ry2, cx, cy, r):
    # closest point on rect to (cx, cy)
    qx = max(rx1, min(cx, rx2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

# We want all connectors to align at the South edge:
# For J8, J9, J10: front face is y + 9.20. Let front face be y_cut (or y_cut - 0.2)
# For J7: front face is y + 3.79. Let front face be y_cut (or y_cut - 0.2)

H2 = (84.444, 115.556, 2.95)
H1 = (115.556, 115.556, 2.95)

results = []

for y_cut in [123.0, 123.5, 124.0, 124.5, 125.0]:
    dy = y_cut - 100.0
    dx_max = math.sqrt(35.0**2 - dy**2)
    x_left_edge = 100.0 - dx_max
    x_right_edge = 100.0 + dx_max
    
    # Try different connector orders:
    # We have 4 connectors: J8, J9, J7, J10
    import itertools
    for order in itertools.permutations(['J8', 'J9', 'J7', 'J10']):
        # Define crtyd dimensions for each:
        # We need to choose x positions for c0, c1, c2, c3 such that:
        # x_left_edge <= crtyd_min
        # crtyd_max <= x_right_edge
        # no crtyd overlap between adjacent connectors (gap >= 0.2mm)
        # no overlap with H1, H2
        
        # Let's use a fine grid search for the 4 x-positions:
        # To make grid search fast:
        # Let's find valid intervals for each connector independently!
        valid_x = {}
        for c in ['J8', 'J9', 'J7', 'J10']:
            valid_x[c] = []
            if c in ['J8', 'J9']:
                y_orig = y_cut - 9.20
                lx1, lx2 = -2.95, 7.95
                ly1, ly2 = y_orig - 2.81, y_orig + 9.70
            elif c == 'J10':
                y_orig = y_cut - 9.20
                lx1, lx2 = -2.95, 12.95
                ly1, ly2 = y_orig - 2.81, y_orig + 9.70
            elif c == 'J7':
                y_orig = y_cut - 3.79
                lx1, lx2 = -5.32, 5.32
                ly1, ly2 = y_orig - 4.85, y_orig + 4.18
                
            # Test x_orig from x_left_edge + 5 to x_right_edge - 5
            x_test = x_left_edge - lx1 + 0.2
            while x_test + lx2 <= x_right_edge - 0.2:
                # check H1, H2
                rx1, rx2 = x_test + lx1, x_test + lx2
                ry1, ry2 = ly1, ly2
                if not rect_circle_overlap(rx1, ry1, rx2, ry2, H2[0], H2[1], H2[2]) and \
                   not rect_circle_overlap(rx1, ry1, rx2, ry2, H1[0], H1[1], H1[2]):
                    valid_x[c].append((x_test, rx1, rx2, y_orig, ry1, ry2))
                x_test += 0.25
        
        # Now check if we can pick one from each in 'order' with gaps >= 0.2:
        # c0, c1, c2, c3
        c0, c1, c2, c3 = order
        for p0 in valid_x[c0]:
            # p0[2] is rx2
            for p1 in valid_x[c1]:
                if p1[1] < p0[2] + 0.2:
                    continue
                for p2 in valid_x[c2]:
                    if p2[1] < p1[2] + 0.2:
                        continue
                    for p3 in valid_x[c3]:
                        if p3[1] < p2[2] + 0.2:
                            continue
                        results.append({
                            'y_cut': y_cut,
                            'order': order,
                            'p': {c0: p0, c1: p1, c2: p2, c3: p3},
                            'span': (p0[1], p3[2]),
                            'edges': (x_left_edge, x_right_edge)
                        })
                        break # find one p3 per p2
                    if len(results) > 0 and results[-1]['p'].get(c2) == p2:
                        break # find one p2 per p1
                if len(results) > 0 and results[-1]['p'].get(c1) == p1:
                    break # find one p1 per p0
            if len(results) > 10:
                break
        if len(results) > 50:
            break
    if len(results) > 100:
        break

print(f"Total valid arrangements found: {len(results)}")
for r in results[:5]:
    print(f"\ny_cut={r['y_cut']}, order={r['order']}, span=[{r['span'][0]:.2f}, {r['span'][1]:.2f}] within [{r['edges'][0]:.2f}, {r['edges'][1]:.2f}]:")
    for c in r['order']:
        p = r['p'][c]
        print(f"  {c:4s}: pos=({p[0]:.2f}, {p[3]:.2f}), CrtYd X=[{p[1]:.2f}, {p[2]:.2f}], Y=[{p[4]:.2f}, {p[5]:.2f}]")
