with open('scratch/solve_final_zero_conflicts.py', 'r') as f:
    text = f.read()

import re
for ref in ['U9', 'C60', 'C61', 'C62', 'R45', 'R46', 'JP1']:
    m = re.search(r"'" + ref + r"':\s*\(([^)]+)\)", text)
    if m:
        print(f"{ref:4s}: ({m.group(1)})")
