import math

# Holes:
H_SW = (84.44, 115.56)
H_SE = (115.56, 115.56)
R_keepout = 3.0 # keepout radius

print("H_SW keepout x range:", H_SW[0] - R_keepout, "to", H_SW[0] + R_keepout)
print("H_SW keepout y range:", H_SW[1] - R_keepout, "to", H_SW[1] + R_keepout)
print("H_SE keepout x range:", H_SE[0] - R_keepout, "to", H_SE[0] + R_keepout)
print("H_SE keepout y range:", H_SE[1] - R_keepout, "to", H_SE[1] + R_keepout)

# Note: Between H_SW and H_SE:
# x from 87.44 to 112.56 mm is a 25.12 mm gap.
# West of H_SW: x from 75.5 to 81.44 is only 5.94 mm.
# East of H_SE: x from 118.56 to 124.5 is only 5.94 mm.
# SOUTH of H_SW and H_SE:
# y > 118.56 mm!
# If connectors are placed at y > 118.56 mm:
# For JST XH: pins at y_pin, body from y_pin - 2.81 to y_pin + 9.7.
# If y_pin = 120.0 mm:
#   Top of courtyard is y = 120.0 - 2.81 = 117.19 mm (overlaps keepout by 1.37 mm if x overlaps).
# If y_pin = 122.0 mm:
#   Top of courtyard is y = 122.0 - 2.81 = 119.19 mm > 118.56 mm!
# That means if y_pin >= 121.5 mm, the courtyard is ENTIRELY SOUTH OF THE SCREW HEAD KEEPOUT!
# And the mating face extends to y = 121.5 + 9.3 = 130.8 mm!
