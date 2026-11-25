with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "TP1"' in l:
        for k in range(i-6, i+30):
            print(lines[k].rstrip())
        break
