import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

# Holes PCD 44 mm:
delta_h = 22.0 / math.sqrt(2)
H2 = (CX - delta_h, CY + delta_h) # (84.444, 115.556)
H1 = (CX + delta_h, CY + delta_h) # (115.556, 115.556)
R_KO = 3.0

print(f"H2 center: {H2}, H1 center: {H1}")

# We want 4 connectors: J8 (XH 3p), J9 (XH 3p), J7 (USB-C), J10 (SWD XH 5p)
# Or J8 (CAN_IN), J9 (CAN_OUT), J7 (Type-C), J10 (SWD)
# Footprint specs:
# XH 3p (J8, J9): Pad 1 at (0, 0), Pad 3 at (5.0, 0).
#   X span: [-2.95, 7.95] relative to Pad 1.
#   Y span: [-2.81, 9.70] relative to Pad 1.
# XH 5p (J10): Pad 1 at (0, 0), Pad 5 at (10.0, 0).
#   X span: [-2.95, 12.95] relative to Pad 1.
#   Y span: [-2.81, 9.70] relative to Pad 1.
# USB-C (J7): Center at (0, 0).
#   X span: [-4.50, 4.50]
#   Y span: [-4.85, 3.70] (mouth at +3.70)

# Let's test South flat cut Y_cut:
# If Y_cut = 131.0:
# For XH connectors to be inside the board:
# Y_pin + 9.70 <= Y_cut => Y_pin <= Y_cut - 9.70
# If Y_cut = 130.0: Y_pin <= 120.30
# If Y_cut = 131.0: Y_pin <= 121.30
# If Y_cut = 132.0: Y_pin <= 122.30

# What if the board has NO flat cut at all, or a flat cut only where needed?
# Wait! Can the board have a flat cut at Y_cut = 131.0?
# Let's check what the board circle looks like at Y in [115, 131]:
for y in [128.0, 129.0, 130.0, 131.0, 132.0]:
    dy = y - CY
    if dy < R_BOARD:
        dx = math.sqrt(R_BOARD**2 - dy**2)
        print(f"At Y={y:.1f}: Board X span is [{CX - dx:.2f}, {CX + dx:.2f}], width = {2*dx:.2f} mm")
