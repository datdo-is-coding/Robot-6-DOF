import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

# PCD 44 Holes:
delta = 22.0 / math.sqrt(2)
H3 = (100 - delta, 100 - delta) # 84.444, 84.444
H2 = (100 - delta, 100 + delta) # 84.444, 115.556
R_KO = 3.0

# J8: 3p (w_x=12.51, h_y=9.9)
# J9: 3p (w_x=12.51, h_y=9.9)
# J10: 5p (w_x=12.51, h_y=14.9)

# If facing West (rot=90):
# Pad 1 at (x, y).
# Shroud front is at x - 9.70.
# Shroud back is at x + 2.81.
# Width in Y for 3p: [y - 2.45, y + 7.45]
# Width in Y for 5p: [y - 2.45, y + 12.45]

# If x_pin = 76.0:
# front at x = 66.3 (inside circle at x=65!)
# back at x = 78.81 < 81.44 (clears H3 and H2 keepouts!)

# Let's test if J8, J9, J10 can be placed along Y:
for order in [("J10", "J8", "J9"), ("J8", "J9", "J10")]:
    print(f"\n--- Testing order {order} ---")
    # Total heights:
    heights = {"J8": 9.9, "J9": 9.9, "J10": 14.9}
    h_tot = sum(heights[c] for c in order) + 2 * 1.5
    print(f"Total height = {h_tot} mm")
    
    # Check Y range centered around Y=100:
    for y_center in [98.0, 99.0, 100.0, 101.0, 102.0]:
        y_cur = y_center - h_tot / 2.0
        all_ok = True
        for c in order:
            h = heights[c]
            ymin = y_cur
            ymax = y_cur + h
            # Check 4 corners of box [66.3, 78.81] x [ymin, ymax]
            for px in [66.3, 78.81]:
                for py in [ymin, ymax]:
                    d = math.hypot(px - CX, py - CY)
                    if d > 35.0:
                        all_ok = False
            y_cur += h + 1.5
        if all_ok:
            print(f"  Valid at Y_center={y_center:.1f}!")
