from exact_crtyd_engine import load_pcb_footprints

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
print(f"Total footprints in git_raw: {len(fps)}")

by_prefix = {}
for ref in fps:
    prefix = ''.join([c for c in ref if c.isalpha()])
    by_prefix[prefix] = by_prefix.get(prefix, 0) + 1

for p, c in sorted(by_prefix.items()):
    print(f"  {p:10s}: {c:3d}")
