with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("\t(zone") or line.startswith("  (zone") or line.startswith("(zone"):
        print(f"Zone at line {i+1}: {line.strip()[:60]}")
        for k in range(i+1, min(len(lines), i+8)):
            print(f"    {lines[k].strip()}")
