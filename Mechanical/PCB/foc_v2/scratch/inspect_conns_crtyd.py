import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for ref in ['J8', 'J9', 'J10', 'J7']:
    for b in text.split('(footprint '):
        if f'"{ref}"' in b:
            lines = re.findall(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)', b)
            rects = re.findall(r'\(fp_rect\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)', b)
            xs = []
            ys = []
            for l in lines:
                xs.extend([float(l[0]), float(l[2])])
                ys.extend([float(l[1]), float(l[3])])
            for r in rects:
                xs.extend([float(r[0]), float(r[2])])
                ys.extend([float(r[1]), float(r[3])])
            print(f"{ref} CrtYd: X in [{min(xs) if xs else 0:.2f}, {max(xs) if xs else 0:.2f}], Y in [{min(ys) if ys else 0:.2f}, {max(ys) if ys else 0:.2f}]")
            break
