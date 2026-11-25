with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for k in range(23490, 25600):
    if '(layer "F.CrtYd")' in lines[k]:
        start = k
        while start > 23490 and not lines[start].startswith('\t\t(fp_'):
            start -= 1
        end = k
        while end < 25600 and not lines[end].startswith('\t\t)'):
            end += 1
        for m in range(start, end+1):
            print(lines[m].rstrip())
        break
