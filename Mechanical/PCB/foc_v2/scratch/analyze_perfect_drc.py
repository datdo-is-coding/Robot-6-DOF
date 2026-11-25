import json

with open('scratch/drc_verified_perfect.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

violations = data.get('violations', [])

crtyd_viols = [v for v in violations if v.get('type') == 'courtyards_overlap']
print(f"==========================================")
print(f"COURTYARDS OVERLAP VIOLATIONS: {len(crtyd_viols)}")
print(f"==========================================")
for v in crtyd_viols:
    items = [it.get('description', '') for it in v.get('items', [])]
    print("  OVERLAP:", " <--> ".join(items))

fp_edge_viols = []
for v in violations:
    vtype = v.get('type', '')
    items = v.get('items', [])
    desc_str = " ".join(it.get('description', '') for it in items)
    if 'copper_edge' in vtype and ('Pad' in desc_str or 'Footprint' in desc_str) and 'Track' not in desc_str and 'Via' not in desc_str:
        fp_edge_viols.append(desc_str)

print(f"\n==========================================")
print(f"FOOTPRINT PAD COPPER EDGE VIOLATIONS: {len(fp_edge_viols)}")
print(f"==========================================")
for d in fp_edge_viols:
    print("  EDGE:", d)
