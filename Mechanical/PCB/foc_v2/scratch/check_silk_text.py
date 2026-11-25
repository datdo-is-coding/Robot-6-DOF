with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\(gr_text\s+"([^"]+)".*?\(layer "([^"]+)"\)', text, flags=re.DOTALL)
for t, l in matches:
    if 'PCD' in t or 'FOC' in t or 'D70' in t:
        print(f"Layer {l}: {t}")
