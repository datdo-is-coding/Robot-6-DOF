with open('scratch/solve_zero_drc_exact0.py', 'r') as f:
    code = f.read()

# 1. J1 and J3
code = code.replace("P['J1'] = (87.0, 71.5, 0, 'F.Cu')", "P['J1'] = (86.5, 71.5, 0, 'F.Cu')")
code = code.replace("P['J3'] = (113.0, 71.5, 0, 'F.Cu')", "P['J3'] = (113.5, 71.5, 0, 'F.Cu')")

# 2. West Wing F.Cu passives:
code = code.replace("P['U9']  = (75.5, 95.0, 0, 'F.Cu')", "P['U9']  = (75.5, 94.0, 0, 'F.Cu')")
code = code.replace("P['JP1'] = (75.5, 97.5, 0, 'F.Cu')", "P['JP1'] = (75.5, 98.0, 0, 'F.Cu')")
code = code.replace("P['R45'] = (75.5, 98.0, 0, 'F.Cu')", "P['R45'] = (75.5, 100.5, 0, 'F.Cu')")
code = code.replace("P['R46'] = (75.5, 100.0, 0, 'F.Cu')", "P['R46'] = (75.5, 102.5, 0, 'F.Cu')")

code = code.replace("P['D1']  = (75.5, 102.0, 0, 'F.Cu')", "P['D1']  = (75.5, 104.5, 0, 'F.Cu')")
code = code.replace("P['R33'] = (79.0, 102.0, 0, 'F.Cu')", "P['R33'] = (79.0, 104.5, 0, 'F.Cu')")
code = code.replace("P['D2']  = (75.5, 104.2, 0, 'F.Cu')", "P['D2']  = (75.5, 106.8, 0, 'F.Cu')")
code = code.replace("P['R35'] = (79.0, 104.2, 0, 'F.Cu')", "P['R35'] = (79.0, 106.8, 0, 'F.Cu')")
code = code.replace("P['D3']  = (75.5, 106.4, 0, 'F.Cu')", "P['D3']  = (75.5, 109.0, 0, 'F.Cu')")
code = code.replace("P['R36'] = (79.0, 106.4, 0, 'F.Cu')", "P['R36'] = (79.0, 109.0, 0, 'F.Cu')")

code = code.replace("P['C60'] = (71.5, 95.0, 90, 'F.Cu')", "P['C60'] = (71.5, 94.0, 90, 'F.Cu')")
code = code.replace("P['C61'] = (71.5, 97.5, 90, 'F.Cu')", "P['C61'] = (71.5, 97.5, 90, 'F.Cu')")
code = code.replace("P['C62'] = (71.5, 99.0, 90, 'F.Cu')", "P['C62'] = (71.5, 101.0, 90, 'F.Cu')")

# 3. B.Cu filter caps under U1:
code = code.replace("P['R37'] = (88.5, 96.0, 0, 'B.Cu')", "P['R37'] = (85.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C54'] = (91.5, 96.0, 0, 'B.Cu')", "P['C54'] = (88.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['R38'] = (94.0, 96.0, 0, 'B.Cu')", "P['R38'] = (91.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C4']  = (96.5, 96.0, 0, 'B.Cu')", "P['C4']  = (94.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C55'] = (99.0, 93.5, 0, 'B.Cu')", "P['C55'] = (97.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['R39'] = (101.0, 93.5, 0, 'B.Cu')", "P['R39'] = (103.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C5']  = (103.5, 96.0, 0, 'B.Cu')", "P['C5']  = (106.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C56'] = (106.0, 96.0, 0, 'B.Cu')", "P['C56'] = (109.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['C64'] = (108.5, 96.0, 0, 'B.Cu')", "P['C64'] = (112.0, 96.0, 0, 'B.Cu')")
code = code.replace("P['TP3'] = (110.0, 95.5, 0, 'B.Cu')", "P['TP3'] = (115.0, 96.0, 0, 'B.Cu')")

# 4. U10, C57, C58 on B.Cu:
code = code.replace("P['U10'] = (123.0, 88.0, 0, 'B.Cu')", "P['U10'] = (123.0, 88.0, 0, 'B.Cu')")
code = code.replace("P['C57'] = (123.0, 87.5, 0, 'B.Cu')", "P['C57'] = (127.0, 87.5, 0, 'B.Cu')")
code = code.replace("P['C58'] = (127.0, 90.5, 0, 'B.Cu')", "P['C58'] = (127.0, 90.0, 0, 'B.Cu')")

with open('scratch/solve_zero_drc_exact0.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/solve_zero_drc_exact0.py'], capture_output=True, text=True)
print(res.stdout)
