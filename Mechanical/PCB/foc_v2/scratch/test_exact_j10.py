import math

CX, CY = 100.0, 100.0
H3 = (84.44365, 84.44365)
H2 = (84.44365, 115.55635)
R_KO = 3.0

# J10 (XH 5p, rot=90 facing West):
# Pad 1 at (74.0, 102.0).
# In KiCad rot=90:
# Pad 1 is at (0, 0). Pad 5 at (10, 0) -> along Y from 102.0 to 112.0!
# Wait! Let's check the footprint relative to Pad 1:
# In rot=90:
# x range: [x_pin - 9.70, x_pin + 2.81]
# y range: [y_pin - 2.45, y_pin + 12.45]
# Let's test x_pin=75.0, y_pin=95.0:
# x in [65.3, 77.81]
# y in [92.55, 107.45]

xmin, xmax = 65.3, 77.81
ymin, ymax = 92.55, 107.45

max_r = max(math.hypot(px - 100, py - 100) for px in [xmin, xmax] for py in [ymin, ymax])
print(f"J10 max radius: {max_r:.2f} mm (Limit: 35.0) -> {'OK' if max_r <= 35.0 else 'FAIL'}")

cx3 = max(xmin, min(H3[0], xmax))
cy3 = max(ymin, min(H3[1], ymax))
d3 = math.hypot(cx3 - H3[0], cy3 - H3[1])
print(f"J10 distance to H3: {d3:.3f} mm (Limit: 3.0) -> {'OK' if d3 >= 3.0 else 'FAIL'}")

cx2 = max(xmin, min(H2[0], xmax))
cy2 = max(ymin, min(H2[1], ymax))
d2 = math.hypot(cx2 - H2[0], cy2 - H2[1])
print(f"J10 distance to H2: {d2:.3f} mm (Limit: 3.0) -> {'OK' if d2 >= 3.0 else 'FAIL'}")
