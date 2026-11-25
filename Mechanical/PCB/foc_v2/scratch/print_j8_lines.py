import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = text.split('(footprint ')
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if ref_m and ref_m.group(1) == 'J8':
        lines = b.splitlines()
        for l in lines:
            if any(k in l for k in ['fp_line', 'pad', 'model']):
                print(l.strip()[:100])
