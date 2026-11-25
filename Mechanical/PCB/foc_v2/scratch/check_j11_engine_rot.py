from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
for rot in [90, 270]:
    b = get_world_bbox('J11', False, parse_shapes(fps['J11'])[1], 121.0, 99.5, rot)
    print(f"rot={rot}: X=[{b['x1']:.2f}, {b['x2']:.2f}], Y=[{b['y1']:.2f}, {b['y2']:.2f}], cx={b['cx']:.2f}, cy={b['cy']:.2f}")
