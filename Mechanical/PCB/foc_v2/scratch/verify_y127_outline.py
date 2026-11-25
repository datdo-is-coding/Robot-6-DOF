import math

CX, CY = 100.0, 100.0
R = 35.0

# If South flat cut is at y = 127.0 mm:
y_south = 127.0
dy = y_south - CY # 27.0 mm
dx = math.sqrt(R**2 - dy**2) # sqrt(1225 - 729) = sqrt(496) = 22.271 mm
x1 = CX - dx # 77.73 mm
x2 = CX + dx # 122.27 mm
print(f"South flat cut at y={y_south:.1f} mm:")
print(f"  Start: ({x1:.3f}, {y_south:.3f})")
print(f"  End:   ({x2:.3f}, {y_south:.3f})")
print(f"  Width: {2*dx:.2f} mm")

# If connectors are:
# J8 (XH 3p, width 9.9 mm): center at x = 81.0, y_pin = 117.5
# Front of shroud: y = 117.5 + 9.2 = 126.7 mm < 127.0 mm! (inside board by 0.3 mm!)
# Back of shroud: y = 117.5 - 2.45 = 115.05 mm
# J9 (XH 3p, width 9.9 mm): center at x = 91.5, y_pin = 117.5
# Front of shroud: y = 126.7 mm < 127.0 mm!
# J7 (Type-C, width 9.0 mm): center at x = 101.5, front mouth at y = 127.0 mm (flush!)
# J10 (XH 5p, width 14.9 mm): center at x = 113.5, y_pin = 117.5
# Front of shroud: y = 126.7 mm < 127.0 mm!
print("\nConnector positions with y_pin = 117.5 mm:")
for name, cx in [("J8", 81.0), ("J9", 91.5), ("J7", 101.5), ("J10", 113.5)]:
    print(f"  {name:5s} at x={cx:.1f}")

# Check clearances of H1 and H2:
H_SW = (84.444, 115.556)
H_SE = (115.556, 115.556)
R_ko = 3.0

print("\nClearance to H_SW (84.44, 115.56):")
# J8 right edge is at 81.0 + 4.95 = 85.95
# J9 left edge is at 91.5 - 4.95 = 86.55
# Wait, H_SW is at x=84.444!
# If J8 is at x=78.0, J8 right edge is at 78.0 + 4.95 = 82.95 mm.
# Distance to H_SW keepout (84.444 - 3.0 = 81.444 mm) is 82.95 - 81.444 = 1.5 mm overlap if y overlaps!
