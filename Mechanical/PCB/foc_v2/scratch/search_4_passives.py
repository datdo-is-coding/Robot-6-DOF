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

# Search positions for C16, C17, R53, R54
# C16, C17 are 0805 caps (1.96 x 3.76 at rot 90, or 3.76 x 1.96 at rot 0)
# R53, R54 are 0603 resistors (3.36 x 1.90 at rot 0, or 1.90 x 3.36 at rot 90)

found = []
# Grid search in region x in [110..122], y in [86..104]
for rot_c in [0, 90]:
    for cx in [x * 0.5 for x in range(220, 244)]:
        for cy in [y * 0.5 for y in range(172, 210)]:
            b_c16 = s.s.get_world_bbox('C16', False, s.c16_shapes, cx, cy, rot_c)
            if not is_free(b_c16): continue
            obstacles['C16'] = b_c16
            
            for rot_c2 in [0, 90]:
                for cx2 in [x * 0.5 for x in range(220, 244)]:
                    for cy2 in [y * 0.5 for y in range(172, 210)]:
                        b_c17 = s.s.get_world_bbox('C17', False, s.c17_shapes, cx2, cy2, rot_c2)
                        if not is_free(b_c17): continue
                        obstacles['C17'] = b_c17

                        for rot_r in [0, 90]:
                            for rx in [x * 0.5 for x in range(220, 244)]:
                                for ry in [y * 0.5 for y in range(172, 210)]:
                                    b_r53 = s.s.get_world_bbox('R53', False, s.r53_shapes, rx, ry, rot_r)
                                    if not is_free(b_r53): continue
                                    obstacles['R53'] = b_r53

                                    for rot_r2 in [0, 90]:
                                        for rx2 in [x * 0.5 for x in range(220, 244)]:
                                            for ry2 in [y * 0.5 for y in range(172, 210)]:
                                                b_r54 = s.s.get_world_bbox('R54', False, s.r54_shapes, rx2, ry2, rot_r2)
                                                if not is_free(b_r54): continue
                                                found.append((
                                                    (cx, cy, rot_c),
                                                    (cx2, cy2, rot_c2),
                                                    (rx, ry, rot_r),
                                                    (rx2, ry2, rot_r2)
                                                ))
                                                print(f"FOUND! C16=({cx}, {cy}, {rot_c}), C17=({cx2}, {cy2}, {rot_c2}), R53=({rx}, {ry}, {rot_r}), R54=({rx2}, {ry2}, {rot_r2})")
                                                break
                                            if found: break
                                        if found: break
                                    if found: break
                                    del obstacles['R53']
                                if found: break
                            if found: break
                        if found: break
                        del obstacles['C17']
                    if found: break
                if found: break
            if found: break
            del obstacles['C16']
        if found: break
    if found: break

print("Done. Found count:", len(found))
