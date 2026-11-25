import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's import the base placement without East Wing
from solve_all_zero_perfect import P, HOLES, ALLOWED, get_custom_bbox

# Components to solve on East Wing:
# J11, F1, D6, L1, D4, C16, C17, R53, R54, U10, C57, C58

# Fixed items:
# H4: (115.556, 84.444)
# H1: (115.556, 115.556)
# C63: (123.5, 86.0) -> can R=5.25 centered at (126.0, 86.0)
# J9: (121.0, 110.30)
# IC1: (100.0, 87.5) -> right flank passives C15..C21 at X=106.0, R55..R60 at X=109.5
# U1: (100.0, 101.0) -> right flank passives C6, C7, C50 at X=107.5

# Let's check bounding boxes of obstacles:
obs_P = {k: v for k, v in P.items() if k not in ['J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58']}

bboxes_obs = {}
for ref, (x, y, rot, layer) in obs_P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    bboxes_obs[ref] = get_custom_bbox(ref, is_b, shapes, x, y, rot)

def check_single_box_overlap(b1, b2):
    return (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01)

def is_valid_east(east_dict):
    east_boxes = {}
    for ref, (x, y, rot, layer) in east_dict.items():
        is_b = (layer == 'B.Cu')
        _, shapes = parse_shapes(fps[ref])
        b = get_custom_bbox(ref, is_b, shapes, x, y, rot)
        east_boxes[ref] = b
        
        # Check OOB
        for px in [b['x1'], b['x2']]:
            for py in [b['y1'], b['y2']]:
                if py > 120.0: return False, f"{ref} OOB Y={py}"
                d = math.hypot(px - 100.0, py - 100.0)
                if d > 34.95: return False, f"{ref} OOB dist={d}"
                
        # Check hole collision
        for hname, (hx, hy) in HOLES.items():
            cx_box = max(b['x1'], min(hx, b['x2']))
            cy_box = max(b['y1'], min(hy, b['y2']))
            if math.hypot(cx_box - hx, cy_box - hy) < 2.40:
                return False, f"{ref} collides with {hname}"
                
        # Check against existing obstacles
        for r_obs, b_obs in bboxes_obs.items():
            if b_obs['layer'] == b['layer']:
                if check_single_box_overlap(b, b_obs):
                    return False, f"{ref} overlaps with {r_obs}"
                    
    # Check pairwise within east_dict
    refs = list(east_boxes.keys())
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            if check_single_box_overlap(east_boxes[r1], east_boxes[r2]):
                return False, f"{r1} overlaps with {r2}"
                
    return True, "OK"

print("Solver framework ready.")
# Let's test a candidate configuration:
# 1. J11 at (117.0, 101.5, rot=270)
# 2. F1 at (126.0, 93.0, rot=90)
# 3. D6 at (126.0, 103.5, rot=90)
# 4. L1 at (114.5, 90.0, rot=0)
# 5. D4 at (114.5, 95.0, rot=0)
# 6. C16 at (113.0, 98.0, rot=90)
# 7. C17 at (115.5, 98.0, rot=90)
# 8. R53 at (113.0, 100.5, rot=0)
# 9. R54 at (115.5, 100.5, rot=0)
# 10. U10 at (113.0, 104.0, rot=0)
# 11. C57 at (112.5, 106.5, rot=0)
# 12. C58 at (115.5, 106.5, rot=0)

east_cand = {
    'J11': (117.0, 101.5, 270, 'F.Cu'),
    'F1':  (126.5, 93.5, 90, 'F.Cu'),
    'D6':  (126.0, 103.5, 90, 'F.Cu'),
    'L1':  (114.5, 90.0, 0, 'F.Cu'),
    'D4':  (114.5, 95.0, 0, 'F.Cu'),
    'C16': (113.0, 98.0, 90, 'F.Cu'),
    'C17': (115.5, 98.0, 90, 'F.Cu'),
    'R53': (113.0, 100.5, 0, 'F.Cu'),
    'R54': (115.5, 100.5, 0, 'F.Cu'),
    'U10': (113.0, 104.0, 0, 'F.Cu'),
    'C57': (112.5, 106.5, 0, 'F.Cu'),
    'C58': (115.5, 106.5, 0, 'F.Cu')
}

valid, msg = is_valid_east(east_cand)
print("Candidate test:", valid, msg)
