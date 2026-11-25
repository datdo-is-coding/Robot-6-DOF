with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for u in ['U8', 'Q7', 'R40', 'R41', 'R42', 'R43', 'C59']:
        if f'(property "Reference" "{u}"' in l:
            for k in range(i-6, i+5):
                if lines[k].strip().startswith('(at '):
                    print(u, lines[k].strip())
