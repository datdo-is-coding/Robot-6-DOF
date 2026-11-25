with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for ref in ['R45', 'R46', 'JP1', 'U9', 'D4']:
    m = re.search(r'\(footprint "[^"]+".*?\(property "Reference" "' + ref + r'".*?\n\t\)', text, flags=re.DOTALL)
    if m:
        print(f"=== {ref} ===")
        for block in re.findall(r'\(fp_line.*?\n\t\t\)', m.group(0), flags=re.DOTALL):
            if 'CrtYd' in block:
                print(" ", " ".join(block.split()))
