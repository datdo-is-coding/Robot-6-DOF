import math

# Test Option 1: Bottom straight bank of 4 connectors (CAN_IN, CAN_OUT, Type-C, SWD)
# Widths (courtyard):
# CAN_IN (XH-3): 10.9 mm, x-span 10.9 mm
# CAN_OUT (XH-3): 10.9 mm
# Type-C: 9.0 mm
# SWD (XH-5): 15.9 mm
# Total width = 10.9 + 1.5 + 10.9 + 1.5 + 9.0 + 1.5 + 15.9 = 50.7 mm.
# Centered around x = 100 mm:
# x goes from 100 - 50.7/2 = 74.65 mm to 100 + 50.7/2 = 125.35 mm.

# Let's check distance to circle at y = 126 mm:
# At y = 126 mm, dy = 26 mm. R = 35 mm.
# dx_circle = sqrt(35^2 - 26^2) = sqrt(1225 - 676) = sqrt(549) = 23.43 mm -> x from 76.57 to 123.43 mm.
# If y_cut = 124 mm:
# dy = 24 mm. dx_circle = sqrt(1225 - 576) = sqrt(649) = 25.47 mm -> x from 74.53 to 125.47 mm.
# Total flat width = 50.95 mm!

print(f"Flat cut at y = 124 mm has width {2*25.47:.2f} mm.")
print("Fits 4 connectors perfectly with 50.7 mm total width!")

# What if J11 (XT30) is replaced with XH-2 cong (2-pin)?
# XH-2 cong width = 8.4 mm.
# If all 5 were: XT30 (10.2) + CAN_IN (10.9) + CAN_OUT (10.9) + Type-C (9.0) + SWD (15.9) = 57.9 + 4*1.5 = 63.9 mm.
# For 63.9 mm width, dy = sqrt(35^2 - (63.9/2)^2) = sqrt(1225 - 1020.8) = sqrt(204.2) = 14.29 mm.
# That means y = 100 + 14.29 = 114.29 mm, which directly clashes with H_SW and H_SE at y = 115.56 mm!
