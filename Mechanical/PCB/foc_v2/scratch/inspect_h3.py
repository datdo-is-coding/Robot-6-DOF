with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "H3"' in l:
        for k in range(max(0, i-10), min(len(lines), i+30)):
            print(lines[k].rstrip())
        break
