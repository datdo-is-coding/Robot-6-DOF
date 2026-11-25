import re

with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    sch = f.read()

# find all (property "Reference" "J...")
for m in re.finditer(r'\(property "Reference" "([^"]+)"', sch):
    start = max(0, m.start() - 200)
    end = min(len(sch), m.end() + 300)
    print("--- MATCH ---")
    print(sch[start:end])
