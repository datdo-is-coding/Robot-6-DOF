with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "C_BULK1"' in l:
        start = i - 5
        for k in range(start, start + 400):
            if lines[k].startswith('\t)'):
                print(f"End of C_BULK1 at {k}")
                break
            if 'CrtYd' in lines[k]:
                print(f"Line {k}: {lines[k].strip()}")
                for m in range(max(start, k-4), min(start+400, k+5)):
                    print("  ", lines[m].rstrip())
        break
