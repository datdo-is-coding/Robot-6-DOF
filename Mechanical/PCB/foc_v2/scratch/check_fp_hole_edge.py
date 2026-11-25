import json

with open('scratch/drc_verified_flipped.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

violations = data.get('violations', [])

fp_hole_viols = []
fp_edge_viols = []

for v in violations:
    vtype = v.get('type', '')
    items = v.get('items', [])
    desc_str = " ".join(it.get('description', '') for it in items)
    if 'Pad' in desc_str or 'Footprint' in desc_str:
        if 'hole' in vtype:
            fp_hole_viols.append((vtype, desc_str))
        elif 'edge' in vtype and 'Track' not in desc_str and 'Via' not in desc_str:
            fp_edge_viols.append((vtype, desc_str))

print(f"Footprint Pad vs Hole violations: {len(fp_hole_viols)}")
for vt, d in fp_hole_viols:
    print(f"  {vt}: {d}")

print(f"\nFootprint Pad vs Edge violations: {len(fp_edge_viols)}")
for vt, d in fp_edge_viols:
    print(f"  {vt}: {d}")
