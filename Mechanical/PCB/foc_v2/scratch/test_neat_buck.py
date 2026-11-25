import sys
sys.path.insert(0, 'scratch')
import search_buck_cluster as s

b_l1  = s.s.get_world_bbox('L1', False, s.l1_shapes, 114.5, 92.5, 0)
b_d4  = s.s.get_world_bbox('D4', False, s.d4_shapes, 114.5, 98.0, 0)
b_c16 = s.s.get_world_bbox('C16', False, s.c16_shapes, 112.5, 101.5, 90)
b_c17 = s.s.get_world_bbox('C17', False, s.c17_shapes, 115.0, 101.5, 90)
b_r53 = s.s.get_world_bbox('R53', False, s.r53_shapes, 117.5, 101.0, 0)
b_r54 = s.s.get_world_bbox('R54', False, s.r54_shapes, 117.5, 103.0, 0)

test_boxes = {
    'L1': b_l1,
    'D4': b_d4,
    'C16': b_c16,
    'C17': b_c17,
    'R53': b_r53,
    'R54': b_r54
}

overlaps = []
holes = []
for ref, b in test_boxes.items():
    if s.check_hole(b): holes.append(('HOLE', ref))
    for sref, sbox in s.static_boxes.items():
        if sbox['layer'] == 'top' and s.check_box_overlap(b, sbox):
            overlaps.append((ref, sref))

refs = list(test_boxes.keys())
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        if s.check_box_overlap(test_boxes[refs[i]], test_boxes[refs[j]]):
            overlaps.append((refs[i], refs[j]))

print(f"Overlaps: {len(overlaps)}")
for r1, r2 in overlaps: print(" ", r1, "<-->", r2)
print(f"Holes: {len(holes)}")
