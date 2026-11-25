import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

# PCD 44 Holes:
delta = 22.0 / math.sqrt(2)
H2 = (100 - delta, 100 + delta) # (84.444, 115.556)
H1 = (100 + delta, 100 + delta) # (115.556, 115.556)
R_KO = 3.0 # keepout radius

print(f"H2: ({H2[0]:.3f}, {H2[1]:.3f})")
print(f"H1: ({H1[0]:.3f}, {H1[1]:.3f})")

# Let's inspect JST-XH footprint exact courtyard relative to footprint center (at X Y):
# For S3B-XH-A (3-pin):
# If Pad 1 is at (0, 0), Pad 3 at (5, 0). Center of pads is at (2.5, 0).
# In KiCad footprint: Pad 1 is at (0, 0).
# X span: [-2.95, 7.95] (width 10.9 mm)
# Y span: [-2.81, 9.70] (depth 12.51 mm)
# If placed at (X, Y):
# X range of body: [X - 2.95, X + 7.95]
# Y range of body: [Y - 2.81, Y + 9.70]

# For S5B-XH-A (5-pin):
# Pad 1 is at (0, 0), Pad 5 at (10, 0).
# X span: [-2.95, 12.95] (width 15.9 mm)
# Y span: [-2.81, 9.70] (depth 12.51 mm)
# If placed at (X, Y):
# X range of body: [X - 2.95, X + 12.95]
# Y range of body: [Y - 2.81, Y + 9.70]

# For USB-C (J7):
# Footprint center (at X Y):
# X range of body: [X - 4.58, X + 4.58] (courtyard is ~[-5.3, 5.3])
# Y range of body: [Y - 4.85, Y + 3.75] (front mouth at Y + 3.75)

# Notice: All connectors have their mating face pointing in +Y (South)!
# If they are in a straight row, their front edges can align!
# Front of JST-XH is at Y_pin + 9.70.
# Front of USB-C is at Y_usbc + 3.75.
# If their front faces align at Y_front:
# Y_pin = Y_front - 9.70
# Y_usbc = Y_front - 3.75

# Now let's test values of Y_front and connector X positions!
# For any point (px, py) on a connector:
# 1. Must be inside board: math.hypot(px - 100, py - 100) <= 35.0
# 2. Must be outside H1, H2 keepouts:
#    math.hypot(px - H2[0], py - H2[1]) >= 3.2
#    math.hypot(px - H1[0], py - H1[1]) >= 3.2

def check_connector_box(xmin, xmax, ymin, ymax, name):
    # Check 4 corners and midpoints against board circle and hole keepouts
    pts = [
        (xmin, ymin), (xmax, ymin), (xmin, ymax), (xmax, ymax),
        ((xmin+xmax)/2, ymin), ((xmin+xmax)/2, ymax),
        (xmin, (ymin+ymax)/2), (xmax, (ymin+ymax)/2)
    ]
    for px, py in pts:
        d_board = math.hypot(px - 100, py - 100)
        if d_board > 35.0:
            return False, f"{name} corner ({px:.2f}, {py:.2f}) outside board: R={d_board:.2f} > 35.0"
        
        # Check against H2 keepout
        d_h2 = math.hypot(px - H2[0], py - H2[1])
        if d_h2 < 3.2:
            return False, f"{name} point ({px:.2f}, {py:.2f}) inside H2 keepout: d={d_h2:.2f} < 3.2"
        
        # Check against H1 keepout
        d_h1 = math.hypot(px - H1[0], py - H1[1])
        if d_h1 < 3.2:
            return False, f"{name} point ({px:.2f}, {py:.2f}) inside H1 keepout: d={d_h1:.2f} < 3.2"
            
    return True, "OK"

# Let's test Y_front from 124.0 to 132.0:
for y_front in [124.0, 125.0, 126.0, 127.0, 128.0, 129.0, 130.0]:
    y_pin = y_front - 9.70
    y_usbc = y_front - 3.75
    print(f"\n--- Testing Y_front = {y_front:.1f} (Y_pin = {y_pin:.2f}, Y_usbc = {y_usbc:.2f}) ---")
    
    # Let's see: corridor between H2 and H1 is x in [87.45, 112.55] (width 25.1 mm).
    # Can we put J7 (USB-C, width 10mm) and J8 or J9 in the corridor?
    # What can fit in the corridor:
    # 25.1 mm can fit J7 (10mm) + one XH-3p (11mm) = 21mm!
    # But NOT all 4 connectors!
    # So 2 connectors must be outside the corridor (one to the left of H2, one to the right of H1)?
    # Wait! Can an XH connector fit to the left of H2 (x < 81.44)?
    # Let's check:
    # Left edge of board at y in [y_pin - 2.81, y_front]:
    # At y_pin = 116.3: circle left edge is 100 - sqrt(35^2 - 16.3^2) = 100 - 31.0 = 69.0.
    # At y_front = 126.0: circle left edge is 100 - sqrt(35^2 - 26.0^2) = 100 - 23.4 = 76.6!
    # So if an XH is to the left of H2: its right edge must be < 81.44 (H2 keepout left),
    # so its body X is [X - 2.95, X + 7.95] <= 81.44 => X + 7.95 <= 81.44 => X <= 73.49!
    # Then its left edge is X - 2.95 <= 70.54!
    # But at y_front = 126.0, the board edge is at 76.6! 70.54 is FAR OUTSIDE THE BOARD!
    print(f"  At Y_front={y_front:.1f}, circle Xmin={100 - math.sqrt(35**2 - (y_front-100)**2):.2f}. Max X to avoid H2 is 73.49.")
