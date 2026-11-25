with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# Fix F.Cu JP1, R45, D1..D3:
code = code.replace("P['JP1'] = (75.5, 97.2, 0, 'F.Cu')", "P['JP1'] = (75.5, 96.5, 0, 'F.Cu')")
code = code.replace("P['R45'] = (75.5, 99.0, 0, 'F.Cu')", "P['R45'] = (75.5, 99.2, 0, 'F.Cu')")
code = code.replace("P['D1']  = (74.5, 102.5, 0, 'F.Cu')", "P['D1']  = (74.5, 101.5, 0, 'F.Cu')")
code = code.replace("P['R33'] = (77.5, 102.5, 0, 'F.Cu')", "P['R33'] = (77.5, 101.5, 0, 'F.Cu')")
code = code.replace("P['D2']  = (74.5, 104.5, 0, 'F.Cu')", "P['D2']  = (74.5, 103.5, 0, 'F.Cu')")
code = code.replace("P['R35'] = (77.5, 104.5, 0, 'F.Cu')", "P['R35'] = (77.5, 103.5, 0, 'F.Cu')")
code = code.replace("P['D3']  = (74.5, 106.5, 0, 'F.Cu')", "P['D3']  = (74.5, 105.2, 0, 'F.Cu')")
code = code.replace("P['R36'] = (77.5, 106.5, 0, 'F.Cu')", "P['R36'] = (77.5, 105.2, 0, 'F.Cu')")

# Spread out B.Cu components:
# L1 at (115.0, 78.0), D4 at (123.0, 78.0)
code = code.replace("P['L1']  = (114.0, 96.0, 0, 'B.Cu')",  "P['L1']  = (115.0, 78.0, 0, 'B.Cu')")
code = code.replace("P['D4']  = (122.5, 86.0, 0, 'B.Cu')",  "P['D4']  = (123.0, 78.0, 0, 'B.Cu')")

code = code.replace("P['C16'] = (114.5, 91.5, 0, 'B.Cu')", "P['C16'] = (114.5, 83.5, 0, 'B.Cu')")
code = code.replace("P['C17'] = (118.5, 91.5, 0, 'B.Cu')", "P['C17'] = (118.5, 83.5, 0, 'B.Cu')")
code = code.replace("P['R53'] = (114.5, 89.0, 0, 'B.Cu')", "P['R53'] = (114.5, 86.0, 0, 'B.Cu')")
code = code.replace("P['R54'] = (118.5, 89.0, 0, 'B.Cu')", "P['R54'] = (118.5, 86.0, 0, 'B.Cu')")

code = code.replace("P['U10'] = (123.0, 88.0, 0, 'B.Cu')", "P['U10'] = (123.0, 83.5, 0, 'B.Cu')")
code = code.replace("P['C57'] = (127.0, 87.5, 0, 'B.Cu')", "P['C57'] = (127.0, 83.5, 0, 'B.Cu')")
code = code.replace("P['C58'] = (127.0, 90.0, 0, 'B.Cu')", "P['C58'] = (127.0, 86.0, 0, 'B.Cu')")

code = code.replace("P['F1']  = (122.0, 104.5, 90, 'B.Cu')", "P['F1']  = (115.0, 104.5, 90, 'B.Cu')")
code = code.replace("P['D6']  = (122.0, 86.0, 0, 'B.Cu')",  "P['D6']  = (124.0, 104.5, 0, 'B.Cu')")

code = code.replace("P['TP3'] = (110.0, 93.0, 0, 'B.Cu')", "P['TP3'] = (110.0, 85.0, 0, 'B.Cu')")
code = code.replace("P['C64'] = (112.0, 96.0, 0, 'B.Cu')", "P['C64'] = (112.0, 96.0, 0, 'B.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/apply_pure_circle_pcb.py'], capture_output=True, text=True)
print(res.stdout)
