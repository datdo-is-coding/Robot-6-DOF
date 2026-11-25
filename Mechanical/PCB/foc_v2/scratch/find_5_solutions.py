import sys
sys.path.insert(0, 'scratch')
import search_buck_cluster as s

b_l1 = s.s.get_world_bbox('L1', False, s.l1_shapes, 114.5, 92.5, 0)
b_d4 = s.s.get_world_bbox('D4', False, s.d4_shapes, 114.5, 98.0, 0)

obstacles = dict(s.static_boxes)
obstacles['L1'] = b_l1
obstacles['D4'] = b_d4

def is_free(b):
    if s.check_hole(b): return False
    return not any(sbox['layer'] == 'top' and s.check_box_overlap(b, sbox) for sbox in obstacles.values())

solutions = []
for c16_x in [111.0, 112.0, 117.5, 118.0]:
    for c16_y in [y * 0.5 for y in range(176, 208)]:
        b_c16 = s.s.get_world_bbox('C16', False, s.c16_shapes, c16_x, c16_y, 0)
        if not is_free(b_c16): continue
        obstacles['C16'] = b_c16

        for c17_x in [111.0, 112.0, 117.5, 118.0]:
            for c17_y in [y * 0.5 for y in range(176, 208)]:
                b_c17 = s.s.get_world_bbox('C17', False, s.c17_shapes, c17_x, c17_y, 0)
                if not is_free(b_c17): continue
                obstacles['C17'] = b_c17

                for r53_x in [111.0, 112.0, 117.5, 118.0]:
                    for r53_y in [y * 0.5 for y in range(176, 208)]:
                        b_r53 = s.s.get_world_bbox('R53', False, s.r53_shapes, r53_x, r53_y, 0)
                        if not is_free(b_r53): continue
                        obstacles['R53'] = b_r53

                        for r54_x in [111.0, 112.0, 117.5, 118.0]:
                            for r54_y in [y * 0.5 for y in range(176, 208)]:
                                b_r54 = s.s.get_world_bbox('R54', False, s.r54_shapes, r54_x, r54_y, 0)
                                if not is_free(b_r54): continue
                                solutions.append((
                                    (c16_x, c16_y),
                                    (c17_x, c17_y),
                                    (r53_x, r53_y),
                                    (r54_x, r54_y)
                                ))
                                print(f"SOL {len(solutions)}: C16={c16_x, c16_y}, C17={c17_x, c17_y}, R53={r53_x, r53_y}, R54={r54_x, r54_y}")
                                break
                            if len(solutions) >= 5: break
                        if len(solutions) >= 5: break
                        del obstacles['R53']
                    if len(solutions) >= 5: break
                if len(solutions) >= 5: break
                del obstacles['C17']
            if len(solutions) >= 5: break
        if len(solutions) >= 5: break
        del obstacles['C16']
    if len(solutions) >= 5: break

print("Done.")
