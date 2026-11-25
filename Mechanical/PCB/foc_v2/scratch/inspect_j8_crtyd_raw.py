import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for b in text.split('(footprint '):
    if '"J8"' in b:
        lines = re.findall(r'\(fp_[a-z]+\s+[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)[\s\S]*?\)', b)
        for l in lines:
            print("CrtYd item:", l)
        break
