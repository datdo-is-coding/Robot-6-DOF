from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
shapes = parse_shapes(fps['C_BULK1'])
print("C_BULK1 shapes:", shapes)
b = get_world_bbox('C_BULK1', False, shapes[1], 73.0, 84.5, 0)
print("World bbox at (73.0, 84.5, 0):", b)
