with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

crtyd_lines = []
for k in range(23490, 25600):
    if '(layer "F.CrtYd")' in lines[k]:
        # print surrounding
        for m in range(k-6, k+3):
            print(lines[m].rstrip())
        print("...")
        if len(crtyd_lines) > 5:
            break
        crtyd_lines.append(k)
