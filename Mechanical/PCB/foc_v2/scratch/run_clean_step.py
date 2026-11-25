with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# Replace C4, C5, R38, C55, R39, C56, C64 to B.Cu
code = code.replace("P['C4']  = (96.5, 92.2, 0, 'F.Cu')", "P['C4']  = (96.5, 96.0, 0, 'B.Cu')")
code = code.replace("P['C5']  = (103.5, 92.2, 0, 'F.Cu')", "P['C5']  = (103.5, 96.0, 0, 'B.Cu')")
code = code.replace("P['R37'] = (88.5, 92.2, 0, 'F.Cu')", "P['R37'] = (88.5, 96.0, 0, 'B.Cu')")
code = code.replace("P['C54'] = (91.5, 92.2, 0, 'F.Cu')", "P['C54'] = (91.5, 96.0, 0, 'B.Cu')")
code = code.replace("P['R38'] = (94.0, 92.2, 0, 'F.Cu')", "P['R38'] = (94.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C55'] = (99.0, 92.2, 0, 'F.Cu')", "P['C55'] = (99.0, 93.5, 0, 'B.Cu')")
code = code.replace("P['R39'] = (101.0, 92.2, 0, 'F.Cu')", "P['R39'] = (101.0, 93.5, 0, 'B.Cu')")
code = code.replace("P['C56'] = (106.0, 92.2, 0, 'F.Cu')", "P['C56'] = (106.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C64'] = (107.5, 94.8, 0, 'F.Cu')", "P['C64'] = (108.5, 96.0, 0, 'B.Cu')")

# Fix J1 and J3 to avoid OOB:
# Radius of board is 35.0. Center (100, 100).
# Outer ring of J1/J3 pad has radius 1.35.
# At X = 87.0, Y = 71.5: dx = -13.0, dy = -28.5 -> dist = sqrt(169 + 812.25) = 31.32 mm.
# Pad outer ring: 31.32 + 1.35 = 32.67 mm < 34.95 mm!
code = code.replace("P['J1'] = (87.0, 68.0, 0, 'F.Cu')", "P['J1'] = (87.0, 71.5, 0, 'F.Cu')")
code = code.replace("P['J3'] = (113.0, 68.0, 0, 'F.Cu')", "P['J3'] = (113.0, 71.5, 0, 'F.Cu')")

# Fix C_BULK1 and U9:
# U9 moved to Y = 95.0, C60 to Y = 95.0
code = code.replace("P['U9']  = (75.5, 93.0, 0, 'F.Cu')", "P['U9']  = (75.5, 95.0, 0, 'F.Cu')")
code = code.replace("P['C60'] = (71.5, 93.0, 90, 'F.Cu')", "P['C60'] = (71.5, 95.0, 90, 'F.Cu')")
code = code.replace("P['JP1'] = (75.5, 96.0, 0, 'F.Cu')", "P['JP1'] = (75.5, 97.5, 0, 'F.Cu')")
code = code.replace("P['C61'] = (71.5, 96.0, 90, 'F.Cu')", "P['C61'] = (71.5, 97.5, 90, 'F.Cu')")

# Fix L1 and U10 on B.Cu:
# L1 at (124.0, 97.0), U10 at (123.0, 89.0)
code = code.replace("P['L1']  = (124.0, 95.0, 0, 'B.Cu')", "P['L1']  = (124.0, 98.0, 0, 'B.Cu')")
code = code.replace("P['U10'] = (123.0, 90.5, 0, 'B.Cu')", "P['U10'] = (123.0, 88.0, 0, 'B.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/solve_zero_drc_exact0.py'], capture_output=True, text=True)
print(res.stdout)
