import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

def get_custom_bbox(ref, is_bottom, shapes, x, y, rot):
    if ref in ['H1', 'H2', 'H3', 'H4']:
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.40, 'x2': x + 2.40, 'y1': y - 2.40, 'y2': y + 2.40, 'cx': x, 'cy': y, 'w': 4.80, 'h': 4.80}
    elif ref == 'J7':
        return {'ref': ref, 'layer': 'top', 'x1': x - 4.80, 'x2': x + 4.80, 'y1': y - 4.85, 'y2': y + 4.18, 'cx': x, 'cy': y - 0.335, 'w': 9.60, 'h': 9.03}
    elif ref in ['J8', 'J9']:
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 7.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 2.5, 'cy': y + 3.425, 'w': 10.40, 'h': 12.05}
    elif ref == 'J10':
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 12.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 5.0, 'cy': y + 3.425, 'w': 15.40, 'h': 12.05}
    elif ref == 'C_BULK1':
        ccx = x - 2.5
        return {'ref': ref, 'layer': 'top', 'x1': ccx - 5.25, 'x2': ccx + 5.25, 'y1': y - 5.25, 'y2': y + 5.25, 'cx': ccx, 'cy': y, 'w': 10.50, 'h': 10.50, 'is_circle': True, 'cr': 5.25}
    elif ref == 'C63':
        ccx = x + 2.5
        return {'ref': ref, 'layer': 'top', 'x1': ccx - 5.25, 'x2': ccx + 5.25, 'y1': y - 5.25, 'y2': y + 5.25, 'cx': ccx, 'cy': y, 'w': 10.50, 'h': 10.50, 'is_circle': True, 'cr': 5.25}
    else:
        return get_world_bbox(ref, is_bottom, shapes, x, y, rot)

ALLOWED = {
    ("NT1", "R47"), ("NT2", "R47"),
    ("NT3", "R48"), ("NT4", "R48"),
    ("NT5", "R49"), ("NT6", "R49")
}

delta_h = 22.0 / math.sqrt(2) # 15.55635
HOLES = {
    "H3": (100.0 - delta_h, 100.0 - delta_h),
    "H4": (100.0 + delta_h, 100.0 - delta_h),
    "H2": (100.0 - delta_h, 100.0 + delta_h),
    "H1": (100.0 + delta_h, 100.0 + delta_h)
}

def eval_full(P_curr):
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
            if b.get('is_circle'):
                dist = math.hypot(b['cx'] - hx, b['cy'] - hy)
                if dist < b['cr'] + 2.40:
                    hole_errs.append((hname, r, b['cr'] + 2.40 - dist))
            else:
                cx_box = max(b['x1'], min(hx, b['x2']))
                cy_box = max(b['y1'], min(hy, b['y2']))
                dist = math.hypot(cx_box - hx, cy_box - hy)
                if dist < 2.40:
                    hole_errs.append((hname, r, 2.40 - dist))

    oob_errs = []
    for r, b in bboxes.items():
        if b.get('is_circle'):
            max_d = math.hypot(b['cx'] - 100.0, b['cy'] - 100.0) + b['cr']
        else:
            corners = [
                (b['x1'], b['y1']), (b['x1'], b['y2']),
                (b['x2'], b['y1']), (b['x2'], b['y2'])
            ]
            max_d = max(math.hypot(cx - 100.0, cy - 100.0) for cx, cy in corners)
        if max_d > 34.95:
            oob_errs.append((r, max_d))

    return overlaps, hole_errs, oob_errs

# Let's inspect F1 footprint and where it was in git_raw
lines_f1 = fps['F1']
is_b, shapes_f1 = parse_shapes(lines_f1)
print("F1 shapes:", shapes_f1)
print("F1 bbox rot=0:", get_custom_bbox('F1', False, shapes_f1, 0, 0, 0))
print("F1 bbox rot=90:", get_custom_bbox('F1', False, shapes_f1, 0, 0, 90))
