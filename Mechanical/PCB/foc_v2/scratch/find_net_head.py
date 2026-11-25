with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = [f.readline() for _ in range(50)]

for i, l in enumerate(lines):
    if "(net " in l:
        print(l.strip())
