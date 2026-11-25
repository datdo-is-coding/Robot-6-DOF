import math

CX, CY = 100.0, 100.0
R = 35.0

# 1. North arc from West cut to East cut:
# West cut is at x = 66.5.
# Intersection of x = 66.5 with circle (x - 100)^2 + (y - 100)^2 = 35^2:
# (66.5 - 100)^2 = (-33.5)^2 = 1122.25.
# (y - 100)^2 = 1225 - 1122.25 = 102.75.
# y - 100 = +/- sqrt(102.75) = +/- 10.1366.
# y_nw = 100 - 10.1366 = 89.8634 mm.
# y_sw = 100 + 10.1366 = 110.1366 mm.

# East cut is at x = 133.5 (or 134.0):
# If x = 133.5:
# (133.5 - 100)^2 = 33.5^2 = 1122.25.
# y_ne = 100 - 10.1366 = 89.8634 mm.
# y_se = 100 + 10.1366 = 110.1366 mm.

# South cut is at y = 131.5 (or 132.0):
# If y = 131.5:
# (y - 100)^2 = 31.5^2 = 992.25.
# (x - 100)^2 = 1225 - 992.25 = 232.75.
# x - 100 = +/- sqrt(232.75) = +/- 15.256.
# x_sw = 100 - 15.256 = 84.744 mm.
# x_se = 100 + 15.256 = 115.256 mm.

# Wait, look at the South connectors:
# J8 left edge is 83.05 mm!
# If South cut is at y = 132.0:
# The straight line can connect from (x_sw, y_sw) to (x_south_left, y_south) to (x_south_right, y_south) to (x_se, y_se)!
# Let's check how nice chamfers/arcs look between the cuts!
print("Calculated points:")
print(f"West top: (66.5, {89.86:.2f})")
print(f"West bottom: (66.5, {110.14:.2f})")
print(f"East top: (133.5, {89.86:.2f})")
print(f"East bottom: (133.5, {110.14:.2f})")
