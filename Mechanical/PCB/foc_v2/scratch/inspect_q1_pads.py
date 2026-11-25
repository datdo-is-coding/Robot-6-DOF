with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "Q1"' in l:
        start = i - 5
        for k in range(start, start + 300):
            if lines[k].startswith('\t)'): break
            if '(pad "' in lines[k]:
                print(lines[k].strip(), lines[k+1].strip())
        break
