with open('scratch/apply_p_final.py', 'r') as f:
    text = f.read()

import re
for ref in ['J7', 'J8', 'J9', 'J10', 'J11', 'H1', 'H2', 'H3', 'H4', 'J1', 'J2', 'J3']:
    m = re.search(r"'" + ref + r"':\s*\(([^)]+)\)", text)
    if m:
        print(f"{ref:4s}: ({m.group(1)})")
