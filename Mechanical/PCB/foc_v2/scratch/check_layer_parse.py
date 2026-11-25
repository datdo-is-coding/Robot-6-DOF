from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
for r in ['U2', 'C14', 'R61', 'TP2', 'TP3', 'U1']:
    is_b, shapes = parse_shapes(fps[r])
    box = get_world_bbox(r, is_b, shapes, 100, 100, 0)
    print(f"{r:6s}: is_bottom={is_b}, box_layer={box['layer']}")
