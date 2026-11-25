import re

with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# Update D4
code = re.sub(r"P\['D4'\]\s*=\s*\([^)]+\)", "P['D4']  = (115.0, 87.0, 0, 'B.Cu')", code)

# Update R45, R46, JP1
code = re.sub(r"P\['JP1'\]\s*=\s*\([^)]+\)", "P['JP1'] = (75.5, 98.0, 0, 'B.Cu')", code)
code = re.sub(r"P\['R45'\]\s*=\s*\([^)]+\)", "P['R45'] = (73.5, 95.0, 0, 'B.Cu')", code)
code = re.sub(r"P\['R46'\]\s*=\s*\([^)]+\)", "P['R46'] = (77.5, 95.0, 0, 'B.Cu')", code)

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/apply_pure_circle_pcb.py'], capture_output=True, text=True)
print(res.stdout)
