from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
print("J7 shapes:", parse_shapes(fps['J7'])[1])
box = get_world_bbox('J7', False, parse_shapes(fps['J7'])[1], 102.0, 128.0, 0)
print("J7 world box:", box)
