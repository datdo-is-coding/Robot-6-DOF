with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for tp in ['TP1', 'TP2', 'TP3']:
        if f'(property "Reference" "{tp}"' in l:
            for k in range(i-6, i+5):
                if lines[k].strip().startswith('(at '):
                    print(tp, lines[k].strip())
