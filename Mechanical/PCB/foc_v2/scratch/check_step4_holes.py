with open("scratch/clean_step4.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
holes = re.findall(r'\(property\s+"Reference"\s+"(H\d+)"[\s\S]*?\(at\s+([0-9.-]+)\s+([0-9.-]+)', text)
print("Holes in clean_step4:")
for h, x, y in holes:
    print(f"  {h}: at ({x}, {y})")

# Also let's check all mounting hole footprints:
fps = re.findall(r'\(footprint\s+"MountingHole[^\"]*"[\s\S]*?\(at\s+([0-9.-]+)\s+([0-9.-]+)', text)
print("Mounting hole footprints:")
for x, y in fps:
    print(f"  at ({x}, {y})")
