import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's fix F1, D6, J11 at their proven spots:
# F1: (113.0, 104.0, 90)
# D6: (114.0, 109.5, 0)
# J11: (121.0, 96.0, 270)

from auto_solve_perfect_zero import P

P['F1']  = (113.0, 104.0, 90, 'F.Cu')
P['D6']  = (114.0, 109.5, 0,  'F.Cu')
P['J11'] = (121.0, 96.0, 270, 'F.Cu')

# Remove Buck items to search for them:
buck_items = ['L1', 'D4', 'C16', 'C17', 'R53', 'R54']
obstacles = {}
for r, (x, y, rot, layer) in P.items():
    if r in buck_items or layer != 'F.Cu': continue
    _, shapes = parse_shapes(fps[r])
    obstacles[r] = get_world_bbox(r, False, shapes, x, y, rot)

holes = {'H1': (115.556, 115.556), 'H2': (84.444, 115.556), 'H3': (84.444, 84.444), 'H4': (115.556, 84.444)}
for h, (hx, hy) in holes.items():
    obstacles[h] = {'x1': hx - 2.5, 'x2': hx + 2.5, 'y1': hy - 2.5, 'y2': hy + 2.5, 'layer': 'top'}

def fits(ref, x, y, rot, current_obstacles):
    _, shapes = parse_shapes(fps[ref])
    b = get_world_bbox(ref, False, shapes, x, y, rot)
    if b['y2'] > 120.0: return False, None
    for px in [b['x1'], b['x2']]:
        for py in [b['y1'], b['y2']]:
            if math.hypot(px - 100.0, py - 100.0) > 34.8: return False, None
    for h, (hx, hy) in holes.items():
        cx_box = max(b['x1'], min(hx, b['x2']))
        cy_box = max(b['y1'], min(hy, b['y2']))
        if math.hypot(cx_box - hx, cy_box - hy) < 2.45: return False, None
    for r, b2 in current_obstacles.items():
        if (b['x1'] < b2['x2'] - 0.01 and b['x2'] > b2['x1'] + 0.01 and
            b['y1'] < b2['y2'] - 0.01 and b['y2'] > b2['y1'] + 0.01):
            return False, None
    return True, b

print("Searching spots for L1...")
l1_spots = []
for x in [v * 0.5 for v in range(140, 255)]:
    for y in [v * 0.5 for v in range(140, 240)]:
        ok, b = fits('L1', x, y, 0, obstacles)
        if ok:
            l1_spots.append((x, y, b))

print(f"Found {len(l1_spots)} spots for L1!")
for x, y, b in l1_spots[:10]:
    print(f"  L1 at ({x:.1f}, {y:.1f}): X=[{b['x1']:.1f}, {b['x2']:.1f}], Y=[{b['y1']:.1f}, {b['y2']:.1f}]")
