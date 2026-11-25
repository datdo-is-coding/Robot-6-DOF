import json

with open("scratch/drc_verified_parity.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

parity = drc.get("schematic_parity_issues", [])
print(f"Total parity issues: {len(parity)}")
for p in parity:
    print(p.get("type"), "-", p.get("description"))
    for it in p.get("items", []):
        print("  ", it.get("description"))
