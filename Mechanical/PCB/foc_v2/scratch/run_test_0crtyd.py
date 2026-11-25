with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# 1. J11 up to Y = 99.5
code = code.replace("P['J11'] = (115.5, 102.5, 270, 'F.Cu')", "P['J11'] = (115.5, 99.5, 270, 'F.Cu')")

# 2. C1..C13 to X = 93.0, R6..R50 to X = 89.5
code = code.replace("P['C1']  = (94.0, 84.5, 0, 'F.Cu')", "P['C1']  = (93.0, 84.5, 0, 'F.Cu')")
code = code.replace("P['C2']  = (94.0, 86.5, 0, 'F.Cu')", "P['C2']  = (93.0, 86.5, 0, 'F.Cu')")
code = code.replace("P['C3']  = (94.0, 88.5, 0, 'F.Cu')", "P['C3']  = (93.0, 88.5, 0, 'F.Cu')")
code = code.replace("P['C12'] = (94.0, 90.5, 0, 'F.Cu')", "P['C12'] = (93.0, 90.5, 0, 'F.Cu')")
code = code.replace("P['C13'] = (94.0, 92.5, 0, 'F.Cu')", "P['C13'] = (93.0, 92.5, 0, 'F.Cu')")

code = code.replace("P['R6']  = (90.0, 84.5, 0, 'F.Cu')", "P['R6']  = (89.5, 84.5, 0, 'F.Cu')")
code = code.replace("P['R8']  = (90.0, 86.5, 0, 'F.Cu')", "P['R8']  = (89.5, 86.5, 0, 'F.Cu')")
code = code.replace("P['R9']  = (90.0, 88.5, 0, 'F.Cu')", "P['R9']  = (89.5, 88.5, 0, 'F.Cu')")
code = code.replace("P['R10'] = (90.0, 90.5, 0, 'F.Cu')", "P['R10'] = (89.5, 90.5, 0, 'F.Cu')")
code = code.replace("P['R50'] = (90.0, 92.5, 0, 'F.Cu')", "P['R50'] = (89.5, 92.5, 0, 'F.Cu')")

# 3. F1 and D6 on B.Cu
code = code.replace("P['F1']  = (118.0, 104.5, 0, 'B.Cu')", "P['F1']  = (116.5, 104.5, 90, 'B.Cu')")
code = code.replace("P['D6']  = (126.0, 104.5, 0, 'B.Cu')", "P['D6']  = (125.0, 104.5, 0, 'B.Cu')")

# 4. D1..D3 and R33..R36 to Y=101, 103, 105
code = code.replace("P['D1']  = (74.5, 102.8, 0, 'F.Cu')", "P['D1']  = (74.5, 101.5, 0, 'F.Cu')")
code = code.replace("P['R33'] = (77.5, 102.8, 0, 'F.Cu')", "P['R33'] = (77.5, 101.5, 0, 'F.Cu')")
code = code.replace("P['D2']  = (74.5, 104.8, 0, 'F.Cu')", "P['D2']  = (74.5, 103.5, 0, 'F.Cu')")
code = code.replace("P['R35'] = (77.5, 104.8, 0, 'F.Cu')", "P['R35'] = (77.5, 103.5, 0, 'F.Cu')")
code = code.replace("P['D3']  = (74.5, 106.8, 0, 'F.Cu')", "P['D3']  = (74.5, 105.5, 0, 'F.Cu')")
code = code.replace("P['R36'] = (77.5, 106.8, 0, 'F.Cu')", "P['R36'] = (77.5, 105.5, 0, 'F.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/apply_pure_circle_pcb.py'], capture_output=True, text=True)
print(res.stdout)
