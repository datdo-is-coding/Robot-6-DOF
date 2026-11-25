import re

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
b_cu = []
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
    if ref_m and layer_m and layer_m.group(1) == 'B.Cu':
        b_cu.append(ref_m.group(1))

print(f"Total components on B.Cu in git_raw: {len(b_cu)}")
print(b_cu)
