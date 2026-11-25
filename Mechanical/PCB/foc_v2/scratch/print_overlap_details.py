import json

with open('scratch/current_drc.json') as f:
    d = json.load(f)

v = d.get('violations', [])
overlaps = [item for item in v if item['type'] == 'courtyards_overlap']
print(f"Total courtyards_overlap: {len(overlaps)}")
for o in overlaps:
    items = o.get('items', [])
    desc = [it.get('description', '') for it in items]
    print(f"  Overlap: {desc}")
