import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# find all footprints and their references
pattern = re.compile(r'\(footprint\s+"([^"]+)"[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"')
matches = pattern.findall(text)
fp_map = {ref: fp for fp, ref in matches}

for ref in sorted(fp_map.keys()):
    if ref in ['H1', 'H2', 'H3', 'H4', 'J1', 'J2', 'J3', 'J7', 'J8', 'J9', 'J10', 'J11', 'IC1', 'U1', 'U2', 'C_BULK1', 'C63']:
        print(f"{ref:8s}: {fp_map[ref]}")
