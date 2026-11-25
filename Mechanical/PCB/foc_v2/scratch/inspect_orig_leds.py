with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for it in ['D1', 'D2', 'D3', 'R33', 'R35', 'R36']:
        if f'(property "Reference" "{it}"' in l:
            for k in range(i-6, i+5):
                if lines[k].strip().startswith('(at '):
                    print(it, lines[k].strip())
