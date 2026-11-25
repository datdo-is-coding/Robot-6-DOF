import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = text.split('(footprint ')
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    if ref in ['J7', 'J8', 'J9', 'J10', 'J11']:
        print(f"=== {ref} ===")
        # find all pads
        pads = re.findall(r'\(pad\s+"([^"]+)"\s+(\w+)\s+(\w+)\s+\(at\s+([-\d.]+)\s+([-\d.]+)', b)
        print("  Pads count:", len(pads))
        xs = [float(p[3]) for p in pads]
        ys = [float(p[4]) for p in pads]
        if xs and ys:
            print(f"  Pad bounds (relative): X in [{min(xs):.2f}, {max(xs):.2f}], Y in [{min(ys):.2f}, {max(ys):.2f}]")
        # find crtyd lines
        crtyd = re.findall(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)\s+\(stroke[^)]+\)\s+\(layer\s+"[FB]\.CrtYd"\)', b)
        c_xs = []
        c_ys = []
        for cl in crtyd:
            c_xs.extend([float(cl[0]), float(cl[2])])
            c_ys.extend([float(cl[1]), float(cl[3])])
        if c_xs and c_ys:
            print(f"  CrtYd bounds (relative): X in [{min(c_xs):.2f}, {max(c_xs):.2f}], Y in [{min(c_ys):.2f}, {max(c_ys):.2f}]")
        # find silk lines/rects to understand connector opening/orientation
        silk = re.findall(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)\s+\(stroke[^)]+\)\s+\(layer\s+"[FB]\.SilkS"\)', b)
        s_xs = []
        s_ys = []
        for sl in silk:
            s_xs.extend([float(sl[0]), float(sl[2])])
            s_ys.extend([float(sl[1]), float(sl[3])])
        if s_xs and s_ys:
            print(f"  SilkS bounds (relative): X in [{min(s_xs):.2f}, {max(s_xs):.2f}], Y in [{min(s_ys):.2f}, {max(s_ys):.2f}]")
