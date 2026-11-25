from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
east_refs = ['J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58']
for ref in east_refs:
    is_b, shapes = parse_shapes(fps[ref])
    box0 = get_world_bbox(ref, is_b, shapes, 0, 0, 0)
    box90 = get_world_bbox(ref, is_b, shapes, 0, 0, 90)
    print(f"{ref:5s}: rot=0: {box0['w']:.2f} x {box0['h']:.2f} (x:[{box0['x1']:.2f},{box0['x2']:.2f}], y:[{box0['y1']:.2f},{box0['y2']:.2f}])")
    print(f"       rot=90: {box90['w']:.2f} x {box90['h']:.2f}")
