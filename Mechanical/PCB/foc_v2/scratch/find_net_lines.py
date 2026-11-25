with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines[:1000]):
    if "(net " in l:
        print(f"Line {i+1}: {l.strip()}")
        if i > 200:
            break
