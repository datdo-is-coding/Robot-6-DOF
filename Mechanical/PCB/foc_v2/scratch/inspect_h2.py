import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"H2"', p)
    if ref_m:
        for line in p.split('\n'):
            if any(k in line for k in ['(fp_circle', '(center', '(end', 'F.CrtYd', 'pad']):
                print("  ", line.strip())
