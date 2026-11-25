import json

with open('scratch/drc_d_shape.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for v in data.get('violations', []):
    if v.get('type') == 'invalid_outline':
        print("=== INVALID OUTLINE ===")
        print("Description:", v.get('description'))
        for item in v.get('items', []):
            print(" ", item)
    elif v.get('type') == 'courtyards_overlap':
        print("=== COURTYARD OVERLAP ===")
        print("Description:", v.get('description'))
        for item in v.get('items', []):
            print(" ", item)
