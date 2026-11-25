import math

# Check geometric clearance with mounting holes
# H_SW is at (84.44, 115.56)
# H_SE is at (115.56, 115.56)
# Keepout circle has radius 3.0mm, so H_SW keepout reaches:
#   x up to 84.44 + 3.0 = 87.44 mm
#   y up to 115.56 + 3.0 = 118.56 mm
# H_SE keepout reaches:
#   x down to 115.56 - 3.0 = 112.56 mm
#   y up to 115.56 + 3.0 = 118.56 mm

# If connectors are placed at y > 118.56 mm (say y = 120 to 128 mm):
# Let's check available width between the circle arcs at y = 122 mm:
cy = 100.0
cx = 100.0
R = 35.0

for y in [120, 122, 124, 126, 128, 130]:
    dy = y - cy
    if dy < R:
        dx = math.sqrt(R*R - dy*dy)
        print(f"At y={y}mm: circle width = {2*dx:.1f}mm (from x={cx-dx:.1f} to {cx+dx:.1f})")

