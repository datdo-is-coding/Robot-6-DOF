with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "H3"' in l:
        for k in range(i+20, min(len(lines), i+80)):
            if lines[k].startswith('\t)'):
                print(lines[k].rstrip())
                break
            print(lines[k].rstrip())
        break
