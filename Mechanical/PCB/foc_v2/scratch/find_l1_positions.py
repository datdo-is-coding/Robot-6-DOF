import sys
sys.path.insert(0, 'scratch')
import search_buck_cluster as s

valid_l1 = []
for l1_rot in [0, 90]:
    for l1_x in [x * 0.5 for x in range(220, 260)]: # 110 to 130
        for l1_y in [y * 0.5 for y in range(160, 240)]: # 80 to 120
            box_l1 = s.s.get_world_bbox('L1', False, s.l1_shapes, l1_x, l1_y, l1_rot)
            if s.check_hole(box_l1): continue
            colls = [sref for sref, sbox in s.static_boxes.items() if sbox['layer'] == 'top' and s.check_box_overlap(box_l1, sbox)]
            if not colls:
                valid_l1.append((l1_x, l1_y, l1_rot))

print(f"Total valid positions for L1 alone: {len(valid_l1)}")
for p in valid_l1[:15]:
    print(f"  L1 at ({p[0]:.1f}, {p[1]:.1f}, {p[2]})")
