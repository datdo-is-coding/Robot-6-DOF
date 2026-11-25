with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for k in range(995, 1015):
    print(k+1, lines[k].rstrip())
