import math

cx, cy = 100.0, 100.0
R = 35.0

# 1. South flat cut: y = 125.0
y_south = 125.0
dx_south = math.sqrt(R*R - (y_south - cy)**2) # 24.494897
pt_S1 = (cx - dx_south, y_south) # (75.505, 125.0) - bottom-left of flat cut
pt_S2 = (cx + dx_south, y_south) # (124.495, 125.0) - bottom-right of flat cut

# 2. East flat cut: x = 132.0
x_east = 132.0
dy_east = math.sqrt(R*R - (x_east - cx)**2) # 14.177447
pt_E1 = (x_east, cy - dy_east) # (132.0, 85.823) - top of east flat cut
pt_E2 = (x_east, cy + dy_east) # (132.0, 114.177) - bottom of east flat cut

print(f"S1: {pt_S1}")
print(f"S2: {pt_S2}")
print(f"E1: {pt_E1}")
print(f"E2: {pt_E2}")

# Arcs:
# Arc 1: From pt_E2 to pt_S2 along circle (R=35)
# Angle of E2:
ang_E2 = math.atan2(pt_E2[1]-cy, pt_E2[0]-cx) # ~ 23.9 deg
ang_S2 = math.atan2(pt_S2[1]-cy, pt_S2[0]-cx) # ~ 45.6 deg
ang_mid_SE = (ang_E2 + ang_S2) / 2
pt_mid_SE = (cx + R*math.cos(ang_mid_SE), cy + R*math.sin(ang_mid_SE))
print(f"SE Arc: start {pt_E2}, mid {pt_mid_SE}, end {pt_S2}")

# Line 1: South flat cut from pt_S2 to pt_S1 (or S1 to S2)
print(f"South line: from {pt_S2} to {pt_S1}")

# Arc 2: Major arc from pt_S1 clockwise around to pt_E1
# ang_S1 = atan2(25, -24.495) = ~134.4 deg
# ang_E1 = atan2(-14.177, 32) = ~-23.9 deg = 336.1 deg
# This is a large arc (~200 deg) spanning NW, North, NE.
# In KiCad gr_arc, max angle for stable arc is <= 180 deg. So we can split into 2 arcs:
# Arc 2A: from pt_S1 (134.4 deg) to West/North-West (e.g. angle 180 deg: (65, 100))
# Arc 2B: from (65, 100) through North (100, 65) to pt_E1 (132, 85.823)
ang_S1 = math.atan2(pt_S1[1]-cy, pt_S1[0]-cx)
ang_W = math.pi # (65, 100)
ang_mid_W = (ang_S1 + ang_W) / 2
pt_mid_W = (cx + R*math.cos(ang_mid_W), cy + R*math.sin(ang_mid_W))

ang_N = -math.pi / 2 # (100, 65)
ang_E1 = math.atan2(pt_E1[1]-cy, pt_E1[0]-cx)
# From W (180 deg) to N (270 deg / -90 deg): mid is 225 deg (-135 deg)
pt_mid_NW = (cx + R*math.cos(-3*math.pi/4), cy + R*math.sin(-3*math.pi/4))
# From N (-90 deg) to E1 (-23.9 deg): mid is (-90 + -23.9)/2 = -56.95 deg
ang_mid_NE = (-math.pi/2 + ang_E1) / 2
pt_mid_NE = (cx + R*math.cos(ang_mid_NE), cy + R*math.sin(ang_mid_NE))

print(f"Arc S1->W: start {pt_S1}, mid {pt_mid_W}, end (65, 100)")
print(f"Arc W->N: start (65, 100), mid {pt_mid_NW}, end (100, 65)")
print(f"Arc N->E1: start (100, 65), mid {pt_mid_NE}, end {pt_E1}")
print(f"East line: from {pt_E1} to {pt_E2}")
