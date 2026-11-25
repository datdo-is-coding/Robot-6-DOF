import math

# Center (100, 100), R = 35.0 mm
# Let's test South flat cut at y = 128.0 mm
cy_cut = 128.0
dy = cy_cut - 100.0 # 28.0 mm
dx = math.sqrt(35.0**2 - dy**2) # sqrt(1225 - 784) = sqrt(441) = 21.0 mm!
print(f"At y = {cy_cut}: South flat cut from x = {100.0 - dx:.1f} to {100.0 + dx:.1f} (width = {2*dx:.1f} mm)")

# East flat cut at x = 132.0 mm
cx_cut = 132.0
dx_east = cx_cut - 100.0 # 32.0 mm
dy_east = math.sqrt(35.0**2 - dx_east**2) # sqrt(1225 - 1024) = sqrt(201) = 14.1774 mm
print(f"At x = {cx_cut}: East flat cut from y = {100.0 - dy_east:.2f} to {100.0 + dy_east:.2f} (height = {2*dy_east:.2f} mm)")

# Holes:
H_SW = (84.444, 115.556)
H_SE = (115.556, 115.556)
print(f"H_SW = {H_SW}, H_SE = {H_SE}")
print(f"Distance between H_SW and H_SE: {H_SE[0] - H_SW[0]:.2f} mm")
print(f"Y gap from holes (y=115.56) to board edge (y={cy_cut}): {cy_cut - H_SW[1]:.2f} mm")
