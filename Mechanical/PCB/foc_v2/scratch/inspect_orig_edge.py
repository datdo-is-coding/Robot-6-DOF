with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(layer "Edge.Cuts")' in l:
        for k in range(max(0, i-5), min(len(lines), i+40)):
            print(lines[k].rstrip())
        break
