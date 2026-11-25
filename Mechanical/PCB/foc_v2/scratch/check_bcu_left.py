import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

fps = re.split(r'\n\t\(footprint ', text)
print("=== B.Cu components with X < 95 ===")
for fp in fps[1:]:
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', fp)
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp)
    at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', fp)
    if not (ref_m and layer_m and at_m):
        continue
    ref = ref_m.group(1)
    layer = layer_m.group(1)
    x, y = float(at_m.group(1)), float(at_m.group(2))
    if layer == 'B.Cu' and x < 95:
        print(f"B.Cu {ref:<8} at ({x:6.2f}, {y:6.2f})")
