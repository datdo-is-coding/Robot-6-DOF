from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
for r in ['R47', 'R1', 'R2']:
    is_b, shapes = parse_shapes(fps[r])
    print(r, shapes)
