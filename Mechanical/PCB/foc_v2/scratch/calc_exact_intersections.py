import math

# Closed loop for Edge.Cuts:
# 1. West flat line: (66.5, 108.5) -> (66.5, 91.5)
# 2. NW arc: from (66.5, 91.5) to (100.0, 65.0) [center (100, 100)]
# 3. NE arc: from (100.0, 65.0) to (134.5, 88.5) [center (100, 100)]
#    Wait: radius to (66.5, 91.5): hypot(-33.5, -8.5) = 34.56 mm.
#    Radius to (134.5, 88.5): hypot(34.5, -11.5) = 36.36 mm.
#    Wait! If it's a circle of radius 35.0 mm:
#    Intersection of x = 66.5 with circle R=35.0:
#    y = 100 - sqrt(35^2 - 33.5^2) = 100 - 10.1366 = 89.8634 mm.
#    Intersection of x = 134.5 with circle R=35.0:
#    Wait! 134.5 - 100 = 34.5.
#    y = 100 - sqrt(35^2 - 34.5^2) = 100 - sqrt(1225 - 1190.25) = 100 - 5.895 = 94.105 mm.

print("Intersection of x=66.5 with circle R=35.0:")
y1 = 100 - math.sqrt(35.0**2 - (66.5 - 100)**2)
y2 = 100 + math.sqrt(35.0**2 - (66.5 - 100)**2)
print(f"  y_top = {y1:.4f}, y_bottom = {y2:.4f}")

print("Intersection of x=134.5 with circle R=35.0:")
y3 = 100 - math.sqrt(35.0**2 - (134.5 - 100)**2)
y4 = 100 + math.sqrt(35.0**2 - (134.5 - 100)**2)
print(f"  y_top = {y3:.4f}, y_bottom = {y4:.4f}")

print("Intersection of y=132.5 with circle R=35.0:")
# (y - 100) = 32.5. 35^2 - 32.5^2 = 1225 - 1056.25 = 168.75.
x_left = 100 - math.sqrt(168.75)
x_right = 100 + math.sqrt(168.75)
print(f"  x_left = {x_left:.4f}, x_right = {x_right:.4f}")
