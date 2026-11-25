with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re

def get_fp(ref_name):
    pos = 0
    while True:
        idx = text.find('(footprint ', pos)
        if idx == -1: break
        depth = 0
        end = idx
        for i in range(idx, len(text)):
            if text[i] == '(': depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        fp_text = text[idx:end]
        if f'(property "Reference" "{ref_name}"' in fp_text:
            return fp_text
        pos = end
    return None

connectors = ['J7', 'J8', 'J9', 'J10', 'J11', 'J1', 'J2', 'J3', 'H1', 'H2', 'H3', 'H4', 'U1', 'IC1']
for c in connectors:
    fp = get_fp(c)
    if fp:
        m_fp = re.search(r'\(footprint\s+"([^"]+)"', fp)
        fp_name = m_fp.group(1) if m_fp else "unknown"
        # find crtyd lines
        crtyd = re.findall(r'\(fp_rect\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\).*?\(layer\s+"[FB]\.CrtYd"\)', fp)
        if not crtyd:
            crtyd = re.findall(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\).*?\(layer\s+"[FB]\.CrtYd"\)', fp)
        print(f"=== {c}: {fp_name} ===")
        if crtyd:
            xs = [float(p[0]) for p in crtyd] + [float(p[2]) for p in crtyd]
            ys = [float(p[1]) for p in crtyd] + [float(p[3]) for p in crtyd]
            print(f"  Local Courtyard: X in [{min(xs):.2f}, {max(xs):.2f}] (w={max(xs)-min(xs):.2f}), Y in [{min(ys):.2f}, {max(ys):.2f}] (h={max(ys)-min(ys):.2f})")
        # pads count and bounds
        pads = re.findall(r'\(pad\s+"[^"]*"\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)', fp)
        print(f"  Pads count: {len(pads)}")
