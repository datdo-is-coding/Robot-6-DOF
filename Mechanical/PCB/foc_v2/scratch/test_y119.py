import math

cx, cy = 100.0, 100.0
r_board = 35.0
h1_x, h1_y = 115.556, 115.556
h2_x, h2_y = 84.444, 115.556
hole_r = 2.95

y_cut = 119.0

# Connectors:
# Zone 1 (Left of H2): J8 (CAN_IN)
# Zone 2 (Center): J7 (Type-C) + J10 (SWD)
# Zone 3 (Right of H1): J9 (CAN_OUT)

# Wait: in Zone 2: J7 (width 10.64) + J10 (width 15.51) = 26.15 mm > 25.1 mm.
# But what if Zone 2 has:
# J7 (Type-C, width 10.64) + J8 (CAN_IN, width 10.51) = 21.15 mm!
# And Zone 1 has J10 (SWD)?
# Wait, J10 width is 15.51 mm. Can 15.51 mm fit in Zone 1?
# No, 15.51 in Zone 1 extends to 81.4 - 15.51 = 65.89 -> R = 37.8 mm (outside).

# What if J10 (SWD) is in Zone 2 (Center)?
# And J8 (CAN_IN) is in Zone 1?
# And J9 (CAN_OUT) is in Zone 3?
# Where does J7 (Type-C) go?
# Can J7 (Type-C) go in Zone 1? Width is 10.64.
# 81.4 - 10.64 = 70.76. At y=119: sqrt(29.24^2 + 19^2) = 34.87 mm < 35.0 mm!
# YES! J7 FITS IN ZONE 1!
# What about J9 in Zone 3? Width is 10.51.
# 118.6 + 10.51 = 129.11. At y=119: sqrt(29.11^2 + 19^2) = 34.76 mm < 35.0 mm!
# YES! J9 FITS IN ZONE 3!
# And what about Zone 2 (Center)?
# In Zone 2: J8 (CAN_IN, width 10.51) AND J10 (SWD, width 15.51)?
# 10.51 + 15.51 = 26.02 mm > 25.1 mm.

print("Testing connector combinations at y_cut = 119.0...")
