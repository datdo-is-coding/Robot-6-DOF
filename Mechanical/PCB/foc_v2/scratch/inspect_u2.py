from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
is_b, shapes = parse_shapes(fps['U2'])
b = get_world_bbox('U2', is_b, shapes, 100.0, 100.0, 0)
print("U2 box:", b)
is_b, shapes = parse_shapes(fps['R61'])
b_r = get_world_bbox('R61', is_b, shapes, 100.0, 96.5, 90)
print("R61 box:", b_r)
