import math
import sys
import re

# Let's verify the entire layout coordinates dictionary P_test
# All 124 components

sys.path.insert(0, 'scratch')
from verify_all_clean import P

P_test = dict(P)

# 1. South Connectors: Front faces flush at Y = 123.50
P_test['J8']  = (75.0, 114.30, 0, 'F.Cu')   # CAN_IN
P_test['J9']  = (86.5, 114.30, 0, 'F.Cu')   # CAN_OUT
P_test['J7']  = (100.0, 119.71, 0, 'F.Cu')  # Type-C
P_test['J10'] = (111.5, 114.30, 0, 'F.Cu')  # SWD

# 2. CAN Bus Subsystem: Move deep inside West wing (Y in [98 .. 106])
P_test['U9']  = (76.0, 101.0, 0, 'F.Cu')
P_test['JP1'] = (76.0, 105.0, 0, 'F.Cu')
P_test['R45'] = (76.0, 107.5, 0, 'F.Cu')
P_test['R46'] = (76.0, 109.5, 0, 'F.Cu')
P_test['C60'] = (71.5, 99.0, 90, 'F.Cu')
P_test['C61'] = (71.5, 101.5, 90, 'F.Cu')
P_test['C62'] = (71.5, 104.0, 90, 'F.Cu')

# 3. Power Input Subsystem: Move deep inside East wing (Y in [101 .. 116])
P_test['J11'] = (120.5, 101.0, 270, 'F.Cu') # XT30
P_test['F1']  = (122.0, 111.0, 90, 'F.Cu')   # Fuse 10A
P_test['D6']  = (122.0, 117.0, 90, 'F.Cu')   # TVS Diode

# 4. Status LEDs & Resistors (West area X = 80.0, Y in [105 .. 112])
P_test['D1']  = (80.0, 105.0, 0, 'F.Cu')
P_test['R33'] = (82.5, 105.0, 0, 'F.Cu')
P_test['D2']  = (80.0, 107.5, 0, 'F.Cu')
P_test['R35'] = (82.5, 107.5, 0, 'F.Cu')
P_test['D3']  = (80.0, 110.0, 0, 'F.Cu')
P_test['R36'] = (82.5, 110.0, 0, 'F.Cu')

# 5. USB Circuit Passives on B.Cu (aligned near J7 at Y = 118..121)
P_test['U8']  = (96.0, 118.0, 0, 'B.Cu')
P_test['C59'] = (100.0, 117.5, 0, 'B.Cu')
P_test['Q7']  = (104.0, 118.0, 0, 'B.Cu')
P_test['R40'] = (95.0, 120.5, 0, 'B.Cu')
P_test['R41'] = (98.0, 120.5, 0, 'B.Cu')
P_test['R42'] = (102.0, 120.5, 0, 'B.Cu')
P_test['R43'] = (105.0, 120.5, 0, 'B.Cu')

# 6. Motor wire pads (North: deep inside board, complete circular pads)
P_test['J1'] = (88.0, 71.0, 0, 'F.Cu')
P_test['J2'] = (100.0, 71.0, 0, 'F.Cu')
P_test['J3'] = (112.0, 71.0, 0, 'F.Cu')

# Verify that ALL 124 components are strictly inside Circle R = 35.0 and above Y_cut = 123.5!
print(f"Total components in P_test: {len(P_test)}")

outside = []
for ref, (x, y, rot, layer) in P_test.items():
    r = math.hypot(x - 100, y - 100)
    if r > 34.5:
        outside.append((ref, x, y, r))

print(f"Components with center radius > 34.5 mm: {len(outside)}")
for o in outside:
    print(f"  {o[0]}: ({o[1]}, {o[2]}) r={o[3]:.2f}")
