from exact_crtyd_engine import load_pcb_footprints, parse_shapes

fps = load_pcb_footprints('foc_v2.kicad_pcb')
for r in ['D1', 'R33']:
    print(r, parse_shapes(fps[r])[1])
