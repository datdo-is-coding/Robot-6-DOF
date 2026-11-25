import math

# Let's explore how all 4 connectors (J8, J9, J7, J10) CAN fit in a straight line on the PCB.
# Let's check:
# Total width of the 4 connectors:
# J8: 9.9 mm
# J9: 9.9 mm
# J7: 8.94 mm (courtyard 10.64)
# J10: 14.9 mm
# Sum = 43.64 mm.
# With 0.5 mm spacing between them: 43.64 + 3 * 0.5 = 45.14 mm.
# With 1.0 mm spacing: 46.64 mm.

# What is the diameter of the board?
# Ø70 mm, R = 35.0 mm.
# Center: (100, 100).

# At what Y does a Ø70 mm circle have a width of at least 46.64 mm?
# dx = 46.64 / 2 = 23.32 mm.
# dy = sqrt(35.0^2 - 23.32^2) = sqrt(1225 - 543.82) = sqrt(681.18) = 26.10 mm.
# Y = 100 + 26.10 = 126.10 mm!

# Look at that:
# At Y = 126.10 mm, the circle width is 46.64 mm!
# At Y = 125.0 mm, the circle width is 48.99 mm!
# At Y = 124.0 mm, the circle width is 50.95 mm!

# Now let's check:
# Where are H1 and H2?
# H2 = (84.444, 115.556)
# H1 = (115.556, 115.556)
# What is the keepout around H1 and H2?
# The hole is 2.7 mm diameter. The screw head for M2.5 DIN 912 has head diameter 4.5 mm (radius 2.25 mm).
# An ISO 7089 washer has OD 5.0 mm (radius 2.5 mm).
# So the keepout radius is 2.5 mm to 2.7 mm!
print("Let's analyze the exact distance between connector pads/bodies and H1/H2 for various Y_cut and arrangements.")
