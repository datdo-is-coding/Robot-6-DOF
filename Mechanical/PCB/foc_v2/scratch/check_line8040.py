with open("scratch/clean_step3.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(8030, 8055):
    print(f"Line {j+1}: {repr(lines[j])}")
