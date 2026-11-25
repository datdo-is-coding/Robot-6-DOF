from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
b_j8 = get_world_bbox('J8', False, parse_shapes(fps['J8'])[1], 78.5, 122.5, 0)
b_j9 = get_world_bbox('J9', False, parse_shapes(fps['J9'])[1], 89.5, 122.5, 0)
print("J8:", b_j8)
print("J9:", b_j9)
