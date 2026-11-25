import math, re
from verify_golden_layout import P_golden, local_boxes, holes, r_board, y_cut, cx, cy

P_all = dict(P_golden)
P_all['C14'] = (100.0, 103.0, 0.0, 'B.Cu')
P_all['R61'] = (100.0, 97.0, 90.0, 'B.Cu')

print(f"Total components in P_all: {len(P_all)}")

def get_world_box(ref, x, y, rot):
    b = local_boxes.get(ref, (-1, 1, -1, 1))
    rad = math.radians(rot)
    cos_r = math.cos(rad)
    sin_r = math.sin(rad)
    corners = [(b[0], b[2]), (b[1], b[2]), (b[0], b[3]), (b[1], b[3])]
    rot_c = [(x + px * cos_r - py * sin_r, y + px * sin_r + py * cos_r) for px, py in corners]
    xs = [px for px, py in rot_c]
    ys = [py for px, py in rot_c]
    return min(xs), max(xs), min(ys), max(ys)

world_boxes = {}
for ref, (x, y, rot, layer) in P_all.items():
    world_boxes[ref] = (get_world_box(ref, x, y, rot), layer)

# 1. Check boundary
out_of_bounds = []
for ref, (box, layer) in world_boxes.items():
    # check 4 corners
    for px in [box[0], box[1]]:
        for py in [box[2], box[3]]:
            if py > y_cut + 0.05:
                out_of_bounds.append((ref, f"Y={py:.2f} > y_cut={y_cut}"))
            d = math.hypot(px - cx, py - cy)
            if d > 34.8:
                out_of_bounds.append((ref, f"dist={d:.2f} > 34.8"))

print(f"Out of bounds count: {len(out_of_bounds)}")
for item in out_of_bounds[:10]:
    print("  OOB:", item)

# 2. Check hole collisions (except holes themselves)
hole_collisions = []
for ref, (box, layer) in world_boxes.items():
    if ref in holes: continue
    for hname, (hx, hy) in holes.items():
        cx_box = max(box[0], min(hx, box[1]))
        cy_box = max(box[2], min(hy, box[3]))
        d = math.hypot(hx - cx_box, hy - cy_box)
        if d < 2.95:
            hole_collisions.append((ref, hname, f"dist={d:.2f} < 2.95"))

print(f"Hole collisions count: {len(hole_collisions)}")
for item in hole_collisions[:10]:
    print("  Hole collision:", item)

# 3. Check pairwise overlaps (on same layer)
# Allowed overlaps: NetTies with shunts
ALLOWED = {
    ('NT1', 'R47'), ('R47', 'NT1'),
    ('NT2', 'R47'), ('R47', 'NT2'),
    ('NT3', 'R48'), ('R48', 'NT3'),
    ('NT4', 'R48'), ('R48', 'NT4'),
    ('NT5', 'R49'), ('R49', 'NT5'),
    ('NT6', 'R49'), ('R49', 'NT6'),
}

overlaps = []
refs = list(world_boxes.keys())
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        r1, r2 = refs[i], refs[j]
        if (r1, r2) in ALLOWED: continue
        b1, l1 = world_boxes[r1]
        b2, l2 = world_boxes[r2]
        if l1 != l2: continue # different layer!
        # check overlap with 0.05 margin
        if not (b1[1] <= b2[0] + 0.05 or b2[1] <= b1[0] + 0.05 or b1[3] <= b2[2] + 0.05 or b2[3] <= b1[2] + 0.05):
            overlaps.append((r1, r2, b1, b2))

print(f"Pairwise overlaps count: {len(overlaps)}")
for r1, r2, b1, b2 in overlaps[:20]:
    print(f"  Overlap {r1} with {r2}: b1={b1}, b2={b2}")
