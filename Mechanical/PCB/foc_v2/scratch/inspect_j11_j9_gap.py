from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

is_b9, sh9 = parse_shapes(fps['J9'])
b9 = get_world_bbox('J9', is_b9, sh9, 121.0, 110.30, 0)
print("J9 bbox:", b9)

is_b11, sh11 = parse_shapes(fps['J11'])
for y in [101.0, 101.5, 101.8, 102.0, 102.2, 102.5]:
    b11 = get_world_bbox('J11', is_b11, sh11, 115.5, y, 270)
    print(f"J11 at Y={y:5.2f}: y=[{b11['y1']:.2f}, {b11['y2']:.2f}], gap to J9 y1({b9['y1']:.2f}) = {b9['y1'] - b11['y2']:.2f}")
