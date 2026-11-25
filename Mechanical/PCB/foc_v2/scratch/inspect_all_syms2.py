with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines[300:1000]):
    if "(symbol " in l and not l.strip().endswith("_0_0") and not l.strip().endswith("_0_1"):
        print(f"Line {i+301}: {l.strip()[:60]}")
