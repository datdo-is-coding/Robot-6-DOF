with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_j7 = False
for l in lines:
    if '(property "Reference" "J7"' in l:
        in_j7 = True
    if in_j7:
        if "fp_line" in l or "fp_rect" in l or "pad " in l or "(at " in l:
            print(l.strip())
        if l.strip() == ")":
            break
