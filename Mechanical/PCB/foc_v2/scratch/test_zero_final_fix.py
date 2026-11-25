with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# Fix U9, JP1, R45, R46:
code = code.replace("P['U9']  = (75.5, 94.0, 0, 'F.Cu')", "P['U9']  = (75.5, 93.0, 0, 'F.Cu')")
code = code.replace("P['JP1'] = (75.5, 96.5, 0, 'F.Cu')", "P['JP1'] = (75.5, 96.5, 0, 'F.Cu')")
code = code.replace("P['R45'] = (75.5, 99.0, 0, 'F.Cu')", "P['R45'] = (74.0, 99.0, 0, 'F.Cu')")
code = code.replace("P['R46'] = (75.5, 100.5, 0, 'F.Cu')", "P['R46'] = (77.0, 99.0, 0, 'F.Cu')")

code = code.replace("P['D1']  = (74.5, 101.5, 0, 'F.Cu')", "P['D1']  = (74.5, 101.5, 0, 'F.Cu')")
code = code.replace("P['R33'] = (77.5, 101.5, 0, 'F.Cu')", "P['R33'] = (77.5, 101.5, 0, 'F.Cu')")

# Fix F1 and D6 on B.Cu:
code = code.replace("P['F1']  = (115.0, 104.5, 90, 'B.Cu')", "P['F1']  = (124.0, 106.0, 90, 'B.Cu')")
code = code.replace("P['D6']  = (124.0, 104.5, 0, 'B.Cu')",  "P['D6']  = (116.0, 106.0, 0, 'B.Cu')")

# Fix C64 on B.Cu:
code = code.replace("P['C64'] = (112.0, 96.0, 0, 'B.Cu')", "P['C64'] = (108.0, 96.0, 0, 'B.Cu')")

# Fix C16, C17, R53, R54 to avoid H4:
# H4 is at (115.556, 84.444).
# Move them to Y = 80.0..83.0 at X = 110.0 and X = 113.0 or South:
code = code.replace("P['C16'] = (114.5, 83.5, 0, 'B.Cu')", "P['C16'] = (111.0, 78.0, 0, 'B.Cu')")
code = code.replace("P['C17'] = (118.5, 83.5, 0, 'B.Cu')", "P['C17'] = (111.0, 81.0, 0, 'B.Cu')")
code = code.replace("P['R53'] = (114.5, 86.0, 0, 'B.Cu')", "P['R53'] = (111.0, 84.0, 0, 'B.Cu')")
code = code.replace("P['R54'] = (118.5, 86.0, 0, 'B.Cu')", "P['R54'] = (111.0, 87.0, 0, 'B.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/apply_pure_circle_pcb.py'], capture_output=True, text=True)
print(res.stdout)
