import math

H2 = (84.44365, 115.55635)
H1 = (115.55635, 115.55635)
R_KO = 3.0

# Connectors:
# J8: CAN_IN (XH 3p: w=9.9, h=12.51, pad 1 to pad 3 = 5.0)
# J9: CAN_OUT (XH 3p: w=9.9, h=12.51)
# J7: USB-C (w=8.94, h=8.5, mouth at +3.75, back at -4.75)
# J10: SWD (XH 5p: w=14.9, h=12.51, pad 1 to pad 5 = 10.0)

# Let's test if we can place them along X so none of them hit H2 or H1.
# Specifically, check the corridor between H2 and H1: [87.5, 112.5] (width 25.0 mm).
# Can 2 connectors be in the corridor, one to the left of H2, one to the right of H1?
# Let's test:
# Left of H2: X < 81.44.
# Right of H1: X > 118.56.
# Inside corridor: 87.45 < X < 112.55.

# Left connector (e.g. J8 or J10):
# If J8 (w=9.9) is to the left of H2:
# X range of J8: [x_left, x_right] <= 81.44 => x_right <= 81.44.
# If x_right = 81.0, then x_left = 81.0 - 9.9 = 71.1.
# At x_left = 71.1, y_front = 123.0:
# Is (71.1, 123.0) inside the circle R=35?
d1 = math.hypot(71.1 - 100, 123.0 - 100)
print(f"Corner of J8 at (71.1, 123.0): distance to center = {d1:.2f} (R=35.0)")

# And at y_back = 123.0 - 12.51 = 110.49:
d2 = math.hypot(71.1 - 100, 110.49 - 100)
print(f"Back corner of J8 at (71.1, 110.49): distance to center = {d2:.2f} (R=35.0)")
