import math

h1_x, h1_y = 115.556, 115.556
h2_x, h2_y = 84.444, 115.556

# Let's test Y_cut = 120.0
# py_xh = 120.0 - 9.31 = 110.69
# py_typec = 120.0 - 4.18 = 115.82 (or 116.0)

# What if:
# J7 (Type-C) is at X_center = 92.30
# J10 (SWD 5-pin) is at X_pin1 = 100.20
# Let's check:
# J7 box:
# X in [92.30 - 5.32, 92.30 + 5.32] = [86.98, 97.62]
# Y in [115.82 - 4.85, 115.82 + 4.18] = [110.97, 120.00]
# Distance from J7 box to H2(84.444, 115.556):
# Closest point on J7 box is (86.98, 115.556).
# d_H2 = 86.98 - 84.444 = 2.536 mm!
# 2.536 mm > 2.45 mm (and > 2.50 mm)! PASSED!

# J10 box:
# Pin 1 at X = 100.20
# X in [100.20 - 2.56, 100.20 + 12.56] = [97.64, 112.76]
# Y in [110.69 - 2.41, 110.69 + 9.31] = [108.28, 120.00]
# Distance between J7 right edge (97.62) and J10 left edge (97.64):
# gap = 97.64 - 97.62 = 0.02 mm (or with slight adjustment, 0.05 mm)
# Distance from J10 box to H1(115.556, 115.556):
# Closest point on J10 box is (112.76, 115.556).
# d_H1 = 115.556 - 112.76 = 2.796 mm!
# 2.796 mm > 2.45 mm! PASSED!

print("J7 clearance to H2:", 86.98 - 84.444)
print("J10 clearance to H1:", 115.556 - 112.76)
print("Gap between J7 and J10:", 97.64 - 97.62)
