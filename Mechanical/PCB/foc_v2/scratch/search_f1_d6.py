import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

base_P = dict(s.P)

def check_all(P_cand):
    bboxes = {}
    for ref, (x, y, rot, layer) in P_cand.items():
        is_b = (layer == 'B.Cu')
        _, shapes = s.parse_shapes(s.fps[ref])
        box = s.get_world_bbox(ref, is_b, shapes, x, y, rot)
        bboxes[ref] = box

    overlaps = []
    refs = list(bboxes.keys())
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            if (r1, r2) in s.ALLOWED or (r2, r1) in s.ALLOWED:
                continue
            b1, b2 = bboxes[r1], bboxes[r2]
            if b1['layer'] != b2['layer']:
                continue
            if (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
                b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01):
                dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
                dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
                overlaps.append((r1, r2, dx, dy))

    hole_errs = []
    for hname, (hx, hy) in s.HOLES.items():
        for r, b in bboxes.items():
            if r in ['H1', 'H2', 'H3', 'H4']: continue
            cx = max(b['x1'], min(hx, b['x2']))
            cy = max(b['y1'], min(hy, b['y2']))
            d = math.hypot(cx - hx, cy - hy)
            if d < s.R_KO:
                hole_errs.append((hname, r, d))

    return overlaps, hole_errs, bboxes

# Let's fix base positions for the clean parts:
# C63 shifted slightly up to 76.0
base_P['C63'] = (124.5, 76.0, 0, 'F.Cu')

# Buck components around IC1:
# IC1 is at (100.0, 93.5).
# Buck SW_BK is on the right side.
# Let's place L1, D4, C16, C17, R53, R54 in a neat cluster between IC1 and J11:
base_P['L1']  = (123.5, 89.0, 0, 'F.Cu')
base_P['D4']  = (115.0, 92.5, 0, 'F.Cu')
base_P['C16'] = (114.5, 96.2, 90, 'F.Cu')
base_P['C17'] = (114.5, 100.2, 90, 'F.Cu')
base_P['R53'] = (118.0, 96.2, 0, 'F.Cu')
base_P['R54'] = (118.0, 98.5, 0, 'F.Cu')
base_P['J11'] = (122.0, 103.5, 270, 'F.Cu')

# Now search for F1 and D6:
print("Searching for F1 and D6 valid positions...")
found = []
for f1_rot in [90, 270]:
    for f1_x in [126.0, 126.5, 127.0, 127.5, 128.0]:
        for f1_y in [112.0, 113.0, 114.0, 115.0, 116.0, 117.0]:
            for d6_rot in [0, 90, 270]:
                for d6_x in [122.0, 124.0, 125.0, 126.0, 127.0, 128.0]:
                    for d6_y in [122.0, 123.0, 124.0, 125.0, 126.0, 127.0]:
                        test_P = dict(base_P)
                        test_P['F1'] = (f1_x, f1_y, f1_rot, 'F.Cu')
                        test_P['D6'] = (d6_x, d6_y, d6_rot, 'F.Cu')
                        overlaps, holes, bboxes = check_all(test_P)
                        if len(overlaps) == 0 and len(holes) == 0:
                            # Also check if F1 and D6 are within board boundary (x < 134.5, y < 131.0)
                            b_f1 = bboxes['F1']
                            b_d6 = bboxes['D6']
                            if b_f1['x2'] <= 134.5 and b_d6['x2'] <= 134.5 and b_f1['y2'] <= 132.0 and b_d6['y2'] <= 132.0:
                                found.append((f1_x, f1_y, f1_rot, d6_x, d6_y, d6_rot))
                                print(f"SUCCESS: F1=({f1_x}, {f1_y}, {f1_rot}), D6=({d6_x}, {d6_y}, {d6_rot})")
                                break
                    if found: break
                if found: break
            if found: break
        if found: break
    if found: break

if not found:
    print("No immediate match with exact grid, testing broader search...")
    # Let's inspect what conflicts occurred with the best candidate
    test_P = dict(base_P)
    test_P['F1'] = (127.0, 113.0, 270, 'F.Cu')
    test_P['D6'] = (125.0, 126.0, 90, 'F.Cu')
    overlaps, holes, _ = check_all(test_P)
    print(f"Conflicts ({len(overlaps)}):")
    for r1, r2, dx, dy in overlaps:
        print(f"  {r1} <--> {r2}: dx={dx:.2f}, dy={dy:.2f}")
    print(f"Holes ({len(holes)}):")
    for h, r, d in holes:
        print(f"  {h} <--> {r}: dist={d:.2f}")
