import re

text = open('foc_v2.kicad_pcb', 'r', encoding='utf-8').read()
blocks = re.findall(r'\(gr_(?:line|arc)[\s\S]*?\(layer "Edge\.Cuts"\)[\s\S]*?\)', text)
print(f"Total Edge.Cuts elements: {len(blocks)}")
for b in blocks:
    print(b.strip())
