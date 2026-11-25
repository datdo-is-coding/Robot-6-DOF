with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for ref in ['C14', 'R61']:
    pos = text.find(f'"{ref}"')
    if pos != -1:
        start = text.rfind('(footprint ', 0, pos)
        end = text.find('(property "Value"', pos)
        print(ref, text[start:end])
