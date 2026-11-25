import re, math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Extract placements
placements = {}
for ref, lines in fps.items():
    layer = 'F.Cu'
    for l in lines[:15]:
        if '(layer "' in l:
            m = re.search(r'\(layer "([^"]+)"\)', l)
            if m: layer = m.group(1)
    for l in lines:
        if l.strip().startswith('(at '):
            m = re.search(r'\(at\s+([-0-9.]+)\s+([-0-9.]+)(?:\s+([-0-9.]+))?\)', l)
            if m:
                x = float(m.group(1))
                y = float(m.group(2))
                rot = float(m.group(3)) if m.group(3) else 0.0
                placements[ref] = (x, y, rot, layer)
                break

print(f"Total placements parsed: {len(placements)}")

bboxes = {}
for ref, (x, y, rot, layer) in placements.items():
    is_bottom, shapes = parse_shapes(fps[ref])
    box = get_world_bbox(ref, is_bottom, shapes, x, y, rot)
    bboxes[ref] = box

# Check overlaps
ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

overlaps = []
refs = list(bboxes.keys())
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        r1, r2 = refs[i], refs[j]
        if (r1, r2) in ALLOWED or (r2, r1) in ALLOWED:
            continue
        b1, b2 = bboxes[r1], bboxes[r2]
        if b1['layer'] != b2['layer']:
            continue
        
        # AABB overlap test
        # We add a tiny epsilon (0.01 mm) to ignore exact touchings
        if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
            dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
            dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
            overlaps.append((r1, r2, dx, dy, b1, b2))

print(f"Exact engine detected {len(overlaps)} overlaps!")
for r1, r2, dx, dy, b1, b2 in overlaps:
    print(f"  {r1:8s} ({b1['cx']:.1f}, {b1['cy']:.1f}) <--> {r2:8s} ({b2['cx']:.1f}, {b2['cy']:.1f}) : dx={dx:.2f}, dy={dy:.2f}")
