with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\(gr_[a-z]+\s+[\s\S]*?\(layer\s+"Edge\.Cuts"\)[\s\S]*?\)', text)
print(f"Matches on Edge.Cuts: {len(matches)}")
for m in matches:
    print(m)
