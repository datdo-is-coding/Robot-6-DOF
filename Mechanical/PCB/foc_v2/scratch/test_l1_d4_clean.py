import sys
sys.path.insert(0, 'scratch')
import search_buck_cluster as s

# Let's test a clean, compact layout for buck components:
# L1 is at (114.5, 92.5, 0) -> x in [111.0, 118.0], y in [89.25, 95.75]
# Let's check D4:
# D4 at (114.5, 98.0, 0) -> x in [111.0, 118.0], y in [96.25, 99.75]
# Let's check if D4 at (114.5, 98.0) collides with anything:
b_l1 = s.s.get_world_bbox('L1', False, s.l1_shapes, 114.5, 92.5, 0)
b_d4 = s.s.get_world_bbox('D4', False, s.d4_shapes, 114.5, 98.0, 0)

print("L1 collisions:")
for sref, sbox in s.static_boxes.items():
    if sbox['layer'] == 'top' and s.check_box_overlap(b_l1, sbox):
        print(" ", sref, sbox)

print("D4 collisions:")
for sref, sbox in s.static_boxes.items():
    if sbox['layer'] == 'top' and s.check_box_overlap(b_d4, sbox):
        print(" ", sref, sbox)

print("Check holes:")
print(" L1 hole:", s.check_hole(b_l1))
print(" D4 hole:", s.check_hole(b_d4))
