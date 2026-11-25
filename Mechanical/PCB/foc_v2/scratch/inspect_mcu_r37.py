with open('MCU.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for ref in ['R37', 'R38', 'R39']:
    idx = text.find(f'"{ref}"')
    if idx != -1:
        snippet = text[max(0, idx-200):min(len(text), idx+600)]
        print(f"=== {ref} ===")
        print(snippet)
