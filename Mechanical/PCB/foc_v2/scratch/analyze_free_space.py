import math

# Let's map the board space:
# Circle: (100, 100), R = 35.0 mm.
# South flat cut: Y = 125.0 mm.

# Where are the components?
# Top: MOSFETs Q1..Q6 at Y = 75.8, X in [83.5 .. 116.5]
# Motor pads J1, J2, J3 at Y = 69.5
# DC Bus caps C_BUS1,2,3 at Y = 70.0
# Bulk caps: C_BULK1 at (77, 85), C63 at (124, 84)
# Gate driver IC1 at (100, 93.5)
# MCU U1 at (100, 111.5)
# Mounting holes:
# H3 (84.44, 84.44)
# H4 (115.56, 84.44)
# H2 (84.44, 115.56)
# H1 (115.56, 115.56)

# Look at where there is space:
# 1. Left of MCU U1 (West, between H3 and H2):
#    X in [72 .. 82], Y in [92 .. 110]!
#    In the original layout, CAN was at (74, 100) and (74, 115)!
#    Near the middle West edge, radius from (100, 100) at Y = 100 is:
#    At Y = 100, circle goes to X = 65.0!
#    So between X = 72 and 82 at Y = 95..108, the circle has width from 65 to 84!
#    THAT IS A 19 MM WIDE BY 15 MM HIGH EMPTY MEADOW!
#    AND WHAT DID THE PREVIOUS AGENT DO?
#    They pushed CAN down to Y = 118..126 where the circle narrows to 74!
#    Instead of putting it at Y = 98..108 where the circle is 65!

# 2. Right of MCU U1 (East, between H4 and H1):
#    At Y = 100, the circle goes to X = 135!
#    H4 is at (115.56, 84.44), H1 is at (115.56, 115.56).
#    Between X = 118 and 133 at Y = 95..110:
#    THAT IS A 15 MM WIDE BY 15 MM HIGH REGION!
#    XT30 J11, Fuse F1, and Diode D6 can sit right there at Y = 98..108!
#    Inside X = 118..132, Y = 98..108!
#    Distance to center: at X = 125, Y = 104:
#    r = sqrt(25^2 + 4^2) = 25.3 mm!
#    WELL INSIDE 35.0 MM (almost 10 mm of margin to the circular edge)!

print("EUREKA! The board has massive open space at East and West mid-sections (Y in [95..110])!")
