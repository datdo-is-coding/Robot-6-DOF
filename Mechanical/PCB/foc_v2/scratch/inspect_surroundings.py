import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect all parts around X in [70, 82], Y in [90, 105] on F.Cu
# And all parts around X in [110, 130], Y in [85, 115] on B.Cu
fps = re.split(r'\n\t\(footprint ', text)

print("=== F.Cu parts in CAN area (X: 70..82, Y: 90..105) ===")
for fp in fps[1:]:
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', fp)
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp)
    at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', fp)
    if not (ref_m and layer_m and at_m):
        continue
    ref = ref_m.group(1)
    layer = layer_m.group(1)
    x, y = float(at_m.group(1)), float(at_m.group(2))
    if layer == 'F.Cu' and 68 <= x <= 85 and 88 <= y <= 112:
        print(f"F.Cu {ref:<8} at ({x:6.2f}, {y:6.2f})")

print("\n=== B.Cu parts in Right area (X: 110..130, Y: 80..115) ===")
for fp in fps[1:]:
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', fp)
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp)
    at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', fp)
    if not (ref_m and layer_m and at_m):
        continue
    ref = ref_m.group(1)
    layer = layer_m.group(1)
    x, y = float(at_m.group(1)), float(at_m.group(2))
    if layer == 'B.Cu' and 105 <= x <= 135 and 75 <= y <= 120:
        print(f"B.Cu {ref:<8} at ({x:6.2f}, {y:6.2f})")
