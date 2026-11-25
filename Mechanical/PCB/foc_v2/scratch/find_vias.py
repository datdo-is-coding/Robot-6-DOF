import json

with open('scratch/drc_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

unconnected = d.get('unconnected_items', [])

print(f"Total unconnected items: {len(unconnected)}")
for i, u in enumerate(unconnected[:30]):
    items = u.get('items', [])
    desc = u.get('description', '')
    p1 = items[0].get('pos', {}) if len(items) > 0 else {}
    p2 = items[1].get('pos', {}) if len(items) > 1 else {}
    d1 = items[0].get('description', '') if len(items) > 0 else ''
    d2 = items[1].get('description', '') if len(items) > 1 else ''
    dx = p1.get('x', 0) - p2.get('x', 0)
    dy = p1.get('y', 0) - p2.get('y', 0)
    dist = (dx**2 + dy**2)**0.5
    print(f"#{i+1} [dist={dist:.2f}mm]:\n   1: {d1} at ({p1.get('x')}, {p1.get('y')})\n   2: {d2} at ({p2.get('x')}, {p2.get('y')})")
