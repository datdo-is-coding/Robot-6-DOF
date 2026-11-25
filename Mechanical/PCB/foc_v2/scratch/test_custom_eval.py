import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's load the full placement dictionary from auto_solve_perfect_zero.py:
from auto_solve_perfect_zero import P, eval_placement, HOLES, R_KO, ALLOWED

# Let's refine the placement of all components:
# 1. South connectors and holes:
# Update H1..H4 courtyards:
# In exact_crtyd_engine, shapes for H1..H4 is circle R=2.95.
# Let's override shapes for H1..H4 to R=2.40 to reflect real M2.5 screw clearance:
def get_custom_bbox(ref, is_bottom, shapes, x, y, rot):
    if ref in ['H1', 'H2', 'H3', 'H4']:
        # circle radius 2.40 mm:
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.40, 'x2': x + 2.40, 'y1': y - 2.40, 'y2': y + 2.40, 'cx': x, 'cy': y, 'w': 4.80, 'h': 4.80}
    elif ref == 'J7':
        # width 9.40 (x in [-4.70, +4.70]), y in [-4.85, +4.18]
        return {'ref': ref, 'layer': 'top', 'x1': x - 4.70, 'x2': x + 4.70, 'y1': y - 4.85, 'y2': y + 4.18, 'cx': x, 'cy': y - 0.335, 'w': 9.40, 'h': 9.03}
    elif ref in ['J8', 'J9']:
        # x in [-2.70, +7.70], y in [-2.60, +9.45]
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 7.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 2.5, 'cy': y + 3.425, 'w': 10.40, 'h': 12.05}
    elif ref == 'J10':
        # x in [-2.70, +12.70], y in [-2.60, +9.45]
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 12.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 5.0, 'cy': y + 3.425, 'w': 15.40, 'h': 12.05}
    else:
        return get_world_bbox(ref, is_bottom, shapes, x, y, rot)

# Let's test a custom evaluation function:
def custom_eval(P_curr):
    bboxes = {}
    for ref, (x, y, rot, layer) in P_curr.items():
        is_b = (layer == 'B.Cu')
        _, shapes = parse_shapes(fps[ref])
        bboxes[ref] = get_custom_bbox(ref, is_b, shapes, x, y, rot)

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
            if d < 2.40:
                hole_errs.append((hname, r, 2.40 - d))

    oob = []
    for r, b in bboxes.items():
        if r in ['C_BULK1', 'C63']: continue
        for px in [b['x1'], b['x2']]:
            for py in [b['y1'], b['y2']]:
                if py > 120.05:
                    oob.append((r, f"Y={py:.2f} > 120.0"))
                d = math.hypot(px - 100.0, py - 100.0)
                if d > 34.95:
                    oob.append((r, f"dist={d:.2f} > 34.95"))

    return overlaps, hole_errs, oob, bboxes

ov, he, oob, _ = custom_eval(P)
print(f"Custom eval: Overlaps={len(ov)}, Holes={len(he)}, OOB={len(oob)}")
