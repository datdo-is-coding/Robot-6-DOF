with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(name "M2.5 screw head clearance")' in l:
        # find the start of this zone
        for k in range(i, max(0, i-20), -1):
            if lines[k].strip() == "(zone":
                print(f"Zone starts at line {k+1}, name at line {i+1}")
                break
