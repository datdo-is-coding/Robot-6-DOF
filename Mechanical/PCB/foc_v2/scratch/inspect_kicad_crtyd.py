import json

with open('scratch/drc_final_pure_circle.json') as f:
    d = json.load(f)

for v in d.get('violations', []):
    if v.get('type') == 'courtyards_overlap':
        items = [it.get('description', '') for it in v.get('items', [])]
        print(f"Overlap: {items}")
