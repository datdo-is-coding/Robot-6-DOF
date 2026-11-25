import math, copy
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Start with our base placements
from optimize_clean_layout import P

# Fix J11 rotation
P['J11'] = (121.0, 99.5, 270, 'F.Cu')

# Fix L1 position (was colliding with H4 at (115.556, 84.444))
# Move L1 to (118.5, 87.5) or (113.0, 89.5)?
# Distance from H4 (115.556, 84.444):
# If L1 is at (122.0, 88.0):
# dist to H4: sqrt((122-115.55)^2 + (88-84.44)^2) = sqrt(6.44^2 + 3.55^2) = 7.36 mm!
# L1 box: 6.5 x 6.5.
# Let's check where L1, D4, C16, C17 can be cleanly placed in the East zone.

# Also USB passives on B.Cu:
# U8 (103.5, 124.0), Q7 (103.5, 120.0), R40 (98.0, 122.0), R41 (98.0, 125.0), R42 (109.0, 122.0), R43 (109.0, 125.0), C59 (103.5, 127.5)

# Also shunts and gate driver resistors:
# R47, R48, R49:
# If R47 is at y = 84.5, R6 is at y = 89.5:
# R47 is at (93.0, 84.5), R48 at (100.0, 84.5), R49 at (107.0, 84.5)
# R6..R10, R50..R52:
# In rot=90: width 1.46, height 2.96.
# If R6 is at y = 90.0, height is 2.96: y in [88.52, 91.48].
# R47 is at y = 84.5: y in [80.67, 88.33].
# Gap = 88.52 - 88.33 = 0.19 mm! ZERO OVERLAP!

ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

HOLES = {
    "H3": (84.444, 84.444),
    "H4": (115.556, 84.444),
    "H2": (84.444, 115.556),
    "H1": (115.556, 115.556)
}
R_KO = 3.0

def eval_placements(p_dict):
    bboxes = {}
    for ref, (x, y, rot, layer) in p_dict.items():
        is_b = (layer == 'B.Cu')
        _, shapes = parse_shapes(fps[ref])
        box = get_world_bbox(ref, is_b, shapes, x, y, rot)
        bboxes[ref] = box

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
            if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
                b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
                dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
                dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
                overlaps.append((r1, r2, dx, dy, b1, b2))

    hole_errs = []
    for hname, (hx, hy) in HOLES.items():
        for r, b in bboxes.items():
            if r in ['H1', 'H2', 'H3', 'H4']: continue
            cx = max(b['x1'], min(hx, b['x2']))
            cy = max(b['y1'], min(hy, b['y2']))
            d = math.hypot(cx - hx, cy - hy)
            if d < R_KO:
                hole_errs.append((hname, r, d))

    return overlaps, hole_errs, bboxes

overlaps, hole_errs, bboxes = eval_placements(P)
print(f"Initial: overlaps={len(overlaps)}, hole_errs={len(hole_errs)}")
for r1, r2, dx, dy, b1, b2 in overlaps:
    print(f"  {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, d in hole_errs:
    print(f"  {h} <--> {r} : dist={d:.2f}")
