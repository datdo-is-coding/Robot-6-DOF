from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
b_h3 = get_world_bbox('H3', False, parse_shapes(fps['H3'])[1], 84.444, 84.444, 0)
b_r1 = get_world_bbox('R1', False, parse_shapes(fps['R1'])[1], 88.5, 80.8, 0)
print("H3:", b_h3)
print("R1:", b_r1)
