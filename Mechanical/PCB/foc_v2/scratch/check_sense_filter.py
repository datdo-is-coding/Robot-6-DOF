with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for ref in ['R37', 'R38', 'R39', 'C54', 'C55', 'C56']:
    m = re.search(r'\(property\s+"Reference"\s+"' + ref + r'".*?\(pad\s+"1"\s+[^\)]*\(net\s+"([^"]+)"\)', text, re.DOTALL)
    if m:
        print(f"{ref} Pad 1 net: {m.group(1)}")
    m2 = re.search(r'\(property\s+"Reference"\s+"' + ref + r'".*?\(pad\s+"2"\s+[^\)]*\(net\s+"([^"]+)"\)', text, re.DOTALL)
    if m2:
        print(f"{ref} Pad 2 net: {m2.group(1)}")
