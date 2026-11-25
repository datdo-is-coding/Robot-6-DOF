import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)
# Clean base
P['J8']  = (74.5, 122.5, 0, 'F.Cu')
P['J9']  = (86.0, 122.5, 0, 'F.Cu')
P['J7']  = (100.0, 128.0, 0, 'F.Cu')
P['J10'] = (109.5, 122.5, 0, 'F.Cu')

P['J1'] = (88.0, 69.5, 0, 'F.Cu')
P['J2'] = (100.0, 69.0, 0, 'F.Cu')
P['J3'] = (112.0, 69.5, 0, 'F.Cu')

P['C_BUS1'] = (82.5, 70.0, 0, 'F.Cu')
P['C_BUS2'] = (94.0, 70.0, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 70.0, 0, 'F.Cu')

P['Q1'] = (83.5, 75.8, 90, 'F.Cu')
P['Q2'] = (90.1, 75.8, 270, 'F.Cu')
P['Q3'] = (96.7, 75.8, 90, 'F.Cu')
P['Q4'] = (103.3, 75.8, 270, 'F.Cu')
P['Q5'] = (109.9, 75.8, 90, 'F.Cu')
P['Q6'] = (116.5, 75.8, 270, 'F.Cu')

P['R1'] = (83.5, 80.6, 0, 'F.Cu')
P['R2'] = (90.1, 80.6, 0, 'F.Cu')
P['R3'] = (96.7, 80.6, 0, 'F.Cu')
P['R4'] = (103.3, 80.6, 0, 'F.Cu')
P['R5'] = (109.9, 80.6, 0, 'F.Cu')
P['R7'] = (116.5, 80.6, 0, 'F.Cu')

P['C_BULK1'] = (77.0, 85.0, 180, 'F.Cu')
P['C63']     = (123.0, 85.0, 0, 'F.Cu')

P['R47'] = (93.0, 85.3, 90, 'F.Cu')
P['R48'] = (100.0, 85.3, 90, 'F.Cu')
P['R49'] = (107.0, 85.3, 90, 'F.Cu')

P['NT1'] = (92.5, 85.3, 90, 'F.Cu')
P['NT2'] = (93.5, 85.3, 90, 'F.Cu')
P['NT3'] = (99.5, 85.3, 90, 'F.Cu')
P['NT4'] = (100.5, 85.3, 90, 'F.Cu')
P['NT5'] = (106.5, 85.3, 90, 'F.Cu')
P['NT6'] = (107.5, 85.3, 90, 'F.Cu')

P['IC1'] = (100.0, 93.5, 0, 'F.Cu')

P['J11'] = (122.0, 103.5, 270, 'F.Cu')
P['F1']  = (124.5, 121.5, 90, 'F.Cu')
P['D6']  = (126.5, 127.5, 0, 'F.Cu')

P['R55'] = (109.5, 90.0, 0, 'F.Cu')
P['R56'] = (109.5, 91.8, 0, 'F.Cu')
P['R57'] = (109.5, 93.6, 0, 'F.Cu')
P['R58'] = (109.5, 95.4, 0, 'F.Cu')
P['R59'] = (109.5, 97.2, 0, 'F.Cu')
P['R60'] = (109.5, 99.0, 0, 'F.Cu')
P['TP3'] = (109.5, 101.5, 0, 'F.Cu')

# Now components to place: L1, D4, C16, C17, R53, R54
# Let's find static obstacles:
static_refs = [r for r in P.keys() if r not in ['L1', 'D4', 'C16', 'C17', 'R53', 'R54']]
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

_, l1_shapes = s.parse_shapes(s.fps['L1'])
_, d4_shapes = s.parse_shapes(s.fps['D4'])
_, c16_shapes = s.parse_shapes(s.fps['C16'])
_, c17_shapes = s.parse_shapes(s.fps['C17'])
_, r53_shapes = s.parse_shapes(s.fps['R53'])
_, r54_shapes = s.parse_shapes(s.fps['R54'])

print("Searching for valid placement of L1, D4, C16, C17, R53, R54...")
# Let's search L1 position
valid_configs = []
for l1_rot in [0, 90]:
    for l1_x in [x * 0.5 for x in range(224, 240)]: # 112.0 to 119.5
        for l1_y in [y * 0.5 for y in range(176, 196)]: # 88.0 to 97.5
            box_l1 = s.get_world_bbox('L1', False, l1_shapes, l1_x, l1_y, l1_rot)
            if check_hole(box_l1): continue
            if any(sbox['layer'] == 'top' and check_box_overlap(box_l1, sbox) for sbox in static_boxes.values()):
                continue
            # L1 is free! Now test D4
            for d4_rot in [0, 90]:
                for d4_x in [x * 0.5 for x in range(224, 240)]:
                    for d4_y in [y * 0.5 for y in range(180, 204)]:
                        box_d4 = s.get_world_bbox('D4', False, d4_shapes, d4_x, d4_y, d4_rot)
                        if check_hole(box_d4): continue
                        if check_box_overlap(box_l1, box_d4): continue
                        if any(sbox['layer'] == 'top' and check_box_overlap(box_d4, sbox) for sbox in static_boxes.values()):
                            continue
                        # D4 is free! Test C16, C17
                        for c16_y in [y * 0.5 for y in range(182, 206)]:
                            box_c16 = s.get_world_bbox('C16', False, c16_shapes, 118.0, c16_y, 90)
                            if check_hole(box_c16): continue
                            if check_box_overlap(box_l1, box_c16) or check_box_overlap(box_d4, box_c16): continue
                            if any(sbox['layer'] == 'top' and check_box_overlap(box_c16, sbox) for sbox in static_boxes.values()): continue
                            
                            c17_y = c16_y + 3.0
                            box_c17 = s.get_world_bbox('C17', False, c17_shapes, 118.0, c17_y, 90)
                            if check_hole(box_c17): continue
                            if check_box_overlap(box_l1, box_c17) or check_box_overlap(box_d4, box_c17): continue
                            if any(sbox['layer'] == 'top' and check_box_overlap(box_c17, sbox) for sbox in static_boxes.values()): continue
                            
                            # Test R53, R54
                            r53_y = c17_y + 2.5
                            box_r53 = s.get_world_bbox('R53', False, r53_shapes, 118.0, r53_y, 0)
                            if check_hole(box_r53): continue
                            if check_box_overlap(box_l1, box_r53) or check_box_overlap(box_d4, box_r53): continue
                            if any(sbox['layer'] == 'top' and check_box_overlap(box_r53, sbox) for sbox in static_boxes.values()): continue

                            r54_y = r53_y + 2.0
                            box_r54 = s.get_world_bbox('R54', False, r54_shapes, 118.0, r54_y, 0)
                            if check_hole(box_r54): continue
                            if check_box_overlap(box_l1, box_r54) or check_box_overlap(box_d4, box_r54): continue
                            if any(sbox['layer'] == 'top' and check_box_overlap(box_r54, sbox) for sbox in static_boxes.values()): continue

                            valid_configs.append((l1_x, l1_y, l1_rot, d4_x, d4_y, d4_rot, c16_y, c17_y, r53_y, r54_y))
                            print(f"FOUND VALID CONFIG: L1=({l1_x}, {l1_y}, {l1_rot}), D4=({d4_x}, {d4_y}, {d4_rot})")
                            break
                        if valid_configs: break
                    if valid_configs: break
                if valid_configs: break
            if valid_configs: break
        if valid_configs: break
    if valid_configs: break

print(f"Total valid configurations found: {len(valid_configs)}")
