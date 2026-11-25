import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by (footprint
blocks = text.split('(footprint ')
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    if ref in ['J7', 'J8', 'J9', 'J10', 'J11', 'H1', 'H2', 'H3', 'H4', 'J1', 'J2', 'J3', 'U1', 'IC1', 'U2']:
        fp_name = b.split()[0].strip('"')
        val_m = re.search(r'\(property "Value" "([^"]+)"', b)
        val = val_m.group(1) if val_m else ""
        at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
        layer_m = re.search(r'\(layer "([^"]+)"\)', b)
        print(f"{ref:5s} | {val:15s} | fp={fp_name:40s} | at=({at_m.group(1)}, {at_m.group(2)}) rot={at_m.group(3)} | layer={layer_m.group(1)}")
