import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

edges = re.findall(r'\(gr_\w+[^\)]*?\(layer\s+["\']?Edge\.Cuts["\']?\)[^\)]*\)', text)
print(f'Total Edge.Cuts elements: {len(edges)}')
for e in edges:
    print(' ', e.strip())
