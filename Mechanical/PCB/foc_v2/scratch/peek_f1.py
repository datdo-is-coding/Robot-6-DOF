with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "F1"' in l or '(property "Reference" "U9"' in l:
        print("".join(lines[max(0, i-10):min(len(lines), i+30)]))
