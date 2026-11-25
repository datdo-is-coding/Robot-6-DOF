import re
with open('foc_v2.kicad_pcb', 'r') as f:
    text = f.read()

for ref in ['U9', 'C60', 'C61', 'C62', 'R45', 'R46', 'JP1', 'F1', 'D6']:
    for b in text.split('(footprint '):
        if f'"{ref}"' in b:
            at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
            layer_m = re.search(r'\(layer "([^"]+)"\)', b)
            print(f"{ref:4s}: at ({at_m.group(1):>6s}, {at_m.group(2):>6s}) rot={str(at_m.group(3)):>5s} layer={layer_m.group(1)}")
            break
