with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for j in ['J7', 'J8', 'J9', 'J10', 'J11']:
    m = re.search(r'\(footprint "([^"]+)".*?\(property "Reference" "' + j + r'"', text, flags=re.DOTALL)
    if m:
        print(f"{j}: {m.group(1)}")
