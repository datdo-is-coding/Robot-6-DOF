import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

from solve_zero_drc_golden import P, HOLES, ALLOWED, get_custom_bbox

fixed_P = {k: v for k, v in P.items() if k not in ['F1', 'D6', 'J11', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58']}

fixed_boxes = {}
for ref, (x, y, rot, layer) in fixed_P.items():
    if layer == 'F.Cu':
        is_b, shapes = parse_shapes(fps[ref])
        fixed_boxes[ref] = get_custom_bbox(ref, is_b, shapes, x, y, rot)

def check_overlap(b1, b2):
    return (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01)

valid_f1 = []
for rot in [0, 90, 180, 270]:
    for x in range(65, 135):
        for y in range(65, 120):
            fx, fy = float(x), float(y)
            b = get_custom_bbox('F1', False, parse_shapes(fps['F1'])[1], fx, fy, rot)
            oob = False
            for px in [b['x1'], b['x2']]:
                for py in [b['y1'], b['y2']]:
                    if py > 120.0 or math.hypot(px - 100.0, py - 100.0) > 34.90:
                        oob = True
                        break
                if oob: break
            if oob: continue
            
            hole_col = False
            for hname, (hx, hy) in HOLES.items():
                cx_box = max(b['x1'], min(hx, b['x2']))
                cy_box = max(b['y1'], min(hy, b['y2']))
                if math.hypot(cx_box - hx, cy_box - hy) < 2.40:
                    hole_col = True
                    break
            if hole_col: continue
            
            col = False
            for r_obs, b_obs in fixed_boxes.items():
                if check_overlap(b, b_obs):
                    col = True
                    break
            if col: continue
            
            valid_f1.append((fx, fy, rot))

print(f"Total valid positions found for F1 on F.Cu: {len(valid_f1)}")
for pos in valid_f1[:15]:
    print("  Valid F1:", pos)
