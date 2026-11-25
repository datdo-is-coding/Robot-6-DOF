with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "U1"' in l:
        for k in range(i-6, i+5):
            if lines[k].strip().startswith('(at '):
                print("U1 orig:", lines[k].strip())
