with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for tp in ['TP1', 'TP2', 'TP3']:
        if f'(property "Reference" "{tp}"' in l:
            for k in range(i-6, i+25):
                if '(net ' in lines[k]:
                    print(tp, lines[k].strip())
