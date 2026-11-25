import math

# Let's test various placements for J8, J9, J7, J10 and check:
# 1. Distance to H2 (84.444, 115.556) and H1 (115.556, 115.556)
# 2. Fit within circle R = 35 centered at (100, 100)
# 3. Fit on flat cut at Y_cut

# Connectors:
# J8 (CAN_IN): X_local in [-2.5, 7.5], Y_local in [-2.4, 9.3]
# J9 (CAN_OUT): X_local in [-2.5, 7.5], Y_local in [-2.4, 9.3]
# J7 (USB-C): X_local in [-5.3, 5.3], Y_local in [-4.8, 4.2]
# J10 (SWD): X_local in [-2.5, 12.5], Y_local in [-2.4, 9.3]

# In KiCad:
# H2 keepout: circle center (84.444, 115.556), radius 2.8 mm
# H1 keepout: circle center (115.556, 115.556), radius 2.8 mm

for y_cut in [124.0, 125.0, 125.5, 126.0, 127.0]:
    dy = y_cut - 100.0
    dx_max = math.sqrt(35.0**2 - dy**2)
    x_left = 100.0 - dx_max
    x_right = 100.0 + dx_max
    
    # If front face is flush with y_cut:
    # J8, J9, J10 y_pos:
    y_xh = y_cut - 9.20
    # J7 y_pos:
    y_usb = y_cut - 3.80
    
    print(f"\n--- Y_cut = {y_cut:.1f} (Chord: [{x_left:.2f}, {x_right:.2f}], width: {2*dx_max:.2f}) ---")
    print(f"  y_xh = {y_xh:.2f}, y_usb = {y_usb:.2f}")
    
    # Let's try arrangement: J8 (left), J9, J7 (center), J10 (right)
    # J7 at X = 100.0: X in [94.7, 105.3]
    # To the left: J9, then J8
    # To the right: J10
    # J9: width 10mm ([-2.5, 7.5])
    # J10: width 15mm ([-2.5, 12.5])
    
    # Try J7 at 100.0:
    # J9: let J9 pin 1 be at X_j9. J9 spans [X_j9 - 2.5, X_j9 + 7.5].
    # We want J9 right edge (X_j9 + 7.5) <= 100 - 5.3 - 1.5 = 93.2 => X_j9 <= 85.7.
    # J8: J8 spans [X_j8 - 2.5, X_j8 + 7.5].
    # We want J8 right edge <= X_j9 - 2.5 - 1.5 => X_j8 + 7.5 <= X_j9 - 4.0.
    # J10: J10 spans [X_j10 - 2.5, X_j10 + 12.5].
    # We want J10 left edge >= 100 + 5.3 + 1.5 = 106.8 => X_j10 >= 109.3.
    
    # Let's test specific positions:
    # J8 at 74.0: spans [71.5, 81.5]
    # J9 at 84.5: spans [82.0, 92.0]
    # J7 at 100.0: spans [94.7, 105.3]
    # J10 at 109.5: spans [107.0, 122.0]
    
    print(f"  J8: [71.5, 81.5] vs x_left={x_left:.2f} (margin: {71.5 - x_left:.2f})")
    print(f"  J10: [107.0, 122.0] vs x_right={x_right:.2f} (margin: {x_right - 122.0:.2f})")
    
    # Check H2 distance: H2 is (84.44, 115.56)
    # For J8 at (74.0, y_xh): pads are at y_xh. Pin 3 is at (79.0, y_xh).
    d_j8_h2 = math.hypot(79.0 - 84.44, y_xh - 115.56)
    print(f"  Dist J8 pin 3 to H2: {d_j8_h2:.2f} mm")
    
    # For J9 at (84.5, y_xh): J9 pin 1 is at 84.5! H2 is at 84.44!
    # WAIT! If J9 is at 84.5, J9 pads (84.5, 87.0, 89.5) are directly below H2 (84.44)!
    # What is the Y distance between J9 pads and H2?
    dy_j9_h2 = y_xh - 115.56
    print(f"  J9 pads Y - H2 Y: {dy_j9_h2:.2f} mm")
