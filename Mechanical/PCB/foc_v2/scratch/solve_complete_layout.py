import math, json, re

# Let's read all 124 footprints and their exact local bounding boxes from KiCad
with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb_text = f.read()

# Load local boxes
import test_courtyards
local_boxes = test_courtyards.parse_footprints()

print(f"Loaded {len(local_boxes)} footprint definitions.")

# Center and radius of board
cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 120.2

holes = {
    'H1': (115.556, 115.556),
    'H2': (84.444, 115.556),
    'H3': (84.444, 84.444),
    'H4': (115.556, 84.444)
}

def get_global_box(ref, x, y, rot=0.0):
    b = local_boxes.get(ref, (-1, 1, -1, 1))
    rad = math.radians(rot)
    cos_r = math.cos(rad)
    sin_r = math.sin(rad)
    # 4 corners
    corners = [(b[0], b[2]), (b[1], b[2]), (b[0], b[3]), (b[1], b[3])]
    rot_corners = [(x + px * cos_r - py * sin_r, y + px * sin_r + py * cos_r) for px, py in corners]
    xs = [px for px, py in rot_corners]
    ys = [py for px, py in rot_corners]
    return (min(xs), max(xs), min(ys), max(ys))

def check_overlap(b1, b2, margin=0.1):
    if b1[1] + margin < b2[0] or b2[1] + margin < b1[0]:
        return False
    if b1[3] + margin < b2[2] or b2[3] + margin < b1[2]:
        return False
    return True

def check_board_boundary(b, max_r=34.6):
    for x in [b[0], b[1]]:
        for y in [b[2], b[3]]:
            if y > y_cut + 0.05:
                return False
            if math.hypot(x - cx, y - cy) > max_r:
                return False
    return True

print("Layout verification engine initialized.")
