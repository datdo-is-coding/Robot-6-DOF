import re

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

refs = ['U8', 'C59', 'Q7', 'R40', 'R41', 'R42', 'R43', 'U9', 'U10', 'D6', 'F1', 'J11', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'C57', 'C58']
for r in refs:
    m = re.search(r'\(footprint "([^"]+)"[\s\S]*?\(property "Reference" "' + r + r'"[\s\S]*?\(property "Value" "([^"]+)"', text)
    if m:
        fp_name, val = m.group(1), m.group(2)
        print(f"{r:6s}: {val:20s} ({fp_name})")
