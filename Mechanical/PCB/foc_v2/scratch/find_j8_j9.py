import re

with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    sch = f.read()

for m in re.finditer(r'\(property "Reference" "(J[89])"', sch):
    ref = m.group(1)
    start = max(0, m.start() - 50)
    end = min(len(sch), m.end() + 200)
    print(f"=== {ref} ===")
    print(sch[start:end])
