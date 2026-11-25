with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'layer "Edge.Cuts"' in l:
        for j in range(max(0, i-4), min(len(lines), i+8)):
            print(lines[j].rstrip())
        print("---")
