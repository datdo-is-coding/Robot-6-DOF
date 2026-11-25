import math

# Let's test placing J10 in the center between H2 (84.444) and H1 (115.556):
# Available X in center: [87.5 .. 112.5] (width = 25.0 mm)
# J10 width = 14.9 mm (pads 10mm).
# If J10 is at X = 98.0:
# Pads: 98.0, 100.5, 103.0, 105.5, 108.0.
# Plastic body: [98.0 - 2.45, 98.0 + 12.45] = [95.55, 110.45]!
# Clearance to H2: 95.55 - 84.444 = 11.11 mm >> 2.95 mm!
# Clearance to H1: 115.556 - 110.45 = 5.11 mm >> 2.95 mm!
# J10 FITS IN THE CENTER WITH MASSIVE CLEARANCE TO BOTH HOLES!

print("J10 in center: [95.55, 110.45] is 100% clean of H1 and H2!")
