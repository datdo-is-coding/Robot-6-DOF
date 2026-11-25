import math

# Holes PCD 44:
delta = 22.0 / math.sqrt(2)
H3 = (100 - delta, 100 - delta) # 84.444, 84.444
H4 = (100 + delta, 100 - delta) # 115.556, 84.444
H2 = (100 - delta, 100 + delta) # 84.444, 115.556
H1 = (100 + delta, 100 + delta) # 115.556, 115.556

print("Holes:")
print("H3 (NW):", H3)
print("H4 (NE):", H4)
print("H2 (SW):", H2)
print("H1 (SE):", H1)

# Notice:
# 1. Between H2 (84.444) and H1 (115.556):
# Distance between centers = 31.11 mm.
# Clearance between keepouts (r=3.0) = 31.11 - 6.0 = 25.11 mm!
# The corridor between H2 and H1 is x in [87.45, 112.55]!
# Width of this corridor is 25.1 mm!

# 2. What about BELOW H2 and H1?
# H2 and H1 keepout ends at y = 115.556 + 3.0 = 118.556!
# Below y = 118.56, what is the available x span on the board?
for y in range(119, 134):
    dy = y - 100
    if dy < 35:
        dx = math.sqrt(35**2 - dy**2)
        print(f"y={y}: x in [{100-dx:.2f}, {100+dx:.2f}], width={2*dx:.2f} mm")
