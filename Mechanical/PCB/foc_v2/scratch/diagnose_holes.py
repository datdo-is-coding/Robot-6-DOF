import math

holes = [(115.556, 115.556), (84.444, 115.556)]
# Total width of all 4 connectors = 10.51 + 10.51 + 10.64 + 15.51 = 47.17 mm
# + 3 gaps of 0.8 mm = 47.17 + 2.4 = 49.57 mm!
# If centered at x=100.0:
# Leftmost x = 100 - 49.57/2 = 75.215 mm
# Rightmost x = 100 + 49.57/2 = 124.785 mm
# Now check the span:
# From x=75.215 to x=124.785:
# Does this span cover H2 (84.444) and H1 (115.556)?
# YES! Because 75.215 < 84.444, and 124.785 > 115.556!
# That means H2 and H1 are INSIDE the connector span!
print("H2 x=84.444 and H1 x=115.556 are INSIDE the connector span!")
print(f"H2 keepout is [{84.444-2.95:.2f}, {84.444+2.95:.2f}] = [81.49, 87.39]")
print(f"H1 keepout is [{115.556-2.95:.2f}, {115.556+2.95:.2f}] = [112.61, 118.51]")
