with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(17480, 17540):
    print(lines[i].rstrip())
