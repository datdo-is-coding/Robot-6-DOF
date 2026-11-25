import math

# Test connector placement along flat cut Y = 123.5:
# Center of board: (100.0, 100.0)
# Flat cut: from (74.06, 123.5) to (125.94, 123.5)
# H2 = (84.444, 115.556), H1 = (115.556, 115.556)
# J7 at X = 100.0, y_orig = 119.71 (front face at 123.5)

# Connectors:
# J8 (3-pin): front at 123.5 => y_orig = 123.5 - 9.20 = 114.30.
#   Width: x_orig - 2.45 to x_orig + 7.45.
#   Pads at x_orig, x_orig + 2.5, x_orig + 5.0.
# J9 (3-pin): front at 123.5 => y_orig = 114.30.
#   Width: x_orig - 2.45 to x_orig + 7.45.
#   Pads at x_orig, x_orig + 2.5, x_orig + 5.0.
# J10 (5-pin): front at 123.5 => y_orig = 114.30.
#   Width: x_orig - 2.45 to x_orig + 12.45.
#   Pads at x_orig, x_orig + 2.5, x_orig + 5.0, x_orig + 7.5, x_orig + 10.0.

# Notice:
# At y_orig = 114.30, pads are at Y = 114.30.
# Distance to H2 Y (115.556) is |114.30 - 115.556| = 1.256 mm.
# Distance to H1 Y (115.556) is 1.256 mm.

# So for ANY pad to avoid H2 (center 84.444, drill 2.7mm):
# We need hypot(pad_x - 84.444, 114.30 - 115.556) >= pad_radius + hole_radius + clearance
# Pad is oval 1.7x1.7 (radius 0.85). Hole radius 1.35. Clearance 0.2.
# Total dist >= 0.85 + 1.35 + 0.2 = 2.40 mm!
# Since dy = 1.256 mm:
# dx >= sqrt(2.40^2 - 1.256^2) = sqrt(5.76 - 1.58) = sqrt(4.18) = 2.05 mm!
# So any pad must have |pad_x - 84.444| >= 2.05 mm!
# That means NO pad can be in [82.39 .. 86.50]!
# And similarly for H1: NO pad can be in [113.50 .. 117.61]!

print("Pad exclusion zones: [82.39 .. 86.50] and [113.50 .. 117.61]")
