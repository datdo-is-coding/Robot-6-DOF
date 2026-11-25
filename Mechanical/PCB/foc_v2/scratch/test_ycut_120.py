import math

# Let's test a flat cut at Y = 120.0 .. 122.0:
# Circle: (100, 100), R = 35.0 mm.
# H2 = (84.444, 115.556), H1 = (115.556, 115.556)

for y_cut in [119.0, 119.5, 120.0, 120.5, 121.0]:
    dy = y_cut - 100.0
    dx = math.sqrt(35.0**2 - dy**2)
    width = 2 * dx
    x_left = 100.0 - dx
    x_right = 100.0 + dx
    print(f"\n--- Y_cut = {y_cut:.1f} (Chord width = {width:.2f} mm, X in [{x_left:.2f}, {x_right:.2f}]) ---")
    
    # H2 and H1 are at Y = 115.556.
    # Distance from H2 to flat cut = y_cut - 115.556:
    print(f"  H2/H1 distance to flat edge: {y_cut - 115.556:.2f} mm")
    
    # If JST-XH connectors face South with front face flush with y_cut:
    # y_orig = y_cut - 9.20.
    y_orig_xh = y_cut - 9.20
    # Connector body occupies Y in [y_orig_xh - 2.30, y_cut]:
    y_back_xh = y_orig_xh - 2.30
    print(f"  JST-XH pins Y = {y_orig_xh:.2f}, body Y in [{y_back_xh:.2f}, {y_cut:.2f}]")
    print(f"  H2 Y = 115.56 is inside connector Y-span? {y_back_xh <= 115.556 <= y_cut}")
