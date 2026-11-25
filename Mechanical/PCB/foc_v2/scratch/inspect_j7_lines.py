import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if ref_m and ref_m.group(1) == 'J7':
        for line in block.split('\n'):
            if any(k in line for k in ['fp_line', 'fp_rect', 'layer']):
                print(line.strip())
