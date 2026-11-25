from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
for rot in [0, 90, 180, 270]:
    is_b, shapes = parse_shapes(fps['J11'])
    b = get_world_bbox('J11', is_b, shapes, 100, 100, rot)
    print(f"J11 rot={rot:3d}: w={b['w']:.2f}, h={b['h']:.2f}, x=[{b['x1']:.2f}, {b['x2']:.2f}], y=[{b['y1']:.2f}, {b['y2']:.2f}]")

for rot in [0, 90, 180, 270]:
    is_b, shapes = parse_shapes(fps['F1'])
    b = get_world_bbox('F1', is_b, shapes, 100, 100, rot)
    print(f"F1  rot={rot:3d}: w={b['w']:.2f}, h={b['h']:.2f}, x=[{b['x1']:.2f}, {b['x2']:.2f}], y=[{b['y1']:.2f}, {b['y2']:.2f}]")
