import json

with open("scratch/drc_refill.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

violations = drc.get("violations", [])
shorts = [v for v in violations if v.get("type") == "shorting_items"]
print(f"Total shorts: {len(shorts)}")
for s in shorts[:20]:
    items = s.get("items", [])
    desc = s.get("description")
    pos = s.get("pos", {})
    item_strs = [it.get("description", "") for it in items]
    print(f"Short: {desc} at ({pos.get('x',0)}, {pos.get('y',0)})")
    for it in item_strs:
        print(f"   {it}")
