import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for b in text.split('(footprint '):
    if '"H2"' in b:
        for line in b.splitlines()[30:60]:
            print(" ", line)
        break
