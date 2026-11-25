import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

# Holes PCD 44:
delta = 22.0 / math.sqrt(2)
HOLES = {
    "H3": (100 - delta, 100 - delta), # (84.444, 84.444)
    "H4": (100 + delta, 100 - delta), # (115.556, 84.444)
    "H2": (100 - delta, 100 + delta), # (84.444, 115.556)
    "H1": (100 + delta, 100 + delta), # (115.556, 115.556)
}
R_KO = 3.0

# Can J8 (3p), J9 (3p), J10 (5p) fit along the West side (rot=90, facing West)?
# In JST-XH horizontal:
# rot=0: faces South (+Y).
# rot=90: faces West (-X).
# If facing West (rot=90):
# Pad 1 is at (X, Y).
# Front of shroud is at X - 9.70 (towards West).
# Back of connector is at X + 2.81 (towards East).
# Width (in Y) for 3p: 9.9 mm (from Y - 2.45 to Y + 7.45).
# Width (in Y) for 5p: 14.9 mm (from Y - 2.45 to Y + 12.45).

# Total height in Y: 9.9 + 9.9 + 14.9 + 2*2 = 38.7 mm.
# Can a 38.7 mm vertical bank fit on the West side?
# West side: between H3 (y=84.44) and H2 (y=115.56):
# Distance in Y between H3 and H2 is 31.11 mm.
# Keepout Y is [81.44, 87.44] and [112.56, 118.56].
# To the left of H3 and H2: X < 81.44.
# What is the board circle at X = 75.0?
# Y span is 100 +- sqrt(35^2 - 25^2) = 100 +- 24.5 = [75.5, 124.5] (height 49.0 mm)!
# If X is to the left of H3 and H2 (say X = 77.0):
# X is OUTSIDE the keepouts of H3 and H2 (keepouts are at X in [81.44, 87.44])!
# The distance from X=77.0 to H3/H2 center is 84.44 - 77.0 = 7.44 mm > 3.0 mm!
# So for ANY Y, if X <= 78.0, IT NEVER TOUCHES H3 OR H2!

print("Testing West bank (rot=90, facing West):")
# Front at X_front = 70.0 (or 68.0).
# Pins at X_pin = X_front + 9.70 = 78.0.
# Back of shroud at X_back = 78.0 + 2.81 = 80.81 < 81.44 (H2/H3 keepout)!
# Check Y span for 3 connectors: J8, J9, J10:
# Total height = 9.9 + 2.0 + 9.9 + 2.0 + 14.9 = 38.7 mm.
# Centered at Y=100: Y from 100 - 19.35 = 80.65 to 100 + 19.35 = 119.35!
# Let's check circle radius at corners:
corners = [
    (70.0, 80.65), (70.0, 119.35), (80.81, 80.65), (80.81, 119.35)
]
for x, y in corners:
    d = math.hypot(x - CX, y - CY)
    print(f"Corner ({x}, {y}): distance to center = {d:.2f} (R=35.0)")
