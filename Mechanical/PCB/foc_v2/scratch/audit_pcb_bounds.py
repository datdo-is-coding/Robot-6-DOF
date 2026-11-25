import re
import math

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Check Edge.Cuts elements
edge_elements = re.findall(r'\(gr_(?:line|arc)\s+[\s\S]*?\(layer\s+"Edge\.Cuts"\)[\s\S]*?\)', text)
print(f"Total Edge.Cuts elements: {len(edge_elements)}")
for e in edge_elements:
    start_m = re.search(r'\(start ([-\d.]+) ([-\d.]+)\)', e)
    end_m = re.search(r'\(end ([-\d.]+) ([-\d.]+)\)', e)
    mid_m = re.search(r'\(mid ([-\d.]+) ([-\d.]+)\)', e)
    typ = "arc" if "gr_arc" in e else "line"
    print(f"  {typ:4s}: start=({start_m.group(1)}, {start_m.group(2)}) end=({end_m.group(1)}, {end_m.group(2)})" + (f" mid=({mid_m.group(1)}, {mid_m.group(2)})" if mid_m else ""))

# Check any footprint with center radius > 34.0 mm
blocks = text.split('(footprint ')
outside = []
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if not ref_m: continue
    ref = ref_m.group(1)
    at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)', b)
    x, y = float(at_m.group(1)), float(at_m.group(2))
    r = math.hypot(x - 100, y - 100)
    if r > 34.5 or y > 123.5:
        outside.append((ref, x, y, r))

print(f"\nFootprints exceeding bounds (r > 34.5 or y > 123.5): {len(outside)}")
for o in outside:
    print(f"  {o[0]:8s}: at ({o[1]:.2f}, {o[2]:.2f}), r={o[3]:.2f}")
