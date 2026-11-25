import re
with open('foc_v2.kicad_pcb', 'r') as f:
    text = f.read()

for b in text.split('(footprint '):
    if '"J11"' in b:
        m = re.search(r'\(model\s+[\s\S]*?\n\t\t\)', b)
        if m:
            print(m.group(0))
