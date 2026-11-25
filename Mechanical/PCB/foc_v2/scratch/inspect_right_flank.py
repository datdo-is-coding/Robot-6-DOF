import re

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for r in ['C15', 'C18', 'C19', 'C20', 'C21', 'R55', 'R56', 'R57', 'R58', 'R59', 'R60', 'TP3']:
    m = re.search(r'\(footprint "([^"]+)"[\s\S]*?\(property "Reference" "' + r + r'"[\s\S]*?\(property "Value" "([^"]+)"', text)
    if m:
        print(f"{r:6s}: {m.group(2):20s} ({m.group(1)})")
