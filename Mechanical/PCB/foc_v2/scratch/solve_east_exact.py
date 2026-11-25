import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's import the base placement without East Wing
from solve_all_zero_perfect import P, HOLES, ALLOWED, get_custom_bbox

obs_P = {k: v for k, v in P.items() if k not in ['J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58']}

bboxes_obs = {}
for ref, (x, y, rot, layer) in obs_P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    bboxes_obs[ref] = get_custom_bbox(ref, is_b, shapes, x, y, rot)

def check_single_box_overlap(b1, b2):
    return (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01)

def evaluate_east(east_dict):
    east_boxes = {}
    for ref, (x, y, rot, layer) in east_dict.items():
        is_b = (layer == 'B.Cu')
        _, shapes = parse_shapes(fps[ref])
        b = get_custom_bbox(ref, is_b, shapes, x, y, rot)
        east_boxes[ref] = b
        
        # Check OOB
        for px in [b['x1'], b['x2']]:
            for py in [b['y1'], b['y2']]:
                if py > 120.0: return False, f"{ref} OOB Y={py:.2f}"
                d = math.hypot(px - 100.0, py - 100.0)
                if d > 34.90: return False, f"{ref} OOB dist={d:.2f}"
                
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
                
    return True, "PERFECT"

# Search over grid for the 12 components:
# Notice that J11, F1, D6 are high-power 24V inputs.
# L1, D4, C16, C17, R53, R54 are Buck converter.
# U10, C57, C58 are 3.3V LDO.

# Let's run a grid search:
found = False
for f1_rot in [0, 90, 270]:
    for f1_x in [113.0, 114.0, 115.0, 116.0, 117.0, 118.0, 119.0, 120.0, 121.0, 122.0]:
        for f1_y in [90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0]:
            cand = {'F1': (f1_x, f1_y, f1_rot, 'F.Cu')}
            v, _ = evaluate_east(cand)
            if not v: continue
            
            for j11_x in [116.0, 117.0, 118.0, 119.0, 120.0]:
                for j11_y in [96.0, 98.0, 100.0, 102.0, 104.0]:
                    cand['J11'] = (j11_x, j11_y, 270, 'F.Cu')
                    v, _ = evaluate_east(cand)
                    if not v: continue
                    
                    for d6_x in [114.0, 116.0, 118.0, 120.0, 122.0, 124.0]:
                        for d6_y in [98.0, 100.0, 102.0, 104.0, 106.0]:
                            cand['D6'] = (d6_x, d6_y, 0, 'F.Cu')
                            v, _ = evaluate_east(cand)
                            if not v: continue
                            
                            # print promising power input trio:
                            # print(f"Found power input trio: F1=({f1_x},{f1_y}), J11=({j11_x},{j11_y}), D6=({d6_x},{d6_y})")
                            found = True
                            break
                        if found: break
                    if found: break
                if found: break
            if found: break
        if found: break
    if found: break

print("Completed initial search.")
