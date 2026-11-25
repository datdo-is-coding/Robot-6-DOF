import json
from collections import Counter

with open('scratch/drc_current.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

violations = data.get('violations', [])
print(f"Total violations in report: {len(violations)}")

types = Counter(v.get('type') for v in violations)
for t, c in types.most_common():
    print(f"  {t:35s}: {c}")

print("\nSample violations for each type:")
shown = set()
for v in violations:
    vt = v.get('type')
    if vt not in shown:
        shown.add(vt)
        print(f"\n--- Type: {vt} ---")
        print(f"  Desc: {v.get('description')}")
        for item in v.get('items', [])[:3]:
            print(f"    Item: {item}")
