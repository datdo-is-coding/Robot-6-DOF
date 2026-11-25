with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for it in ['L1', 'D4', 'C16', 'C17', 'R53', 'R54']:
        if f'(property "Reference" "{it}"' in l:
            for k in range(i-6, i+5):
                if lines[k].strip().startswith('(at '):
                    print(it, lines[k].strip())
