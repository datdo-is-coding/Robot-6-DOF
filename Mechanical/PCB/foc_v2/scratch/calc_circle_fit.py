import math

cx, cy, r = 100.0, 100.0, 35.0

print("Circle width at different Y:")
for y in range(110, 134, 2):
    dy = y - cy
    if dy < r:
        dx = math.sqrt(r**2 - dy**2)
        w = 2 * dx
        print(f"Y = {y:2d}: dy = {dy:4.1f}, X in [{cx-dx:5.2f}, {cx+dx:5.2f}], width = {w:5.2f} mm")
