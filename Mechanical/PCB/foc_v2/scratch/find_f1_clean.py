import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Define locked obstacles
from test_perfect_schedule import P
# remove items we want to solve
to_solve = ['F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58', 'J11']
obstacles = {}
for r, (x, y, rot, layer) in P.items():
    if r in to_solve or layer != 'F.Cu': continue
    _, shapes = parse_shapes(fps[r])
    obstacles[r] = get_world_bbox(r, False, shapes, x, y, rot)

# Add H1..H4 keepouts as boxes
holes = {'H1': (115.556, 115.556), 'H2': (84.444, 115.556), 'H3': (84.444, 84.444), 'H4': (115.556, 84.444)}
for h, (hx, hy) in holes.items():
    obstacles[h] = {'x1': hx - 2.5, 'x2': hx + 2.5, 'y1': hy - 2.5, 'y2': hy + 2.5, 'layer': 'top'}

def fits(ref, x, y, rot, current_obstacles):
    _, shapes = parse_shapes(fps[ref])
    b = get_world_bbox(ref, False, shapes, x, y, rot)
    # in board
    if b['y2'] > 120.0: return False, None
    for px in [b['x1'], b['x2']]:
        for py in [b['y1'], b['y2']]:
            if math.hypot(px - 100.0, py - 100.0) > 34.8: return False, None
    # hole clearance
    for h, (hx, hy) in holes.items():
        cx_box = max(b['x1'], min(hx, b['x2']))
        cy_box = max(b['y1'], min(hy, b['y2']))
        if math.hypot(cx_box - hx, cy_box - hy) < 2.45: return False, None
    # obstacles
    for r, b2 in current_obstacles.items():
        if (b['x1'] < b2['x2'] - 0.01 and b['x2'] > b2['x1'] + 0.01 and
            b['y1'] < b2['y2'] - 0.01 and b['y2'] > b2['y1'] + 0.01):
            return False, None
    return True, b

# Let's search where F1 can go:
print("Searching for F1...")
f1_spots = []
for rot in [0, 90, 180, 270]:
    for x in [v * 0.5 for v in range(140, 255)]:
        for y in [v * 0.5 for v in range(140, 240)]:
            ok, b = fits('F1', x, y, rot, obstacles)
            if ok:
                f1_spots.append((x, y, rot, b))

print(f"Found {len(f1_spots)} valid spots for F1!")
for x, y, rot, b in f1_spots[:10]:
    print(f"  F1 at ({x:.1f}, {y:.1f}, rot={rot}): X=[{b['x1']:.1f}, {b['x2']:.1f}], Y=[{b['y1']:.1f}, {b['y2']:.1f}]")
