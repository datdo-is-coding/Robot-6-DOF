import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for b in text.split('(footprint '):
    if '"H2"' in b:
        # print full fp_circle and pad
        circles = re.findall(r'\(fp_circle\s+[\s\S]*?\)', b)
        for c in circles:
            print("Circle:", c)
        pad = re.search(r'\(pad\s+[\s\S]*?\)', b)
        if pad:
            print("Pad:", pad.group(0))
        break
