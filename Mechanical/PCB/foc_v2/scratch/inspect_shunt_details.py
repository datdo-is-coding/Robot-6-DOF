import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect pad absolute locations for Phase U shunts:
# Q2, R47, NT1, NT2, C1, R56
targets = ['Q2', 'R47', 'NT1', 'NT2', 'C1', 'R56', 'Q4', 'R48', 'NT3', 'NT4', 'C2', 'R58', 'Q6', 'R49', 'NT5', 'NT6', 'C3', 'R60']

fp_blocks = re.findall(r'\(footprint\s+.*?\n\t\)', content, re.DOTALL)
fps = {}
for b in fp_blocks:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', b)
    at_m = re.search(r'\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\)', b)
    if ref_m and at_m:
        ref = ref_m.group(1)
        if ref in targets:
            at = (float(at_m.group(1)), float(at_m.group(2)), float(at_m.group(3) or 0))
            pads = re.findall(r'\(pad\s+"?([^"\s]+)"?\s+([^\s]+)\s+.*?\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\).*?\(net\s+"([^"]*)"\)', b, re.DOTALL)
            fps[ref] = {'at': at, 'pads': pads}

for group, refs in [('Phase U Shunt', ['Q2', 'R47', 'NT1', 'NT2', 'C1', 'R56']),
                   ('Phase V Shunt', ['Q4', 'R48', 'NT3', 'NT4', 'C2', 'R58']),
                   ('Phase W Shunt', ['Q6', 'R49', 'NT5', 'NT6', 'C3', 'R60'])]:
    print(f"\n=== {group} ===")
    for ref in refs:
        if ref in fps:
            cx, cy, rot = fps[ref]['at']
            print(f" {ref:<5} at ({cx:.2f}, {cy:.2f}) rot {rot}:")
            for p in fps[ref]['pads']:
                dx, dy = float(p[2]), float(p[3])
                # compute absolute position based on rotation
                rad = rot * 3.1415926535 / 180.0
                import math
                ax = cx + dx * math.cos(rad) - dy * math.sin(rad)
                ay = cy + dx * math.sin(rad) + dy * math.cos(rad)
                print(f"    Pad {p[0]:<2} ({p[5]}): at ({ax:.3f}, {ay:.3f})")
