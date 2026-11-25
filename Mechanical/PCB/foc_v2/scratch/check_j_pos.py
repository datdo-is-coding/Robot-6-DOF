with open('scratch/solve_zero_drc_exact0.py') as f:
    for line in f:
        for k in ['J7', 'J8', 'J9', 'J10', 'J11']:
            if f"P['{k}']" in line:
                print(line.strip())
