# South bank layout optimization
# Available X space between Edge.Cuts at y=124: x from 75.5 to 124.5 (49 mm total)
# Screw holes:
# H2 (SW): (84.444, 115.556), keepout radius = 3.0 mm (D = 6.0 mm)
# H1 (SE): (115.556, 115.556), keepout radius = 3.0 mm (D = 6.0 mm)

# Connectors:
# J8: CAN_IN (XH 3p, width 9.9 mm, 3 pins at -2.5, 0, +2.5)
# J9: CAN_OUT (XH 3p, width 9.9 mm, 3 pins at -2.5, 0, +2.5)
# J7: USB-C (GT-USB-7010ASV, width 8.94 mm)
# J10: SWD (XH 5p, width 14.9 mm, 5 pins at -5, -2.5, 0, +2.5, +5)

# Notice:
# J8 and J9 are CAN bus in/out daisy chain! They should definitely be right next to each other!
# For CAN daisy chaining, having J8 and J9 side by side allows trace routing of CAN_H and CAN_L straight through with 0 mm stub!
# J7 is USB Type-C in the center (x = 100).
# J10 is SWD (5 pins).

# Arrangement A: [J8, J9] [J7] [J10]
# Can J8 and J9 be on the West?
# If J8 is at x=78, J9 is at x=89:
# Notice H2 is at x=84.444! H2 is right in the middle between x=78 and x=89!
# That means J8 is left of H2, and J9 is right of H2!
# And what about H1 (x=115.556)?
# If J10 is at x=105 to 110, then J10 is LEFT of H1!
# Let's test if J10 fits entirely between J7 and H1!
# If J7 is at x=98.0:
# J7 right edge is at 98.0 + 4.5 = 102.5 mm.
# H1 left keepout is at 115.556 - 3.0 = 112.556 mm.
# Gap between J7 and H1 keepout is: 112.556 - 102.5 = 10.05 mm!
# J10 width is 14.9 mm, so J10 cannot fit in 10 mm.

# What if Arrangement B:
# What if J10 is placed in the CENTER?
# Or what if connectors are:
# J8 (CAN_IN): x = 80.0
# J9 (CAN_OUT): x = 90.0
# J10 (SWD): x = 101.5 (centered!)
# J7 (USB-C): x = 113.0 or 114.0?
# USB-C width is only 8.94 mm!
# If J7 is at x=114.0, let's check its clearance to H1!
print("Testing Arrangement B: J8 (80), J9 (90), J10 (100.5), J7 (112.5)")
