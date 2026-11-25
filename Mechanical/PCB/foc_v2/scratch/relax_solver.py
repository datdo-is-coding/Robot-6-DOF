import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's import P from solve_all_zero_perfect
from solve_all_zero_perfect import P, HOLES, ALLOWED, get_custom_bbox, eval_zero

print("Starting relaxation optimizer...")

# Locked components that MUST NOT MOVE:
LOCKED = {
    'H1', 'H2', 'H3', 'H4', # Mounting holes PCD 44
    'U2',                   # Encoder center (100, 100)
    'J7', 'J8', 'J9', 'J10',# South connectors
    'J1', 'J2', 'J3',       # Motor wire pads
    'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', # 6 MOSFETs row
    'R47', 'R48', 'R49',    # 3 Shunts row
    'IC1',                  # Gate driver
    'U1',                   # MCU
    'C_BULK1', 'C63'        # Bulk caps
}

# Net-ties must track their shunts:
# NT1, NT2 track R47; NT3, NT4 track R48; NT5, NT6 track R49.

# Let's write a relaxation loop:
best_P = dict(P)

for iteration in range(500):
    ov, he, oob, bboxes = eval_zero(best_P)
    if len(ov) == 0 and len(he) == 0 and len(oob) == 0:
        print(f"SUCCESS AT ITERATION {iteration}!")
        break
    
    # Process overlaps:
    moved = False
    for r1, r2, dx, dy in ov:
        # choose component to move:
        cand = None
        if r1 not in LOCKED and r2 in LOCKED:
            cand = r1
            other = r2
        elif r2 not in LOCKED and r1 in LOCKED:
            cand = r2
            other = r1
        elif r1 not in LOCKED and r2 not in LOCKED:
            cand = r1 if dx < dy else r2
            other = r2 if cand == r1 else r1
        
        if cand:
            b_c = bboxes[cand]
            b_o = bboxes[other]
            # push cand away from other
            cx_c, cy_c = (b_c['x1'] + b_c['x2'])/2, (b_c['y1'] + b_c['y2'])/2
            cx_o, cy_o = (b_o['x1'] + b_o['x2'])/2, (b_o['y1'] + b_o['y2'])/2
            
            x, y, rot, layer = best_P[cand]
            step = 0.25
            if dx < dy:
                # push along X
                new_x = x + (step if cx_c >= cx_o else -step)
                best_P[cand] = (round(new_x, 3), y, rot, layer)
            else:
                # push along Y
                new_y = y + (step if cy_c >= cy_o else -step)
                best_P[cand] = (x, round(new_y, 3), rot, layer)
            moved = True

    # Process hole errors:
    for h, r, pen in he:
        if r not in LOCKED:
            hx, hy = HOLES[h]
            x, y, rot, layer = best_P[r]
            ang = math.atan2(y - hy, x - hx)
            new_x = x + 0.3 * math.cos(ang)
            new_y = y + 0.3 * math.sin(ang)
            best_P[r] = (round(new_x, 3), round(new_y, 3), rot, layer)
            moved = True

    # Process OOB:
    for r, msg in oob:
        if r not in LOCKED:
            x, y, rot, layer = best_P[r]
            # push towards center (100, 100)
            ang = math.atan2(100.0 - y, 100.0 - x)
            new_x = x + 0.3 * math.cos(ang)
            new_y = y + 0.3 * math.sin(ang)
            best_P[r] = (round(new_x, 3), round(new_y, 3), rot, layer)
            moved = True

    if iteration % 20 == 0:
        print(f"Iter {iteration:3d}: Overlaps={len(ov)}, Holes={len(he)}, OOB={len(oob)}")

ov, he, oob, _ = eval_zero(best_P)
print(f"Final state: Overlaps={len(ov)}, Holes={len(he)}, OOB={len(oob)}")
