with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

import re
m = re.search(r'\(footprint [^\n]+Reference "J10"[\s\S]*?\n\t\)', pcb)
if not m:
    m = re.search(r'\(footprint [^\n]+Reference "J10"[\s\S]*?\n  \)', pcb)
if m:
    pads = re.findall(r'\(pad "[0-9]+"[^\)]*?\((?:net \d+ "[^"]*")?\)', m.group(0))
    for p in pads:
        print(p)
else:
    # let's just find lines around Reference "J10"
    lines = pcb.splitlines()
    for i, l in enumerate(lines):
        if 'Reference "J10"' in l:
            for j in range(i, min(len(lines), i+40)):
                print(lines[j])
            break
