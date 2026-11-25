from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
b_j10 = get_world_bbox('J10', False, parse_shapes(fps['J10'])[1], 113.5, 122.5, 0)
print("J10:", b_j10)
