import math

# Center of board:
CX, CY = 100.0, 100.0
R_BOARD = 35.0

# 4 Holes PCD 44 mm (R = 22.0 mm)
delta_h = 22.0 / math.sqrt(2) # 15.55635 mm
HOLES = {
    "H3": (CX - delta_h, CY - delta_h), # NW (84.444, 84.444)
    "H4": (CX + delta_h, CY - delta_h), # NE (115.556, 84.444)
    "H2": (CX - delta_h, CY + delta_h), # SW (84.444, 115.556)
    "H1": (CX + delta_h, CY + delta_h), # SE (115.556, 115.556)
}
R_SCREW_KEEPOUT = 3.0 # keepout radius (D = 6.0 mm)

# Board cuts:
# South flat cut at y = 124.0 or 125.0
# East flat cut at x = 132.0

def dist_to_center(x, y):
    return math.hypot(x - CX, y - CY)

print(f"Holes: H3={HOLES['H3']}, H4={HOLES['H4']}, H2={HOLES['H2']}, H1={HOLES['H1']}")
