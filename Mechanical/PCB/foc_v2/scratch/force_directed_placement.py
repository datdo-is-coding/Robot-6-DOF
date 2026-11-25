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

import perfect_drc_solver as pds
P = dict(pds.P)

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

# Relaxation loop
best_P = dict(P)
best_score = 999999

for it in range(100):
    ov, he, ob, bboxes = eval_state(P)
    score = len(ov) * 10 + len(he) * 50 + len(ob) * 20
    if it % 10 == 0 or score == 0:
        print(f"Iteration {it:3d}: Overlaps={len(ov):2d}, Holes={len(he):2d}, OOB={len(ob):2d}, Score={score}")
    if score < best_score:
        best_score = score
        best_P = dict(P)
    if score == 0:
        print("CONVERGED TO ZERO VIOLATIONS!")
        break
    
    # Calculate displacement vectors for each component
    shifts = {r: [0.0, 0.0] for r in P}
    
    # 1. Overlaps
    for r1, r2, dx, dy in ov:
        b1, b2 = bboxes[r1], bboxes[r2]
        c1x, c1y = (b1['x1'] + b1['x2']) / 2, (b1['y1'] + b1['y2']) / 2
        c2x, c2y = (b2['x1'] + b2['x2']) / 2, (b2['y1'] + b2['y2']) / 2
        step = min(dx, dy) * 0.5 + 0.1
        if dx < dy:
            dir_x = 1.0 if c1x > c2x else -1.0
            if r1 not in LOCKED: shifts[r1][0] += dir_x * step
            if r2 not in LOCKED: shifts[r2][0] -= dir_x * step
        else:
            dir_y = 1.0 if c1y > c2y else -1.0
            if r1 not in LOCKED: shifts[r1][1] += dir_y * step
            if r2 not in LOCKED: shifts[r2][1] -= dir_y * step
            
    # 2. Holes
    for hname, r, pen in he:
        if r in LOCKED: continue
        hx, hy = HOLES[hname]
        b = bboxes[r]
        cx_box = (b['x1'] + b['x2']) / 2
        cy_box = (b['y1'] + b['y2']) / 2
        dist = math.hypot(cx_box - hx, cy_box - hy) + 1e-5
        ux, uy = (cx_box - hx) / dist, (cy_box - hy) / dist
        step = pen + 0.2
        shifts[r][0] += ux * step
        shifts[r][1] += uy * step
        
    # 3. OOB
    for r, pen in ob:
        if r in LOCKED: continue
        b = bboxes[r]
        cx_box = (b['x1'] + b['x2']) / 2
        cy_box = (b['y1'] + b['y2']) / 2
        # pull towards center
        dist = math.hypot(cx_box - 100.0, cy_box - 100.0) + 1e-5
        ux, uy = (100.0 - cx_box) / dist, (100.0 - cy_box) / dist
        step = min(pen + 0.2, 2.0)
        shifts[r][0] += ux * step
        shifts[r][1] += uy * step
        
    # Apply shifts with damping
    for r, (sx, sy) in shifts.items():
        if r in LOCKED: continue
        x, y, rot, layer = P[r]
        # clamp step
        mag = math.hypot(sx, sy)
        if mag > 1.5:
            sx = (sx / mag) * 1.5
            sy = (sy / mag) * 1.5
        P[r] = (round(x + sx, 2), round(y + sy, 2), rot, layer)

P = best_P
ov, he, ob, _ = eval_state(P)
print(f"Final state: Overlaps={len(ov)}, Holes={len(he)}, OOB={len(ob)}")
