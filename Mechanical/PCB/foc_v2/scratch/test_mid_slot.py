import math

# Circle: center (100, 100), R = 35.0
# Holes: H1(115.556, 115.556), H2(84.444, 115.556)
h1_x, h1_y = 115.556, 115.556
h2_x, h2_y = 84.444, 115.556

# What if Y_cut is 120.0 vs 121.0 vs 122.0 vs 123.0?
# Notice: as Y_cut increases (moves South), does the connector move further away from H1/H2?
# YES! Because H1 and H2 are at Y = 115.556!
# If Y_cut = 123.0 mm:
# The pin row of XH is at Y = 123.0 - 9.31 = 113.69 mm!
# The front of XH is at Y = 123.0 mm!
# The rear of XH is at Y = 123.0 - 11.72 = 111.28 mm!
# At Y = 115.556, the connector body is present.

# Let's check: What if the connectors are:
# J8 (CAN_IN 3-pin)
# J9 (CAN_OUT 3-pin)
# J7 (Type-C)
# J10 (SWD 5-pin)
# Can J8 and J9 both be to the left of H2?
# Width of J8 + J9 = 10.12 + 10.12 = 20.24 mm!
# To the left of H2: at Y_cut=120, X goes to 71.28.
# 84.44 - 71.28 = 13.16 mm. So two connectors don't fit to the left of H2.

# What about:
# 1 connector West of H2: (J8 or J9)
# 2 connectors between H2 and H1:
# 1 connector East of H1: (J9 or J8)
# If 1 West, 2 Mid, 1 East:
# West must be 3-pin XH (width 10.12).
# East must be 3-pin XH (width 10.12).
# Mid must be Type-C (width 10.64) AND 5-pin XH (width 15.12).
# Let's check if Type-C and 5-pin XH can fit between H2 and H1!
# Distance between H2 and H1 is 115.556 - 84.444 = 31.112 mm!

dist_h = 115.556 - 84.444
print(f"Distance between H2 and H1 centers: {dist_h:.3f} mm")
