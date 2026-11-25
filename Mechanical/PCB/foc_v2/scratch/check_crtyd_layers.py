import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

refs = ['U1', 'C10', 'C11', 'Q7', 'U8', 'C59', 'R40', 'R41', 'R42', 'R43', 'J9']
for ref in refs:
    lines = s.fps[ref]
    crtyd_layers = set()
    for l in lines:
        if 'CrtYd' in l:
            crtyd_layers.add(l.strip())
    print(f"{ref:6s}: {crtyd_layers}")
