import math

# Board parameters
cx, cy = 100.0, 100.0
R_board = 35.0
PCD_holes = 44.0
R_holes = 22.0

# Holes at 45 deg
delta_h = R_holes / math.sqrt(2) # 15.556 mm
holes = {
    "H_NW": (cx - delta_h, cy - delta_h), # (84.44, 84.44)
    "H_NE": (cx + delta_h, cy - delta_h), # (115.56, 84.44)
    "H_SW": (cx - delta_h, cy + delta_h), # (84.44, 115.56)
    "H_SE": (cx + delta_h, cy + delta_h), # (115.56, 115.56)
}

print("Mounting holes (PCD 44):")
for name, (hx, hy) in holes.items():
    print(f"  {name}: ({hx:.2f}, {hy:.2f})")

# Connectors:
# J7: Type-C, width ~ 9.0mm, depth ~ 7.5mm
# J8: CAN_IN, XH-3 cong, width 10.9mm (pitch 2.54, 3 pins = 5.08 + body ~ 9.9mm, CrtYd 10.9mm), depth 12.5mm
# J9: CAN_OUT, XH-3 cong, width 10.9mm, depth 12.5mm
# J10: SWD, XH-5 cong, width 15.9mm (pitch 2.54, 5 pins = 10.16 + body ~ 14.9mm, CrtYd 15.9mm), depth 12.5mm
# J11: 24V_IN, XT30PW-M, width 10.2mm, depth 14.5mm

# Let's explore flat cut options on Edge.Cuts:
# Option 1: Single flat cut at the bottom (South)
# For y_cut:
for y_cut in [128.0, 127.0, 126.0, 125.0, 124.0]:
    dy = y_cut - cy
    if dy < R_board:
        dx = math.sqrt(R_board**2 - dy**2)
        print(f"y_cut = {y_cut:.1f} mm: flat chord from x = {cx-dx:.1f} to {cx+dx:.1f} (flat width = {2*dx:.1f} mm)")

# Option 2: Symmetrical chamfers or dual flats:
# e.g., Bottom flat for Type-C (or Type-C + SWD), and Side flat or bottom-wide flat?
