with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# Fix D1..D3 and R33..R36 to Y=102, 104, 106
code = code.replace("P['D1']  = (75.5, 104.5, 0, 'F.Cu')", "P['D1']  = (74.5, 102.0, 0, 'F.Cu')")
code = code.replace("P['R33'] = (79.0, 104.5, 0, 'F.Cu')", "P['R33'] = (77.5, 102.0, 0, 'F.Cu')")
code = code.replace("P['D2']  = (75.5, 106.8, 0, 'F.Cu')", "P['D2']  = (74.5, 104.0, 0, 'F.Cu')")
code = code.replace("P['R35'] = (79.0, 106.8, 0, 'F.Cu')", "P['R35'] = (77.5, 104.0, 0, 'F.Cu')")
code = code.replace("P['D3']  = (75.5, 109.0, 0, 'F.Cu')", "P['D3']  = (74.5, 106.0, 0, 'F.Cu')")
code = code.replace("P['R36'] = (79.0, 109.0, 0, 'F.Cu')", "P['R36'] = (77.5, 106.0, 0, 'F.Cu')")

# Fix TP3 on B.Cu away from D4:
code = code.replace("P['TP3'] = (115.0, 96.0, 0, 'B.Cu')", "P['TP3'] = (110.0, 93.0, 0, 'B.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/solve_zero_drc_exact0.py'], capture_output=True, text=True)
print(res.stdout)
