import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for b in text.split('(footprint '):
    if '"H2"' in b:
        lines = b.splitlines()
        for i, l in enumerate(lines):
            if any(k in l for k in ['fp_circle', 'pad', 'center', 'end', 'size']):
                print(f"  {l.strip()}")
        break
