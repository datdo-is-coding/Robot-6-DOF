with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    for i in range(200):
        l = f.readline()
        if "(net " in l:
            print(f"Line {i+1}: {l.strip()}")
            break
