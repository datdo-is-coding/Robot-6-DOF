with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '"Reference" "C54"' in l:
        for j in range(i+90, i+130):
            if j < len(lines):
                print(lines[j].rstrip())
        break
