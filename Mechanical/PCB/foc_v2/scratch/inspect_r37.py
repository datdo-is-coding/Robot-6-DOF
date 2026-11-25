import re

with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for ref in ['R37', 'R38', 'R39', 'U8', 'Q7']:
    m = re.search(r'\(footprint\s+"([^"]+)".*?\(property\s+"Reference"\s+"' + ref + r'"\s*\).*?\(pad\s+"1"\s+[^\)]*\(net\s+[0-9]+\s+"([^"]+)"\).*?\(pad\s+"2"\s+[^\)]*\(net\s+[0-9]+\s+"([^"]+)"\)', text, re.DOTALL)
    if m:
        fp, net1, net2 = m.group(1), m.group(2), m.group(3)
        print(f"{ref}: {net1} <-> {net2}  ({fp})")
