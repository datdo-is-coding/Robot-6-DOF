import json

with open('scratch/drc_final.json') as f:
    drc = json.load(f)

for v in drc.get('violations', []):
    for it in v.get('items', []):
        d = it.get('description', '')
        if 'Pad' in d and ('J11' in d or 'J10' in d or 'Q1' in d):
            print(d, it.get('pos'))
