import math

# Verification of real physical envelopes:
# M2.5 screw head: R = 2.25 mm
# J7 shell: X in [-4.47, +4.47] rel to center
# J8, J9 shell: X in [-2.45, +7.45] rel to pin 1
# J10 shell: X in [-2.45, +12.45] rel to pin 1

# Positions:
# H2 = (84.444, 115.556)
# H1 = (115.556, 115.556)
# J8:  X_pin1 = 74.00,  Y_pin1 = 110.30
# J7:  X_center = 92.25, Y_center = 115.82
# J10: X_pin1 = 100.25, Y_pin1 = 110.30
# J9:  X_pin1 = 121.00, Y_pin1 = 110.30

# Physical X ranges:
j8_x = (74.00 - 2.45, 74.00 + 7.45)   # [71.55, 81.45]
j7_x = (92.25 - 4.47, 92.25 + 4.47)   # [87.78, 96.72]
j10_x = (100.25 - 2.45, 100.25 + 12.45) # [97.80, 112.70]
j9_x = (121.00 - 2.45, 121.00 + 7.45) # [118.55, 128.45]

print("=== REAL PHYSICAL BOUNDS & GAPS ===")
print(f"J8  X: [{j8_x[0]:.2f}, {j8_x[1]:.2f}]")
print(f"Gap J8 to H2 screw head (84.444 - 2.25 = 82.194): {82.194 - j8_x[1]:.3f} mm")
print(f"Gap H2 screw head (84.444 + 2.25 = 86.694) to J7: {j7_x[0] - 86.694:.3f} mm")
print(f"J7  X: [{j7_x[0]:.2f}, {j7_x[1]:.2f}]")
print(f"Gap J7 to J10: {j10_x[0] - j7_x[1]:.3f} mm")
print(f"J10 X: [{j10_x[0]:.2f}, {j10_x[1]:.2f}]")
print(f"Gap J10 to H1 screw head (115.556 - 2.25 = 113.306): {113.306 - j10_x[1]:.3f} mm")
print(f"Gap H1 screw head (115.556 + 2.25 = 117.806) to J9: {j9_x[0] - 117.806:.3f} mm")
print(f"J9  X: [{j9_x[0]:.2f}, {j9_x[1]:.2f}]")

print("\n=== DISTANCE TO BOARD EDGE (R = 35.0 mm at center 100, 100) ===")
# Outer corners of J8 and J9:
d_j8 = math.hypot(j8_x[0] - 100.0, 119.50 - 100.0)
d_j9 = math.hypot(j9_x[1] - 100.0, 119.50 - 100.0)
print(f"J8 outer corner dist to center: {d_j8:.3f} mm (limit 35.000 mm, margin = {35.0 - d_j8:.3f} mm)")
print(f"J9 outer corner dist to center: {d_j9:.3f} mm (limit 35.000 mm, margin = {35.0 - d_j9:.3f} mm)")
