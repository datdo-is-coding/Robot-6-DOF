with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# 1. U9 to Y=94.0 (clear of C_BULK1)
code = code.replace("P['U9']  = (75.5, 93.0, 0, 'F.Cu')", "P['U9']  = (75.5, 94.0, 0, 'F.Cu')")

# 2. R45 and R46 horizontally separated
code = code.replace("P['R45'] = (74.0, 99.0, 0, 'F.Cu')", "P['R45'] = (73.0, 99.0, 0, 'F.Cu')")
code = code.replace("P['R46'] = (77.0, 99.0, 0, 'F.Cu')", "P['R46'] = (77.5, 99.0, 0, 'F.Cu')")

# 3. C64 on B.Cu at (108.0, 99.0)
code = code.replace("P['C64'] = (108.0, 96.0, 0, 'B.Cu')", "P['C64'] = (108.0, 99.0, 0, 'B.Cu')")

# 4. TP3 on B.Cu at (105.0, 85.0)
code = code.replace("P['TP3'] = (110.0, 85.0, 0, 'B.Cu')", "P['TP3'] = (105.0, 85.0, 0, 'B.Cu')")

# 5. L1 and C16, C17 on B.Cu
code = code.replace("P['L1']  = (115.0, 78.0, 0, 'B.Cu')",  "P['L1']  = (118.0, 78.0, 0, 'B.Cu')")
code = code.replace("P['C16'] = (111.0, 78.0, 0, 'B.Cu')", "P['C16'] = (108.0, 78.0, 0, 'B.Cu')")
code = code.replace("P['C17'] = (111.0, 81.0, 0, 'B.Cu')", "P['C17'] = (108.0, 81.0, 0, 'B.Cu')")
code = code.replace("P['R53'] = (111.0, 84.0, 0, 'B.Cu')", "P['R53'] = (108.0, 84.0, 0, 'B.Cu')")
code = code.replace("P['R54'] = (111.0, 87.0, 0, 'B.Cu')", "P['R54'] = (108.0, 87.0, 0, 'B.Cu')")

# 6. F1 at (122.0, 105.0, 90) on B.Cu
code = code.replace("P['F1']  = (124.0, 106.0, 90, 'B.Cu')", "P['F1']  = (122.0, 105.0, 90, 'B.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/apply_pure_circle_pcb.py'], capture_output=True, text=True)
print(res.stdout)
