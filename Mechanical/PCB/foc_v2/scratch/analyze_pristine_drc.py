import json

with open('scratch/drc_verified_pristine.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

violations = data.get('violations', [])
print(f"Total violations in KiCad DRC: {len(violations)}")

by_type = {}
for v in violations:
    vtype = v.get('type', 'unknown')
    by_type[vtype] = by_type.get(vtype, 0) + 1

print("\nViolation counts by type:")
for t, count in sorted(by_type.items(), key=lambda x: -x[1]):
    print(f"  {t:30s}: {count}")

crtyd_viols = [v for v in violations if v.get('type') == 'courtyards_overlap']
print(f"\nCourtyards overlap violations: {len(crtyd_viols)}")
for v in crtyd_viols:
    items = [it.get('description', '') for it in v.get('items', [])]
    print("  OVERLAP:", " <--> ".join(items))
