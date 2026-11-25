import math

H1 = (115.556, 115.556)
R_ko = 3.0

# H1 keepout boundary is all points (x, y) with (x - 115.556)^2 + (y - 115.556)^2 <= 3.0^2 = 9.0
# The maximum Y of the keepout is 115.556 + 3.0 = 118.556 mm.
print("Maximum Y of H1 keepout:", H1[1] + R_ko)

# For J10 at x=112.5, y=121.5:
# Pin 5 is at (117.5, 121.5)
# Pad size: oval 1.7 x 1.95 (radius in Y = 0.975 mm)
# Top edge of pad 5 copper:
pad_top_y = 121.5 - 0.975
print("Top edge of J10 pad 5 copper:", pad_top_y)
print("Clearance from pad 5 copper to keepout max Y:", pad_top_y - (H1[1] + R_ko))

# Distance from pad 5 center (117.5, 121.5) to H1 center:
d = math.hypot(117.5 - H1[0], 121.5 - H1[1])
print(f"Distance from pad 5 center to H1 center: {d:.3f} mm")
print(f"Clearance from pad 5 edge (0.975 mm) to screw keepout (3.0 mm): {d - 0.975 - 3.0:.3f} mm")

# What about the plastic body?
# Top of plastic body is at y = 121.5 - 2.45 = 119.05 mm
print("Top of plastic body:", 121.5 - 2.45)
print("Clearance from plastic body to screw keepout max Y:", (121.5 - 2.45) - (H1[1] + R_ko))
