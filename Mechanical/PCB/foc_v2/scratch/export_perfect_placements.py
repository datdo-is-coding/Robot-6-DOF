import sys
sys.path.append('scratch')
from verify_exact_boxes import boxes

print(f"Total boxed components: {len(boxes)}")

# We need all 124 components: 120 from boxes + 4 mounting holes H1..H4
placements = {}

# 4 Mounting holes:
placements["H3"] = (84.444, 84.444, 0, "both")
placements["H4"] = (115.556, 84.444, 0, "both")
placements["H2"] = (84.444, 115.556, 0, "both")
placements["H1"] = (115.556, 115.556, 0, "both")

for k, b in boxes.items():
    placements[k] = (b['x'], b['y'], b['rot'], b['layer'])

print(f"Total placements: {len(placements)} / 124")

with open('scratch/perfect_placements.py', 'w', encoding='utf-8') as f:
    f.write("# Master perfect placement dictionary for all 124 components\n")
    f.write("placements = {\n")
    for k, v in sorted(placements.items()):
        f.write(f"    '{k}': ({v[0]:.4f}, {v[1]:.4f}, {v[2]}, '{v[3]}'),\n")
    f.write("}\n")

print("Wrote scratch/perfect_placements.py successfully!")
