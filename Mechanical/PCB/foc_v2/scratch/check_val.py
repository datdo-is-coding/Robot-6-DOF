with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for ref in ['R45', 'R46', 'JP1', 'D4', 'F1']:
    m = re.search(r'\(property "Reference" "' + ref + r'".*?\(property "Value" "([^"]+)"', text, flags=re.DOTALL)
    val = m.group(1) if m else "?"
    print(f"{ref}: {val}")
