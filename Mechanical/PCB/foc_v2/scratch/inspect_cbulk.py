from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
lines = fps['C_BULK1']
for l in lines:
    if 'F.CrtYd' in l or 'B.CrtYd' in l:
        print(l.strip())
is_b, shapes = parse_shapes(lines)
print("Shapes:", shapes)
b = get_world_bbox('C_BULK1', False, shapes, 76.5, 86.5, 180)
print("BBox:", b)
