with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

code = code.replace("P['R45'] = (75.5, 100.5, 0, 'F.Cu')", "P['R45'] = (75.5, 99.5, 0, 'F.Cu')")
code = code.replace("P['R46'] = (75.5, 102.5, 0, 'F.Cu')", "P['R46'] = (75.5, 101.0, 0, 'F.Cu')")
code = code.replace("P['D1']  = (74.5, 102.0, 0, 'F.Cu')", "P['D1']  = (74.5, 102.8, 0, 'F.Cu')")
code = code.replace("P['R33'] = (77.5, 102.0, 0, 'F.Cu')", "P['R33'] = (77.5, 102.8, 0, 'F.Cu')")
code = code.replace("P['D2']  = (74.5, 104.0, 0, 'F.Cu')", "P['D2']  = (74.5, 104.8, 0, 'F.Cu')")
code = code.replace("P['R35'] = (77.5, 104.0, 0, 'F.Cu')", "P['R35'] = (77.5, 104.8, 0, 'F.Cu')")
code = code.replace("P['D3']  = (74.5, 106.0, 0, 'F.Cu')", "P['D3']  = (74.5, 106.8, 0, 'F.Cu')")
code = code.replace("P['R36'] = (77.5, 106.0, 0, 'F.Cu')", "P['R36'] = (77.5, 106.8, 0, 'F.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/solve_zero_drc_exact0.py'], capture_output=True, text=True)
print(res.stdout)
