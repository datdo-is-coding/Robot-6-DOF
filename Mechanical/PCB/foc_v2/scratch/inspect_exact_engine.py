import exact_crtyd_engine

fps = exact_crtyd_engine.load_pcb_footprints('scratch/git_raw.kicad_pcb')
print(type(fps))
if isinstance(fps, dict):
    k = list(fps.keys())[0]
    print(k, type(fps[k]), fps[k])
elif isinstance(fps, list):
    print(len(fps), type(fps[0]), fps[0])
