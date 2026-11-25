import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'\(gr_(?:line|arc|circle) .*?layer "Edge\.Cuts".*?\)', text, re.DOTALL):
    print(m.group(0))
