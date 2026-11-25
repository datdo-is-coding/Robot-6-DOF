from exact_crtyd_engine import load_pcb_footprints, parse_shapes

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
bottom_refs = []
top_refs = []
for ref, lines in fps.items():
    is_bottom, shapes = parse_shapes(lines)
    if is_bottom:
        bottom_refs.append(ref)
    else:
        top_refs.append(ref)

print(f"Top refs ({len(top_refs)}): {top_refs}")
print(f"Bottom refs ({len(bottom_refs)}): {bottom_refs}")
