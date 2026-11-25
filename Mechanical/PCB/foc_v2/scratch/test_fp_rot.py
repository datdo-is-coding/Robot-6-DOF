# Test exact transformation of JST-XH 5-pin at rot=90 in KiCad:
# Pad 1 is at local (0, 0).
# Pad 5 is at local (10, 0).
# In KiCad:
# If footprint is at (X0, Y0) with rotation rot:
# pad_x = X0 + local_x * cos(rot) - local_y * sin(rot)
# pad_y = Y0 + local_x * sin(rot) + local_y * cos(rot)

import math

def kicad_transform(x0, y0, rot_deg, lx, ly):
    rad = math.radians(rot_deg)
    return (
        x0 + lx * math.cos(rad) - ly * math.sin(rad),
        y0 + lx * math.sin(rad) + ly * math.cos(rad)
    )

print("J10 with rot=90, placed at (76.5, 95.0):")
print("Pad 1:", kicad_transform(76.5, 95.0, 90, 0, 0))
print("Pad 5:", kicad_transform(76.5, 95.0, 90, 10, 0))
# Courtyard corners: (-2.95, -2.81) to (12.95, 9.70)
c1 = kicad_transform(76.5, 95.0, 90, -2.95, -2.81)
c2 = kicad_transform(76.5, 95.0, 90, 12.95, 9.70)
print("CrtYd corners:", c1, c2)
print("X span:", min(c1[0], c2[0]), max(c1[0], c2[0]))
print("Y span:", min(c1[1], c2[1]), max(c1[1], c2[1]))
