with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "J11"' in l:
        start = i - 5
        for k in range(start, start + 300):
            if lines[k].startswith('\t)'): break
            if 'CrtYd' in lines[k]:
                for m in range(k-4, k+3):
                    print(lines[m].rstrip())
        break
