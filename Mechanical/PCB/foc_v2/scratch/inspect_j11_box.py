import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = text.split('(footprint ')
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if ref_m and ref_m.group(1) == 'J11':
        lines = re.findall(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)', b)
        xs = [float(l[0]) for l in lines] + [float(l[2]) for l in lines]
        ys = [float(l[1]) for l in lines] + [float(l[3]) for l in lines]
        print(f"J11 lines: X in [{min(xs):.2f}, {max(xs):.2f}], Y in [{min(ys):.2f}, {max(ys):.2f}]")
        pads = re.findall(r'\(pad\s+"[^"]*"\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)', b)
        pxs = [float(p[0]) for p in pads]
        pys = [float(p[1]) for p in pads]
        print(f"J11 pads: X in [{min(pxs):.2f}, {max(pxs):.2f}], Y in [{min(pys):.2f}, {max(pys):.2f}]")
