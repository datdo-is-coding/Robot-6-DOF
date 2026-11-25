from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
for r in ['L1', 'D4', 'C16', 'C17', 'U10', 'C6', 'C7', 'C56', 'C57', 'C58', 'R53', 'R54', 'R59', 'R60']:
    is_b, shapes = parse_shapes(fps[r])
    box = get_world_bbox(r, is_b, shapes, fps[r])
    print(f"{r:6s}: bounds=({box['x1']:.2f}, {box['y1']:.2f}) to ({box['x2']:.2f}, {box['y2']:.2f})")
