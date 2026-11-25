import sys
sys.path.insert(0, 'scratch')
import search_buck_cluster as s

# Fix L1 at (114.5, 92.0, 0)
box_l1 = s.s.get_world_bbox('L1', False, s.l1_shapes, 114.5, 92.0, 0)

# Search D4, C16, C17, R53, R54 in the vicinity
dyn_passives = ['D4', 'C16', 'C17', 'R53', 'R54']
shapes_dict = {
    'D4': s.d4_shapes,
    'C16': s.c16_shapes,
    'C17': s.c17_shapes,
    'R53': s.r53_shapes,
    'R54': s.r54_shapes
}

# Where can D4 go?
# D4 is SMA diode (7x3.5 at rot 0, or 3.5x7 at rot 90)
valid_passives = []
for d4_rot in [0, 90]:
    for d4_x in [x * 0.5 for x in range(224, 240)]: # 112.0 to 119.5
        for d4_y in [y * 0.5 for y in range(192, 208)]: # 96.0 to 104.0
            box_d4 = s.s.get_world_bbox('D4', False, s.d4_shapes, d4_x, d4_y, d4_rot)
            if s.check_hole(box_d4): continue
            if s.check_box_overlap(box_l1, box_d4): continue
            if any(sbox['layer'] == 'top' and s.check_box_overlap(box_d4, sbox) for sbox in s.static_boxes.values()):
                continue
            # D4 is valid!
            # Now C16, C17, R53, R54 are small 0805 and 0603.
            # Can we place C16 at (118.5, 92.0) and C17 at (118.5, 95.0)?
            box_c16 = s.s.get_world_bbox('C16', False, s.c16_shapes, 119.0, 91.5, 90)
            if s.check_hole(box_c16) or s.check_box_overlap(box_l1, box_c16) or s.check_box_overlap(box_d4, box_c16): continue
            if any(sbox['layer'] == 'top' and s.check_box_overlap(box_c16, sbox) for sbox in s.static_boxes.values()): continue

            box_c17 = s.s.get_world_bbox('C17', False, s.c17_shapes, 119.0, 94.5, 90)
            if s.check_hole(box_c17) or s.check_box_overlap(box_l1, box_c17) or s.check_box_overlap(box_d4, box_c17): continue
            if any(sbox['layer'] == 'top' and s.check_box_overlap(box_c17, sbox) for sbox in s.static_boxes.values()): continue

            box_r53 = s.s.get_world_bbox('R53', False, s.r53_shapes, 119.0, 97.0, 0)
            if s.check_hole(box_r53) or s.check_box_overlap(box_l1, box_r53) or s.check_box_overlap(box_d4, box_r53): continue
            if any(sbox['layer'] == 'top' and s.check_box_overlap(box_r53, sbox) for sbox in s.static_boxes.values()): continue

            box_r54 = s.s.get_world_bbox('R54', False, s.r54_shapes, 119.0, 99.0, 0)
            if s.check_hole(box_r54) or s.check_box_overlap(box_l1, box_r54) or s.check_box_overlap(box_d4, box_r54): continue
            if any(sbox['layer'] == 'top' and s.check_box_overlap(box_r54, sbox) for sbox in s.static_boxes.values()): continue

            valid_passives.append((d4_x, d4_y, d4_rot))
            print(f"FOUND COMPLETE CLUSTER: D4=({d4_x}, {d4_y}, {d4_rot}), C16=(119.0, 91.5), C17=(119.0, 94.5), R53=(119.0, 97.0), R54=(119.0, 99.0)")
            break
        if valid_passives: break
    if valid_passives: break

print("Finished search.")
