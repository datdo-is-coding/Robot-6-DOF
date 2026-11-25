with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for l in lines:
    if 'layer "Edge.Cuts"' in l or 'layer "Edge.Cuts")' in l:
        print(l.strip())
