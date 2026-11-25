with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '"Reference" "C54"' in l:
        for j in range(i, i+50):
            print(lines[j].rstrip())
        break
