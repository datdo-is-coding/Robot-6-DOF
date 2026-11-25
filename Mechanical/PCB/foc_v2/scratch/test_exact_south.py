import math

H2 = (84.44365, 115.55635)
H1 = (115.55635, 115.55635)
R_KO = 3.0

# J8 (XH 3p: w=9.9, h=12.51, y_pin=121.5)
# x in [84.55, 94.45], y in [118.69, 131.20]
# J9 (XH 3p: w=9.9, h=12.51, y_pin=121.5)
# x in [105.55, 115.45], y in [118.69, 131.20]
# J7 (Type-C: w=8.94, h=8.5, y_center=126.5)
# x in [95.53, 104.47], y in [122.25, 130.75]

def test_box_clearance(name, xmin, xmax, ymin, ymax):
    print(f"\nTesting {name}: X [{xmin:.2f}, {xmax:.2f}], Y [{ymin:.2f}, {ymax:.2f}]")
    # 1. Circle radius check:
    max_r = max(math.hypot(px - 100, py - 100) for px in [xmin, xmax] for py in [ymin, ymax])
    print(f"  Max radius to (100, 100): {max_r:.2f} mm (Limit: 35.0 mm) -> {'OK' if max_r <= 35.0 else 'FAIL'}")
    
    # 2. Distance to H2:
    cx2 = max(xmin, min(H2[0], xmax))
    cy2 = max(ymin, min(H2[1], ymax))
    d2 = math.hypot(cx2 - H2[0], cy2 - H2[1])
    print(f"  Distance to H2: {d2:.3f} mm (Keepout: {R_KO:.1f} mm) -> {'OK' if d2 >= R_KO else 'FAIL'}")
    
    # 3. Distance to H1:
    cx1 = max(xmin, min(H1[0], xmax))
    cy1 = max(ymin, min(H1[1], ymax))
    d1 = math.hypot(cx1 - H1[0], cy1 - H1[1])
    print(f"  Distance to H1: {d1:.3f} mm (Keepout: {R_KO:.1f} mm) -> {'OK' if d1 >= R_KO else 'FAIL'}")

test_box_clearance("J8", 84.55, 94.45, 118.69, 131.20)
test_box_clearance("J7", 95.53, 104.47, 122.25, 130.75)
test_box_clearance("J9", 105.55, 115.45, 118.69, 131.20)
