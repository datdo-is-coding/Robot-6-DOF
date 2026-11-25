# Check a pad with known offset under rotation from KiCad DRC!
import json

with open('scratch/drc_final.json') as f:
    drc = json.load(f)

# Find any pad violation that shows pad position
for v in drc.get('violations', []):
    for it in v.get('items', []):
        if 'Pad' in it.get('description', ''):
            print(it.get('description'), it.get('pos'))
            break
    if 'Pad' in str(v): break
