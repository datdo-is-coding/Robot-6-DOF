import json
from collections import Counter

with open('scratch/drc_d_shape.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

violations = data.get('violations', [])
print(f"Total violations in report: {len(violations)}")

types = Counter(v.get('type') for v in violations)
for t, c in types.most_common():
    print(f"  {t:35s}: {c}")

# Check courtyards_overlap:
c_overlaps = [v for v in violations if v.get('type') == 'courtyards_overlap']
print(f"\nCourtyards overlap violations: {len(c_overlaps)}")
for co in c_overlaps:
    print(" ", co.get('description'))
