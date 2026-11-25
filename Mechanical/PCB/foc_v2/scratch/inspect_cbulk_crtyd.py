with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "C_BULK1"' in l:
        for k in range(i+20, min(len(lines), i+80)):
            if 'CrtYd' in lines[k]:
                for m in range(k-2, k+10):
                    print(lines[m].rstrip())
        break
