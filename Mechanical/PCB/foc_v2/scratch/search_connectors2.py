import math
from itertools import permutations

h1_x, h1_y = 115.556, 115.556
h2_x, h2_y = 84.444, 115.556

def get_box(cname, px, py):
    if cname in ['J8', 'J9']:
        return (px - 2.56, px + 7.56, py - 2.41, py + 9.31)
    elif cname == 'J10':
        return (px - 2.56, px + 12.56, py - 2.41, py + 9.31)
    elif cname == 'J7':
        return (px - 5.32, px + 5.32, py - 4.85, py + 4.18)

def dist_box_pt(box, px, py):
    x1, x2, y1, y2 = box
    cx = max(x1, min(px, x2))
    cy = max(y1, min(py, y2))
    return math.hypot(cx - px, cy - py)

def inside_board(box, y_edge, r_board=35.0):
    x1, x2, y1, y2 = box
    if y2 > y_edge + 0.05:
        return False
    for x in [x1, x2]:
        for y in [y1, y2]:
            if math.hypot(x - 100.0, y - 100.0) > r_board:
                return False
    return True

conns = ['J8', 'J9', 'J7', 'J10']
# We specifically prefer CAN_IN (J8) and CAN_OUT (J9) to be on the sides, or CAN together
# Common orders:
# 1. J8, J7, J10, J9  (CAN_IN on West, Type-C center-left, SWD center-right, CAN_OUT on East)
# 2. J8, J9, J7, J10  (CAN together on West, Type-C center, SWD East)
# 3. J8, J10, J7, J9
# Let's test all orders!

valid_solutions = []

# Try different y_edge
for y_edge in [119.5, 120.0, 120.2, 120.5, 121.0]:
    py_xh = y_edge - 9.31
    py_typec = y_edge - 4.18
    
    for perm in permutations(conns):
        # We want to place c0, c1, c2, c3 from left to right
        # c0 must be inside board and not collide with H2, H1
        # c1 must be > c0 + gap and not collide with H2, H1
        # etc.
        # Let's do a recursive or forward scan
        def solve_placement(idx, current_x_min, placed):
            if idx == 4:
                return [placed]
            cname = perm[idx]
            py = py_typec if cname == 'J7' else py_xh
            sols = []
            # step through possible x positions
            # x ranges from current_x_min to 125.0
            x = current_x_min
            while x <= 126.0:
                box = get_box(cname, x, py)
                # check inside board
                if inside_board(box, y_edge):
                    # check clearance to H1 and H2
                    d_h1 = dist_box_pt(box, h1_x, h1_y)
                    d_h2 = dist_box_pt(box, h2_x, h2_y)
                    if d_h1 >= 2.45 and d_h2 >= 2.45:
                        # valid!
                        # next min_x is box[1] + 0.5 (for spacing)
                        # if xh: pin offset
                        next_res = solve_placement(idx + 1, box[1] + 0.6, placed + [(cname, x, py, box)])
                        if next_res:
                            return next_res # take first valid pack
                x += 0.2
            return []

        res = solve_placement(0, 71.0, [])
        if res:
            valid_solutions.append((y_edge, perm, res[0]))

print(f"Total valid solutions found: {len(valid_solutions)}")
for y_edge, perm, sol in valid_solutions[:10]:
    print(f"\ny_edge = {y_edge}, order = {perm}:")
    for cname, px, py, box in sol:
        d_h1 = dist_box_pt(box, h1_x, h1_y)
        d_h2 = dist_box_pt(box, h2_x, h2_y)
        print(f"  {cname:5s}: at=({px:6.2f}, {py:6.2f}), X=[{box[0]:6.2f}, {box[1]:6.2f}], dH2={d_h2:.2f}, dH1={d_h1:.2f}")
