import re

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
P_raw = {}
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m:
        ref = ref_m.group(1)
        layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
        at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', p)
        x = float(at_m.group(1))
        y = float(at_m.group(2))
        rot = float(at_m.group(3)) if at_m.group(3) else 0.0
        P_raw[ref] = (x, y, rot, layer_m.group(1))

print(f"Total components in git_raw: {len(P_raw)}")
for r in ['H1', 'H2', 'H3', 'H4', 'J8', 'J9', 'J7', 'J10', 'J1', 'J2', 'J3', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']:
    print(f"{r:5s}: {P_raw[r]}")
