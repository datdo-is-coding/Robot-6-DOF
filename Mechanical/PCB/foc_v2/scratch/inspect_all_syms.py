with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines[:300]):
    if "(symbol " in l:
        print(f"Line {i+1}: {l.strip()[:60]}")
