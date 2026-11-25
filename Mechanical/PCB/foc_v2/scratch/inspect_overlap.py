with open('scratch/solve_zero_drc_exact0.py') as f:
    lines = f.readlines()

for line in lines:
    for k in ['D4', 'F1', 'JP1', 'U9', 'R45', 'R46', 'C_BULK1', 'J8']:
        if f"'{k}'" in line and '=' in line:
            print(line.strip())
