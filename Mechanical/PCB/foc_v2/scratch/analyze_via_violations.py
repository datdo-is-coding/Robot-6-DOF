import json
from collections import Counter

with open('scratch/drc_via_injection.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

violations = d.get('violations', [])
severities = Counter()
types = Counter()
errors = []

for v in violations:
    s = v.get('severity', 'unknown')
    t = v.get('type', 'unknown')
    severities[s] += 1
    types[t] += 1
    if s == 'error':
        errors.append(v)

print("Severities:", severities)
print("Violation Types:", types)
print(f"\nTotal Errors: {len(errors)}")
for e in errors[:10]:
    print(f"  [{e.get('type')}] {e.get('description')}:")
    for it in e.get('items', []):
        print(f"     - {it.get('description')} at ({it.get('pos', {}).get('x')}, {it.get('pos', {}).get('y')})")
