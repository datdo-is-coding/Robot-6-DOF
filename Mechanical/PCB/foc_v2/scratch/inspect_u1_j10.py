from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
is_b, shapes = parse_shapes(fps['U1'])
b_u1 = get_world_bbox('U1', is_b, shapes, 100.0, 101.5, 0)
print("U1 bbox at (100, 101.5):", b_u1)

is_b, shapes = parse_shapes(fps['J10'])
b_j10 = get_world_bbox('J10', is_b, shapes, 100.25, 111.0, 0)
print("J10 bbox at (100.25, 111):", b_j10)
