import math

# Let's test the exact conditions under which 4 connectors (J8, J9, J7, J10) can be placed in a straight line facing South.
# Connectors:
# J8: 3-pin XH (width 9.9mm, depth 11.5mm, crtyd 10.9 x 12.5)
# J9: 3-pin XH (width 9.9mm, depth 11.5mm, crtyd 10.9 x 12.5)
# J7: USB-C (width 8.94mm, depth 7.5mm, crtyd 10.64 x 9.03)
# J10: 5-pin XH (width 14.9mm, depth 11.5mm, crtyd 15.9 x 12.5)

# Mounting holes:
# H2 = (84.444, 115.556), r = 2.95
# H1 = (115.556, 115.556), r = 2.95

# Let's check:
# If the connectors are placed in a row at Y_front = y_f:
# For J8, J9, J10:
# y_origin = y_f - 9.20
# y_crtyd_min = y_origin - 2.81 = y_f - 12.01
# y_crtyd_max = y_origin + 9.70 = y_f + 0.50
# For J7:
# y_origin = y_f - 3.79
# y_crtyd_min = y_origin - 4.85 = y_f - 8.64
# y_crtyd_max = y_origin + 4.18 = y_f + 0.39

# Notice:
# For H2 (84.444, 115.556) and H1 (115.556, 115.556), the crtyd circle is [112.61 .. 118.51] in Y.
# When does y_crtyd_min of J8, J9, J10 become > 118.51?
# y_f - 12.01 >= 118.51  ===>  y_f >= 130.52!

# But at y_f = 130.52, the circle width is only 34 mm!
# What if y_f is SMALLER, e.g. y_f = 123.5 or 124.0 or 125.0?
# Then y_crtyd overlaps the Y-band [112.61 .. 118.51] of H1 and H2!
# And in that Y-band, H2 is at X = 84.444 and H1 is at X = 115.556!
# That means NO connector can have its crtyd covering [81.5 .. 87.4] or [112.6 .. 118.5]!

# Now, let's see what happens if a connector is placed:
# In the center: between H2 and H1!
# Available X span in the center: [87.4 .. 112.6] -> width = 25.2 mm!
# What can fit in 25.2 mm?
# J7 (10.64 mm) + J9 (10.9 mm) = 21.54 mm!
# With 1.5 mm gap: 23.04 mm < 25.2 mm!
# So TWO connectors can easily fit in the center!
# But what about the other two connectors?
# Can one connector be to the left of H2 (X < 81.5)?
# To the left of H2, X is in [x_left_edge .. 81.5].
# How wide is [x_left_edge .. 81.5]?
# At Y = 120: circle R = 35 => dy = 20 => dx = sqrt(35^2 - 20^2) = 28.72 => x_left = 100 - 28.72 = 71.28.
# 81.5 - 71.28 = 10.22 mm!
# At Y = 118: dy = 18 => dx = sqrt(35^2 - 18^2) = 29.98 => x_left = 70.02.
# 81.5 - 70.02 = 11.48 mm!
# At Y = 116: dy = 16 => dx = sqrt(35^2 - 16^2) = 31.12 => x_left = 68.88.
# 81.5 - 68.88 = 12.62 mm!

# LOOK AT THAT!
# At Y = 116 .. 118, the width to the left of H2 is 11.5 .. 12.6 mm!
# And J8 courtyard is 10.90 mm wide!
# 10.90 mm < 12.62 mm!
# IT CAN FIT TO THE LEFT OF H2!
print("Wait! Why did the previous test say it didn't fit?")
