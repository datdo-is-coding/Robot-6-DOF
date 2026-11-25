with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# 1. J11 at Y = 101.50
code = code.replace("P['J11'] = (115.5, 99.5, 270, 'F.Cu')", "P['J11'] = (115.5, 101.50, 270, 'F.Cu')")

# 2. F1 and D6 and L1 on B.Cu
code = code.replace("P['F1']  = (116.5, 104.5, 90, 'B.Cu')", "P['F1']  = (122.0, 104.5, 90, 'B.Cu')")
code = code.replace("P['D6']  = (125.0, 104.5, 0, 'B.Cu')", "P['D6']  = (122.0, 86.0, 0, 'B.Cu')")
code = code.replace("P['L1']  = (124.0, 98.0, 0, 'B.Cu')",  "P['L1']  = (114.0, 96.0, 0, 'B.Cu')")

# 3. D1..D3 and R33..R36
code = code.replace("P['R45'] = (75.5, 99.5, 0, 'F.Cu')", "P['R45'] = (75.5, 99.0, 0, 'F.Cu')")
code = code.replace("P['R46'] = (75.5, 101.0, 0, 'F.Cu')", "P['R46'] = (75.5, 100.5, 0, 'F.Cu')")
code = code.replace("P['D1']  = (74.5, 101.5, 0, 'F.Cu')", "P['D1']  = (74.5, 102.5, 0, 'F.Cu')")
code = code.replace("P['R33'] = (77.5, 101.5, 0, 'F.Cu')", "P['R33'] = (77.5, 102.5, 0, 'F.Cu')")
code = code.replace("P['D2']  = (74.5, 103.5, 0, 'F.Cu')", "P['D2']  = (74.5, 104.5, 0, 'F.Cu')")
code = code.replace("P['R35'] = (77.5, 103.5, 0, 'F.Cu')", "P['R35'] = (77.5, 104.5, 0, 'F.Cu')")
code = code.replace("P['D3']  = (74.5, 105.5, 0, 'F.Cu')", "P['D3']  = (74.5, 106.5, 0, 'F.Cu')")
code = code.replace("P['R36'] = (77.5, 105.5, 0, 'F.Cu')", "P['R36'] = (77.5, 106.5, 0, 'F.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/apply_pure_circle_pcb.py'], capture_output=True, text=True)
print(res.stdout)
