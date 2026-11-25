with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(845, 875):
    print(f"Line {j+1}: {repr(lines[j])}")
