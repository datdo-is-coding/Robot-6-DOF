with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']:
        if f'(property "Reference" "{q}"' in l:
            for k in range(i-6, i+5):
                if lines[k].strip().startswith('(at '):
                    print(q, lines[k].strip())
