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

# Fixed anchors:
# H4: (115.556, 84.444)
# H1: (115.556, 115.556)
# C63: (122.5, 86.5, rot=0)
# J9: (121.0, 110.30, rot=0)
# U1: right edge is at X = 106.7
# IC1: right flank passives at X = 109.2

fixed = {
    'H4': (115.556, 84.444, 0, 'F.Cu'),
    'H1': (115.556, 115.556, 0, 'F.Cu'),
    'C63': (122.5, 86.5, 0, 'F.Cu'),
    'J9': (121.0, 110.30, 0, 'F.Cu'),
}

# Remaining to place:
# J11, F1, D6, L1, D4, C16, C17, R53, R54, U10, C57, C58

# Let's test F1 at (127.0, 107.0, 90)
# D6 at (124.0, 113.0, 0)
# Where can J11 be?
# Can J11 be at rot=0, 90, 180, or 270?
