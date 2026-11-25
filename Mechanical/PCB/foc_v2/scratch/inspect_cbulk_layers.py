with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "C_BULK1"' in l:
        start = i - 5
        curr = ""
        for k in range(start, start + 300):
            if lines[k].startswith('\t)'):
                break
            if '(fp_' in lines[k]:
                curr = lines[k].strip()
            if '(layer ' in lines[k]:
                print(curr, lines[k].strip())
            if '(pad ' in lines[k]:
                print(lines[k].strip())
        break
