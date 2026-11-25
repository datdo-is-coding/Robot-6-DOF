import os

work_dir = 'work/2026-11-13-pcb-layout'
for f in os.listdir(work_dir):
    if f.endswith('.kicad_pcb'):
        p = os.path.join(work_dir, f)
        with open(p, 'r', encoding='utf-8') as fp:
            t = fp.read()
        vias = t.count('(via ')
        segs = t.count('(segment ')
        fps = t.count('(footprint ')
        print(f"{f:<35}: {vias:>4} vias, {segs:>5} segments, {fps:>4} footprints")
