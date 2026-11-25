import re
import math

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse all footprints with their bounding boxes and pads
# In KiCad 8+:
# (footprint "..." (layer "...") (uuid "...") (at X Y [ROT]) ... (property "Reference" "REF") ...)

fps = []
blocks = text.split('(footprint ')
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    fp_name = b.split()[0].strip('"')
    layer_m = re.search(r'\(layer "([^"]+)"\)', b)
    layer = layer_m.group(1) if layer_m else "F.Cu"
    at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
    x = float(at_m.group(1))
    y = float(at_m.group(2))
    rot = float(at_m.group(3)) if at_m.group(3) else 0.0
    val_m = re.search(r'\(property "Value" "([^"]+)"', b)
    val = val_m.group(1) if val_m else ""
    
    # get all pads
    pads = re.findall(r'\(pad\s+"([^"]*)"\s+(\w+)\s+(\w+)\s+\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)\s+\(size\s+([-\d.]+)\s+([-\d.]+)\)', b)
    # get courtyard lines/rects
    crtyd_lines = re.findall(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)', b)
    crtyd_rects = re.findall(r'\(fp_rect\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)', b)
    crtyd_circles = re.findall(r'\(fp_circle\s+\(center\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)', b)
    
    fps.append({
        'ref': ref,
        'val': val,
        'fp': fp_name,
        'layer': layer,
        'x': x,
        'y': y,
        'rot': rot,
        'pads': pads,
        'crtyd_lines': crtyd_lines,
        'crtyd_rects': crtyd_rects,
        'crtyd_circles': crtyd_circles
    })

print(f"Parsed {len(fps)} footprints successfully.")

# Check which footprints have pads or courtyards with distance from (100, 100) > 35.0
print("\n--- Footprints extending outside Circle R = 35.0 mm ---")
outside_circle = []
for fp in fps:
    # check footprint center
    d_center = math.hypot(fp['x'] - 100, fp['y'] - 100)
    # check pads
    rad = math.radians(fp['rot'])
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    max_pad_r = 0.0
    for p in fp['pads']:
        px, py = float(p[3]), float(p[4])
        # transform pad to world
        wx = fp['x'] + px * cos_a - py * sin_a
        wy = fp['y'] + px * sin_a + py * cos_a
        pr = math.hypot(wx - 100, wy - 100)
        if pr > max_pad_r:
            max_pad_r = pr
    if max_pad_r > 34.5 or d_center > 34.0:
        outside_circle.append((fp['ref'], fp['val'], fp['x'], fp['y'], max_pad_r, d_center))

for item in outside_circle:
    print(f"  {item[0]:8s} ({item[1]:15s}): at ({item[2]:.2f}, {item[3]:.2f}), max_pad_r={item[4]:.2f}, center_r={item[5]:.2f}")
