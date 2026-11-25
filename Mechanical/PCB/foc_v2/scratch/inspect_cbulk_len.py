with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "C_BULK1"' in l:
        print(f"Reference line: {i}")
        for k in range(i, len(lines)):
            if lines[k].startswith('\t(footprint ') or lines[k].startswith('(footprint '):
                print(f"Next footprint at line {k}")
                break
        break
