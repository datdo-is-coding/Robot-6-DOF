import re

content = open('foc_v2.kicad_pcb', 'r', encoding='utf-8').read()
blocks = re.findall(r'\(gr_(?:line|arc)\n(?:\s+\([^\n]+\n)+', content)
for b in blocks:
    if 'Edge.Cuts' in b:
        print(b.strip())
