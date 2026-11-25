import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

targets = ['IC1', 'R1', 'R2', 'R3', 'R4', 'R5', 'R7', 'R55', 'R56', 'R57', 'R58', 'R59', 'R60', 'NT1', 'NT2', 'NT3', 'NT4', 'NT5', 'NT6', 'C1', 'C2', 'C3']

fp_blocks = re.findall(r'\(footprint\s+.*?\n\t\)', content, re.DOTALL)
fps = {}
for b in fp_blocks:
    m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', b)
    if m:
        ref = m.group(1)
        if ref in targets:
            at_m = re.search(r'\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\)', b)
            at = (float(at_m.group(1)), float(at_m.group(2)), float(at_m.group(3) or 0)) if at_m else None
            pads = re.findall(r'\(pad\s+"?([^"\s]+)"?\s+([^\s]+)\s+.*?\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\).*?\(net\s+"([^"]*)"\)', b, re.DOTALL)
            fps[ref] = {'at': at, 'pads': pads}

for ref in sorted(fps.keys()):
    pos = fps[ref]['at']
    print(f"\n{ref} at ({pos[0]:.2f}, {pos[1]:.2f}) rot {pos[2]}:")
    for p in fps[ref]['pads']:
        print(f"   Pad {p[0]}: rel({p[2]}, {p[3]}) net '{p[5]}'")
