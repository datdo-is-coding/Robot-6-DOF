import math

def kicad_transform(x0, y0, rot_deg, lx, ly):
    rad = math.radians(rot_deg)
    return (
        x0 + lx * math.cos(rad) + ly * math.sin(rad),
        y0 - lx * math.sin(rad) + ly * math.cos(rad)
    )

print("J10 (S5B) at (76.5, 95.0): local front is ly = +9.7")
for rot in [0, 90, 180, 270]:
    front = kicad_transform(76.5, 95.0, rot, 0, 9.7)
    back = kicad_transform(76.5, 95.0, rot, 0, -2.81)
    print(f"rot = {rot:3d}: front=({front[0]:.1f}, {front[1]:.1f}), back=({back[0]:.1f}, {back[1]:.1f})")
