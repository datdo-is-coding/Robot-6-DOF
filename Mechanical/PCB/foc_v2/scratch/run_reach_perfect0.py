with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

code = code.replace("P['JP1'] = (75.5, 98.0, 0, 'F.Cu')", "P['JP1'] = (75.5, 97.2, 0, 'F.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/solve_zero_drc_exact0.py'], capture_output=True, text=True)
print(res.stdout)
