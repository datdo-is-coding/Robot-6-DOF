from exact_crtyd_engine import load_pcb_footprints, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

targets = ['J7', 'J8', 'J9', 'J10', 'J11', 'H1', 'H2', 'H3', 'H4', 'Q1', 'IC1', 'U1', 'U2', 'C_BULK1', 'C63']
for ref in targets:
    fp = fps.get(ref)
    if fp:
        print(f"Ref: {ref:8s} Footprint: {fp['name']}")
        print(f"  crtyd_poly points: {len(fp['crtyd_poly'])}, pads: {len(fp['pads'])}, lines: {len(fp['lines'])}")
        # Print bounding box at (0, 0, rot=0)
        min_x, min_y, max_x, max_y = get_world_bbox(fp, 0, 0, 0)
        print(f"  bbox at (0,0 rot=0): X=[{min_x:.3f}, {max_x:.3f}] (w={max_x-min_x:.3f}), Y=[{min_y:.3f}, {max_y:.3f}] (h={max_y-min_y:.3f})")
