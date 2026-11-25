with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "J11"' in l:
        start = i - 5
        for k in range(start, start + 300):
            if lines[k].startswith('\t)'): break
            if 'CrtYd' in lines[k]:
                for m in range(k-6, k):
                    if '(start ' in lines[m] or '(end ' in lines[m]:
                        print(lines[m].strip())
        break
