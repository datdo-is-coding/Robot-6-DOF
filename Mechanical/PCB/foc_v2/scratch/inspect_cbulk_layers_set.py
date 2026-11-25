with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

layers = set()
for k in range(23496, 25600):
    if '(layer ' in lines[k]:
        layers.add(lines[k].strip())
print("Layers in C_BULK1:", layers)
