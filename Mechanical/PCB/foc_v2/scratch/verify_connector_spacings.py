import math

# Candidate coordinates:
# J8 (XH 3p): x=78.0, y=119.5
# J9 (XH 3p): x=89.0, y=119.5
# J7 (Type-C): x=100.0, y=121.2
# J10 (XH 5p): x=111.5, y=119.5

# Holes:
H_SW = (84.444, 115.556)
H_SE = (115.556, 115.556)
R_ko = 3.0 # keepout radius

print("=== Checking clearances to Screw Keepouts ===")
# J8 pads: x = 78.0 + [-2.5, 0, 2.5] = [75.5, 78.0, 80.5], y = 119.5
for pin, px in enumerate([75.5, 78.0, 80.5], 1):
    d = math.hypot(px - H_SW[0], 119.5 - H_SW[1])
    clearance = d - 0.85 - R_ko
    print(f"J8 pin {pin} ({px}, 119.5): dist to H_SW = {d:.3f} mm, copper clearance = {clearance:.3f} mm")

# J9 pads: x = 89.0 + [-2.5, 0, 2.5] = [86.5, 89.0, 91.5], y = 119.5
for pin, px in enumerate([86.5, 89.0, 91.5], 1):
    d = math.hypot(px - H_SW[0], 119.5 - H_SW[1])
    clearance = d - 0.85 - R_ko
    print(f"J9 pin {pin} ({px}, 119.5): dist to H_SW = {d:.3f} mm, copper clearance = {clearance:.3f} mm")

# J10 pads: x = 111.5 + [-5, -2.5, 0, 2.5, 5] = [106.5, 109.0, 111.5, 114.0, 116.5], y = 119.5
for pin, px in enumerate([106.5, 109.0, 111.5, 114.0, 116.5], 1):
    d = math.hypot(px - H_SE[0], 119.5 - H_SE[1])
    clearance = d - 0.85 - R_ko
    print(f"J10 pin {pin} ({px}, 119.5): dist to H_SE = {d:.3f} mm, copper clearance = {clearance:.3f} mm")

print("\n=== Checking J7 clearances ===")
# J7 shell pads are at ~ (100.0 +- 4.32, 121.2) = [95.68, 104.32]
print(f"J9 pin 3 to J7 left shell: {95.68 - 91.5:.2f} mm")
print(f"J7 right shell to J10 pin 1: {106.5 - 104.32:.2f} mm")
