import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

# Base positions
P = dict(s.P)
P['C63'] = (124.5, 76.0, 0, 'F.Cu')
P['L1']  = (123.5, 89.0, 0, 'F.Cu')
P['D4']  = (115.0, 92.5, 0, 'F.Cu')
P['C16'] = (114.5, 96.2, 90, 'F.Cu')
P['C17'] = (114.5, 100.2, 90, 'F.Cu')
P['R53'] = (118.0, 96.2, 0, 'F.Cu')
P['R54'] = (118.0, 98.5, 0, 'F.Cu')
P['J11'] = (122.0, 103.5, 270, 'F.Cu')

# Precompute static boxes
static_refs = [r for r in P.keys() if r not in ['F1', 'D6']]
static_boxes = {}
for ref in static_refs:
    x, y, rot, layer = P[ref]
    is_b = (layer == 'B.Cu')
    _, shapes = s.parse_shapes(s.fps[ref])
    box = s.get_world_bbox(ref, is_b, shapes, x, y, rot)
    static_boxes[ref] = box

def check_box_overlap(b1, b2):
    return (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01)

def check_hole(b):
    for hname, (hx, hy) in s.HOLES.items():
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        if math.hypot(cx - hx, cy - hy) < s.R_KO:
            return True
    return False

_, f1_shapes = s.parse_shapes(s.fps['F1'])
_, d6_shapes = s.parse_shapes(s.fps['D6'])

found = []
# F1 can be at x in [120..130], y in [105..128]
# D6 can be at x in [115..130], y in [105..128]
print("Running fast search...")
for f1_rot in [0, 90, 180, 270]:
    for f1_x in [x * 0.5 for x in range(240, 260)]: # 120.0 to 129.5
        for f1_y in [y * 0.5 for y in range(215, 255)]: # 107.5 to 127.0
            box_f1 = s.get_world_bbox('F1', False, f1_shapes, f1_x, f1_y, f1_rot)
            # board edge constraint (x <= 134.5, y <= 132.0)
            if box_f1['x2'] > 134.5 or box_f1['y2'] > 132.0 or box_f1['x1'] < 105.0:
                continue
            if check_hole(box_f1):
                continue
            # check static overlaps
            f1_coll = False
            for sref, sbox in static_boxes.items():
                if sbox['layer'] == 'top' and check_box_overlap(box_f1, sbox):
                    f1_coll = True
                    break
            if f1_coll:
                continue

            # F1 is valid! Now test D6
            for d6_rot in [0, 90]:
                for d6_x in [x * 0.5 for x in range(230, 260)]: # 115.0 to 129.5
                    for d6_y in [y * 0.5 for y in range(215, 258)]: # 107.5 to 128.5
                        box_d6 = s.get_world_bbox('D6', False, d6_shapes, d6_x, d6_y, d6_rot)
                        if box_d6['x2'] > 134.5 or box_d6['y2'] > 132.0:
                            continue
                        if check_hole(box_d6):
                            continue
                        if check_box_overlap(box_f1, box_d6):
                            continue
                        d6_coll = False
                        for sref, sbox in static_boxes.items():
                            if sbox['layer'] == 'top' and check_box_overlap(box_d6, sbox):
                                d6_coll = True
                                break
                        if not d6_coll:
                            found.append((f1_x, f1_y, f1_rot, d6_x, d6_y, d6_rot))
                            print(f"FOUND: F1=({f1_x:.1f}, {f1_y:.1f}, {f1_rot}), D6=({d6_x:.1f}, {d6_y:.1f}, {d6_rot})")
                            break
                    if found: break
                if found: break
            if found: break
        if found: break
    if found: break

if found:
    f1_x, f1_y, f1_rot, d6_x, d6_y, d6_rot = found[0]
    P['F1'] = (f1_x, f1_y, f1_rot, 'F.Cu')
    P['D6'] = (d6_x, d6_y, d6_rot, 'F.Cu')
    
    # Run full verification
    print("\nRunning FULL verification on all 124 components:")
    all_bboxes = {}
    for ref, (x, y, rot, layer) in P.items():
        is_b = (layer == 'B.Cu')
        _, shapes = s.parse_shapes(s.fps[ref])
        all_bboxes[ref] = s.get_world_bbox(ref, is_b, shapes, x, y, rot)
    
    overlaps = []
    refs = list(all_bboxes.keys())
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            if (r1, r2) in s.ALLOWED or (r2, r1) in s.ALLOWED: continue
            b1, b2 = all_bboxes[r1], all_bboxes[r2]
            if b1['layer'] != b2['layer']: continue
            if check_box_overlap(b1, b2):
                overlaps.append((r1, r2))
    
    holes = []
    for hname, (hx, hy) in s.HOLES.items():
        for r, b in all_bboxes.items():
            if r in ['H1', 'H2', 'H3', 'H4']: continue
            cx = max(b['x1'], min(hx, b['x2']))
            cy = max(b['y1'], min(hy, b['y2']))
            if math.hypot(cx - hx, cy - hy) < s.R_KO:
                holes.append((hname, r))

    print(f"FINAL OVERLAPS: {len(overlaps)}")
    for r1, r2 in overlaps: print(" ", r1, "<-->", r2)
    print(f"FINAL HOLE COLLISIONS: {len(holes)}")
    for h, r in holes: print(" ", h, "<-->", r)
