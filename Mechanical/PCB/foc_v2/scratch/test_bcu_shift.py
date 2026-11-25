# Test moving USB circuit to B.Cu
with open('scratch/find_perfect_coords.py', 'r') as f:
    code = f.read()

# Replace USB circuit layer from F.Cu to B.Cu
code = code.replace("P['U8']  = (86.0, 109.0, 0, 'F.Cu')", "P['U8']  = (92.25, 110.0, 0, 'B.Cu')")
code = code.replace("P['C59'] = (86.0, 106.5, 0, 'F.Cu')", "P['C59'] = (92.25, 112.5, 0, 'B.Cu')")
code = code.replace("P['Q7']  = (92.25, 109.5, 0, 'F.Cu')", "P['Q7']  = (92.25, 115.0, 0, 'B.Cu')")
code = code.replace("P['R40'] = (88.5, 111.5, 0, 'F.Cu')", "P['R40'] = (88.5,  118.0, 0, 'B.Cu')")
code = code.replace("P['R41'] = (96.0, 111.5, 0, 'F.Cu')", "P['R41'] = (96.0,  118.0, 0, 'B.Cu')")
code = code.replace("P['R42'] = (88.5, 107.5, 0, 'F.Cu')", "P['R42'] = (88.5,  115.5, 0, 'B.Cu')")
code = code.replace("P['R43'] = (96.0, 107.5, 0, 'F.Cu')", "P['R43'] = (96.0,  115.5, 0, 'B.Cu')")

with open('scratch/find_perfect_coords.py', 'w') as f:
    f.write(code)

import subprocess
res = subprocess.run(['python', 'scratch/find_perfect_coords.py'], capture_output=True, text=True)
print(res.stdout)
