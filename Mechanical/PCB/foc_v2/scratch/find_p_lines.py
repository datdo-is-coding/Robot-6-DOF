with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    for k in ['D4', 'JP1', 'U9', 'R45', 'R46', 'F1', 'C16', 'C17', 'L1', 'U10', 'D6']:
        if f"P['{k}']" in l:
            print(f"{i+1:3d}: {l.strip()}")
