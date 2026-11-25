import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

def get_bbox(ref, x, y, rot, layer='F.Cu'):
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    if ref in ['H1', 'H4']:
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.40, 'x2': x + 2.40, 'y1': y - 2.40, 'y2': y + 2.40, 'cx': x, 'cy': y, 'w': 4.80, 'h': 4.80}
    elif ref == 'C63':
        ccx = x + 2.5
        return {'ref': ref, 'layer': 'top', 'x1': ccx - 5.25, 'x2': ccx + 5.25, 'y1': y - 5.25, 'y2': y + 5.25, 'cx': ccx, 'cy': y, 'w': 10.50, 'h': 10.50, 'is_circle': True, 'cr': 5.25}
    elif ref == 'J9':
        return {'ref': ref, 'layer': 'top', 'x1': x - 2.70, 'x2': x + 7.70, 'y1': y - 2.60, 'y2': y + 9.45, 'cx': x + 2.5, 'cy': y + 3.425, 'w': 10.40, 'h': 12.05}
    else:
        return get_world_bbox(ref, is_b, shapes, x, y, rot)

fixed = {
    'H4': (115.556, 84.444, 0, 'F.Cu'),
    'H1': (115.556, 115.556, 0, 'F.Cu'),
    'C63': (122.5, 86.5, 0, 'F.Cu'),
    'J9': (121.0, 110.30, 0, 'F.Cu'),
    'U1': (100.0, 100.8, 0, 'F.Cu')
}

# Let's inspect J11 at (116.0, 100.0, rot=270):
# x in [113.75, 129.60], y in [90.35, 104.65]
# Wait, F1 can be at rot=0 (horizontal, w=16.5, h=7.24) at X=118.0, Y=106.0?
# Or F1 at rot=90 (vertical, w=7.24, h=16.5) at X=126.5, Y=98.0?

def check_overlaps(candidates):
    bboxes = {}
    for r, (x, y, rot, layer) in candidates.items():
        bboxes[r] = get_bbox(r, x, y, rot, layer)
    overlaps = []
    refs = list(bboxes.keys())
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            b1, b2 = bboxes[r1], bboxes[r2]
            if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
                b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
                overlaps.append((r1, r2))
    oob = []
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
            oob.append((r, max_d))
    return overlaps, oob

# Let's write an automatic grid search for the 10 components in East wing:
print("Searching for clean East placement...")
