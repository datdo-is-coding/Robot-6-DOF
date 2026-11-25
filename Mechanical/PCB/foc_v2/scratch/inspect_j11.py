import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"J11"', p)
    if ref_m:
        print(p[:500])
