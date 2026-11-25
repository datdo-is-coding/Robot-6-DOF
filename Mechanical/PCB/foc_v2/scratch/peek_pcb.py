with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "D4"' in l or '(property "Reference" "JP1"' in l:
        print("".join(lines[max(0, i-10):min(len(lines), i+25)]))
