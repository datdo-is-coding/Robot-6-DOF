import math, sys, random
sys.path.insert(0, 'scratch')
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 120.2

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
R_KO = 2.95

# Let's import best_P from force_directed_placement
import force_directed_placement as fdp
P = dict(fdp.best_P)

LOCKED = {'H1', 'H2', 'H3', 'H4'}

def eval_state(P_curr):
    bboxes = {}
    for ref, (x, y, rot, layer) in P_curr.items():
        is_b = (layer == 'B.Cu')
        _, shapes = parse_shapes(fps[ref])
        bboxes[ref] = get_world_bbox(ref, is_b, shapes, x, y, rot)
    
    overlaps = []
    refs = list(bboxes.keys())
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            if (r1, r2) in ALLOWED or (r2, r1) in ALLOWED: continue
            b1, b2 = bboxes[r1], bboxes[r2]
            if b1['layer'] != b2['layer']: continue
            if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
                b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
                dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
                dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
                overlaps.append((r1, r2, dx, dy))
    
    hole_errs = []
    for hname, (hx, hy) in HOLES.items():
        for r, b in bboxes.items():
            if r in ['H1', 'H2', 'H3', 'H4']: continue
            cx_box = max(b['x1'], min(hx, b['x2']))
            cy_box = max(b['y1'], min(hy, b['y2']))
            d = math.hypot(cx_box - hx, cy_box - hy)
            if d < R_KO:
                hole_errs.append((hname, r, R_KO - d))
    
    oob = []
    for r, b in bboxes.items():
        for px in [b['x1'], b['x2']]:
            for py in [b['y1'], b['y2']]:
                if py > y_cut + 0.05:
                    oob.append((r, py - y_cut))
                d = math.hypot(px - 100.0, py - 100.0)
                if d > 34.85:
                    oob.append((r, d - 34.85))
    
    return overlaps, hole_errs, oob, bboxes

ov, he, ob, bboxes = eval_state(P)
print(f"Remaining overlaps ({len(ov)}):")
for r1, r2, dx, dy in ov:
    print(f"  {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")

print(f"Remaining hole errors ({len(he)}):")
for h, r, pen in he:
    print(f"  {h} <--> {r} : pen={pen:.2f}")

print(f"Remaining OOB ({len(ob)}):")
for r, pen in ob:
    print(f"  {r} : pen={pen:.2f}")
