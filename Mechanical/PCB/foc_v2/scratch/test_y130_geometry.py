import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

# South flat cut at y = 130.0 mm
y_south = 130.0
dy = y_south - CY # 30.0 mm
dx = math.sqrt(R_BOARD**2 - dy**2) # sqrt(1225 - 900) = sqrt(325) = 18.0277 mm
print(f"South flat cut at y={y_south}: from x = {CX - dx:.2f} to {CX + dx:.2f} (width = {2*dx:.2f} mm)")

# East flat cut at x = 132.0 mm
x_east = 132.0
dx_e = x_east - CX # 32.0 mm
dy_e = math.sqrt(R_BOARD**2 - dx_e**2) # sqrt(1225 - 1024) = sqrt(201) = 14.1774 mm
print(f"East flat cut at x={x_east}: from y = {CY - dy_e:.2f} to {CY + dy_e:.2f} (height = {2*dy_e:.2f} mm)")

# SE corner arc:
# Connects South flat cut at (100 + dx, y_south) = (118.03, 130.0)
# to East flat cut at (x_east, 100 + dy_e) = (132.0, 114.18)
# Both endpoints are at radius exactly R = 35.0 mm!
print(f"Radius of South cut endpoint (118.03, 130.0): {math.hypot(dx, dy):.4f}")
print(f"Radius of East cut endpoint (132.0, 114.18): {math.hypot(dx_e, dy_e):.4f}")

# Connectors at South bank (y_pin = 120.0 mm):
# Front of XH shroud: y = 120.0 + 9.2 = 129.2 mm < 130.0 mm!
# Clearance from shroud front to board edge: 130.0 - 129.2 = 0.8 mm inside the board!
# Back of XH shroud: y = 120.0 - 2.45 = 117.55 mm
# Top of H1/H2 keepout: y = 115.556 + 3.0 = 118.556 mm
print(f"XH shroud front y = {120.0 + 9.2:.2f} mm (inside board by {130.0 - (120.0 + 9.2):.2f} mm)")
