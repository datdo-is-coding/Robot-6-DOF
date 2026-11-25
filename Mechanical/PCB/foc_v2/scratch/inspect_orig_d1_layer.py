with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "D1"' in l:
        for k in range(i-6, i+5):
            if lines[k].strip().startswith('(layer '):
                print("D1 layer:", lines[k].strip())
