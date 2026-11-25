import re, subprocess

with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# Update D4 to (113.0, 96.0, 90, 'B.Cu')
code = re.sub(r"P\['D4'\]\s*=\s*\([^)]+\)", "P['D4']  = (113.0, 96.0, 90, 'B.Cu')", code)

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

res = subprocess.run(['python', 'scratch/apply_pure_circle_pcb.py'], capture_output=True, text=True)
print(res.stdout)
