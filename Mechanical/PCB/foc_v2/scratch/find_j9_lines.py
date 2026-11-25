with open("scratch/pcb_step2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "J9"' in l:
        print(f"J9 at line {i+1}")
        for j in range(max(0, i-10), min(len(lines), i+10)):
            print(f"  {lines[j].rstrip()}")
        break
