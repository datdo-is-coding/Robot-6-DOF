with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "C_BULK1"' in l:
        start = i - 5
        for k in range(start, start + 200):
            if lines[k].startswith('\t)'):
                print(f"End at line {k}")
                break
            if 'CrtYd' in lines[k] or 'pad' in lines[k] or 'fp_' in lines[k]:
                print(lines[k].rstrip())
        break
