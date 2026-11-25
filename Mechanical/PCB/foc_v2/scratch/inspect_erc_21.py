import json

with open("scratch/erc_clean2.json", "r", encoding="utf-8") as f:
    erc = json.load(f)

for sheet in erc.get("sheets", []):
    v = sheet.get("violations", [])
    if v:
        print(f"Sheet {sheet.get('path')}: {len(v)} violations")
        for item in v[:5]:
            print(f"  {item.get('type')}: {item.get('description')}")
