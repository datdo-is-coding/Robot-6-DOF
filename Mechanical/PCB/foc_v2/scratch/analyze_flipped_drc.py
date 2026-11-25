import json

with open('scratch/drc_verified_flipped.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

violations = data.get('violations', [])
print(f"Total violations in KiCad DRC: {len(violations)}")

crtyd_viols = [v for v in violations if v.get('type') == 'courtyards_overlap']
print(f"\n==========================================")
print(f"COURTYARDS OVERLAP VIOLATIONS IN KICAD DRC: {len(crtyd_viols)}")
print(f"==========================================")
for v in crtyd_viols:
    items = [it.get('description', '') for it in v.get('items', [])]
    print("  OVERLAP:", " <--> ".join(items))
