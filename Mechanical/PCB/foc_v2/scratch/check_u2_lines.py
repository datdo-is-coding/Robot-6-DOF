from exact_crtyd_engine import load_pcb_footprints

fps = load_pcb_footprints('foc_v2.kicad_pcb')
for idx, l in enumerate(fps['U2'][:10]):
    print(idx, repr(l))
