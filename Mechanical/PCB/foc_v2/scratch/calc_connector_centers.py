import math

# Target flat cut at y = 122.5 mm
cy = 100.0
cx = 100.0
R = 35.0
y_cut = 122.5

dy = y_cut - cy # 22.5 mm
dx = math.sqrt(R*R - dy*dy) # 26.87 mm
x_start = cx - dx # 73.13 mm
x_end = cx + dx   # 126.87 mm
flat_w = 2 * dx   # 53.74 mm

print(f"South flat cut at y = {y_cut} mm: width = {flat_w:.2f} mm (from x = {x_start:.2f} to {x_end:.2f})")

# 4 Connectors:
# J8: CAN_IN (XH-3): width 10.9 mm
# J9: CAN_OUT (XH-3): width 10.9 mm
# J7: USB-C: width 9.0 mm
# J10: SWD (XH-5): width 15.9 mm
# Total width = 46.7 mm

# Let's space them across flat_w = 53.74 mm:
# Spacing margin = (53.74 - 46.7) / 5 = 1.4 mm padding on ends, ~1.8 mm between connectors.
# Let's calculate center x of each:
# 1. J8 (CAN_IN):
#    Courtyard width 10.9 mm.
#    Let x_j8_center = 79.5 mm.
#    Courtyard: [74.05, 84.95]. (Leaves 0.9 mm to board edge 73.13)
# 2. J9 (CAN_OUT):
#    Courtyard width 10.9 mm.
#    Let x_j9_center = 91.5 mm.
#    Courtyard: [86.05, 96.95]. (Gap to J8 = 91.5 - 5.45 - 84.95 = 1.1 mm)
# 3. J7 (USB-C):
#    Courtyard width 9.0 mm.
#    Centered at x = 100.0 mm! (Exact center of board!)
#    Courtyard: [95.5, 104.5]. (Wait, overlaps J9 if J9 is at 91.5. Let's recalculate!)

# Let's optimize centers:
# J7 (Type-C) at x = 100.0 (width 9.0 -> [95.5, 104.5])
# Left of J7: available [74.0, 95.0] = 21.0 mm for J8 + J9!
# J8 (10.9) + J9 (10.9) = 21.8 mm -> tight by 0.8 mm if J7 is exactly at 100.
# What if J7 is at 102.0 or order is:
# Order: J8 (CAN_IN), J9 (CAN_OUT), J7 (USB-C), J10 (SWD)
# Total width:
# J8: 10.9, J9: 10.9, J7: 9.0, J10: 15.9.
# Let's find centers c1, c2, c3, c4 with equal gap g:
w1, w2, w3, w4 = 10.9, 10.9, 9.0, 15.9
total_w = w1 + w2 + w3 + w4
avail = 52.0 # available width from 74.0 to 126.0
gap = (avail - total_w) / 3 # gap between connectors
print(f"Gap between connectors = {gap:.2f} mm")

c1 = 74.0 + w1/2
c2 = c1 + w1/2 + gap + w2/2
c3 = c2 + w2/2 + gap + w3/2
c4 = c3 + w3/2 + gap + w4/2
print(f"c1 (J8  CAN_IN ): x = {c1:.2f} mm")
print(f"c2 (J9  CAN_OUT): x = {c2:.2f} mm")
print(f"c3 (J7  USB-C  ): x = {c3:.2f} mm")
print(f"c4 (J10 SWD    ): x = {c4:.2f} mm")
