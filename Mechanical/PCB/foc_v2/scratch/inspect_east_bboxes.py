from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
east_refs = ['J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58']
for r in east_refs:
    is_b, shapes = parse_shapes(fps[r])
    b = get_world_bbox(r, is_b, shapes, 0, 0, 0)
    print(f"{r:6s}: w={b['w']:.2f}, h={b['h']:.2f}, x=[{b['x1']:.2f}, {b['x2']:.2f}], y=[{b['y1']:.2f}, {b['y2']:.2f}]")
