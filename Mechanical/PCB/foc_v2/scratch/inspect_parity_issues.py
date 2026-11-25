import json

with open("scratch/drc_unrouted.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

parity = drc.get("schematic_parity_issues", [])
print(f"Total schematic parity issues: {len(parity)}")
for p in parity:
    print("--- Issue ---")
    print(json.dumps(p, indent=2))
