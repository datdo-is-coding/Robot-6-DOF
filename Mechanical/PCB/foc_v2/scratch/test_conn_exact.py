import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's test the 4 connectors and H1, H2:
y_cut = 120.0

# Proposed positions:
# J8: 3-pin XH
# J7: USB-C
# J10: 5-pin XH
# J9: 3-pin XH
# Let's test positions:
P_test = {
    'H2': (84.444, 115.556, 0, 'F.Cu'),
    'H1': (115.556, 115.556, 0, 'F.Cu'),
    'J8': (74.0, 110.30, 0, 'F.Cu'),
    'J7': (92.25, 115.82, 0, 'F.Cu'),
    'J10': (100.40, 110.30, 0, 'F.Cu'),
    'J9': (121.0, 110.30, 0, 'F.Cu')
}

bboxes = {}
for ref, (x, y, rot, layer) in P_test.items():
    is_b, shapes = parse_shapes(fps[ref])
    bboxes[ref] = get_world_bbox(ref, is_b, shapes, x, y, rot)

print("Bounding boxes:")
for ref, b in bboxes.items():
    print(f"  {ref:5s}: X in [{b['x1']:6.2f}, {b['x2']:6.2f}], Y in [{b['y1']:6.2f}, {b['y2']:6.2f}]")

# Check overlaps between components:
refs = list(P_test.keys())
print("\nPairwise checks:")
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        r1, r2 = refs[i], refs[j]
        b1, b2 = bboxes[r1], bboxes[r2]
        overlap_x = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
        overlap_y = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
        if overlap_x > 0 and overlap_y > 0:
            print(f"  OVERLAP: {r1} <--> {r2}: dx={overlap_x:.3f}, dy={overlap_y:.3f}")
        else:
            gap_x = max(b1['x1'] - b2['x2'], b2['x1'] - b1['x2'], 0)
            gap_y = max(b1['y1'] - b2['y2'], b2['y1'] - b1['y2'], 0)
            print(f"  OK: {r1:5s} <--> {r2:5s}: gap_x={gap_x:.3f}, gap_y={gap_y:.3f}")

# Check distance to circle (100, 100), R = 35.0 mm:
print("\nDistance to board edge:")
for ref in ['J8', 'J7', 'J10', 'J9']:
    b = bboxes[ref]
    corners = [(b['x1'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y1']), (b['x2'], b['y2'])]
    max_d = max(math.hypot(x - 100.0, y - 100.0) for x, y in corners)
    max_y = max(y for _, y in corners)
    print(f"  {ref:5s}: max_dist_to_center = {max_d:.2f} mm (limit 35.0), max_Y = {max_y:.2f} mm (cut {y_cut:.2f})")
