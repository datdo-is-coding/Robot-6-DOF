import re
import math

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for ref in ['J1', 'J2', 'J3', 'H1', 'H2', 'H3', 'H4']:
    for b in text.split('(footprint '):
        if f'"{ref}"' in b:
            at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
            x, y = float(at_m.group(1)), float(at_m.group(2))
            r = math.hypot(x - 100, y - 100)
            print(f"{ref:4s}: at ({x:.2f}, {y:.2f}), dist_center={r:.2f}")
            break
