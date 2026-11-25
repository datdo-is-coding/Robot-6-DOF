import json

with open('scratch/drc_check.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== DRC COURTYARD OVERLAPS ===")
for v in d.get('violations', []):
    if v.get('type') == 'courtyards_overlap':
        items = v.get('items', [])
        desc = v.get('description', '')
        pos = v.get('pos', {})
        print(f"Overlap: {desc}")
        for it in items:
            print(f"   item: {it.get('description', '')}")

print("\n=== DRC INVALID OUTLINE ===")
for v in d.get('violations', []):
    if v.get('type') == 'invalid_outline':
        print(v)
