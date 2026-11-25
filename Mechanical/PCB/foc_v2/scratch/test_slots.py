import math

# Let's test the geometric fit of connectors in South slots.
# Board: center (100, 100), R = 35.0 mm.
# Mounting holes: H2=(84.444, 115.556), H1=(115.556, 115.556).
# Screw head M2.5 radius = 2.25 mm. With 0.2 mm clearance, R_ko = 2.45 mm.
# Connectors:
# J8: 3-pin XH (width 10.9 mm, x in [-2.95, +7.95] rel to pin 1)
# J9: 3-pin XH (width 10.9 mm)
# J10: 5-pin XH (width 15.9 mm, x in [-2.95, +12.95] rel to pin 1)
# J7: USB Type-C (width 10.64 mm, x in [-5.32, +5.32] rel to center)

# Let's test various y_cut values, e.g. 119.0, 120.0, 121.0, 122.0 mm:
for y_cut in [119.0, 120.0, 121.0, 122.0]:
    x_half = math.sqrt(35.0**2 - (y_cut - 100.0)**2)
    x_min = 100.0 - x_half
    x_max = 100.0 + x_half
    print(f"\n--- Y_CUT = {y_cut:.1f} mm: X in [{x_min:.2f}, {x_max:.2f}], width = {2*x_half:.2f} mm ---")
    
    # If front mating face of all connectors is aligned at Y_front = y_cut:
    # JST-XH: pin 1 is at y_pos = y_cut - 9.20. (Courtyard y_max = y_pos + 9.70 = y_cut + 0.50).
    # If courtyard is strictly <= y_cut: y_pos = y_cut - 9.70.
    # USB Type-C: center is at y_pos = y_cut - 3.68 (or y_cut - 4.18 for courtyard <= y_cut).
    
    # Let's test two configurations:
    # Config A: [J8 (3p), J7 (USB), J10 (5p), J9 (3p)]
    # Config B: [J8 (3p), J9 (3p), J7 (USB), J10 (5p)]
    # Config C: [J8 (3p), J10 (5p), J7 (USB), J9 (3p)]
    print(f"  Slot West: [{x_min:.2f} .. {84.444 - 2.45:.2f}] (width = {84.444 - 2.45 - x_min:.2f} mm)")
    print(f"  Slot Mid : [{84.444 + 2.45:.2f} .. {115.556 - 2.45:.2f}] (width = {115.556 - 84.444 - 4.90:.2f} mm)")
    print(f"  Slot East: [{115.556 + 2.45:.2f} .. {x_max:.2f}] (width = {x_max - (115.556 + 2.45):.2f} mm)")
