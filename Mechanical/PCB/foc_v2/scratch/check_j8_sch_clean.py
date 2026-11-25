with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Let's see all lines with J8 and J9 instances
lines = text.splitlines()
for i, l in enumerate(lines):
    if '(property "Reference" "J8"' in l or '(property "Reference" "J9"' in l:
        print(f"Line {i+1}:")
        for j in range(max(0, i-5), min(len(lines), i+25)):
            print(f"  {lines[j]}")
