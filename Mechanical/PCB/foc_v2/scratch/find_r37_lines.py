with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '"Reference" "R37"' in l:
        print(f"R37 found at line {i}")
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f"{j}: {lines[j].strip()}")
        break
