import math, re, json
import test_courtyards

local_boxes = test_courtyards.parse_footprints()

cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 120.2

# 4 Mounting holes at PCD 44mm (r = 22.0mm)
# H1: (115.556, 115.556), H2: (84.444, 115.556), H3: (84.444, 84.444), H4: (115.556, 84.444)
holes = {
    'H1': (115.556, 115.556),
    'H2': (84.444, 115.556),
    'H3': (84.444, 84.444),
    'H4': (115.556, 84.444)
}

# Base positions for major blocks:
pos = {}

# 1. Mounting Holes
pos['H1'] = (115.556, 115.556, 0.0)
pos['H2'] = (84.444, 115.556, 0.0)
pos['H3'] = (84.444, 84.444, 0.0)
pos['H4'] = (115.556, 84.444, 0.0)

# 2. South Connectors (Front faces perfectly flush at Y = 120.00 mm):
# J8: CAN_IN (3-pin XH)
pos['J8'] = (74.0, 110.80, 0.0)
# J7: USB Type-C
pos['J7'] = (92.5, 116.21, 0.0)
# J10: SWD (5-pin XH)
pos['J10'] = (100.0, 110.80, 0.0)
# J9: CAN_OUT (3-pin XH)
pos['J9'] = (121.0, 110.80, 0.0)

# 3. Motor Terminals (U, V, W):
# generous copper margin > 1.8mm to edge
pos['J1'] = (85.0, 72.0, 0.0)
pos['J2'] = (100.0, 71.0, 0.0)
pos['J3'] = (115.0, 72.0, 0.0)

# 4. MOSFET Inverter Bridge (Q1..Q6):
# Placed in a neat horizontal line at Y = 78.50 mm (rot = 90 / 270)
# Width 7.16, Height 5.66 -> Y in [78.5 - 2.83, 78.5 + 2.83] = [75.67, 81.33]
# Distance to J1..J3 at Y=72.0 (bottom 73.88): 75.67 - 73.88 = 1.79 mm margin!
pos['Q1'] = (83.5, 78.5, 90.0)
pos['Q2'] = (90.1, 78.5, 270.0)
pos['Q3'] = (96.7, 78.5, 90.0)
pos['Q4'] = (103.3, 78.5, 270.0)
pos['Q5'] = (109.9, 78.5, 90.0)
pos['Q6'] = (116.5, 78.5, 270.0)

# DC-link high frequency ceramic capacitors (C_BUS1..3):
# Placed directly above/below FET pairs
pos['C_BUS1'] = (86.8, 83.5, 0.0)
pos['C_BUS2'] = (100.0, 83.5, 0.0)
pos['C_BUS3'] = (113.2, 83.5, 0.0)

# Current sense shunts (R1, R2, R3) for Phase U, V, W:
pos['R1'] = (90.1, 83.5, 90.0)
pos['R2'] = (103.3, 83.5, 90.0)
pos['R3'] = (116.5, 83.5, 90.0)

# 5. Gate Driver IC (IC1: DRV8353):
# Placed in the center at Y = 90.00 mm
pos['IC1'] = (100.0, 90.0, 0.0)

# 6. MCU (U1: STM32G473 LQFP-64):
# Placed in the center at Y = 103.50 mm
# Y in [103.5 - 6.7, 103.5 + 6.7] = [96.8, 110.2]
# Margin to IC1 at Y=90 (bottom 94.13): 96.8 - 94.13 = 2.67 mm!
# Margin to J7 at Y=116.21 (top 111.36): 111.36 - 110.2 = 1.16 mm!
pos['U1'] = (100.0, 103.5, 0.0)

# 7. Power Input & Protection (East Wing):
# XT30 (J11)
pos['J11'] = (120.5, 96.0, 270.0)
# Fuse F1
pos['F1'] = (122.0, 105.0, 0.0)
# TVS Diode D6
pos['D6'] = (122.0, 112.0, 0.0)
# Protection FET Q7
pos['Q7'] = (122.0, 88.0, 0.0)

# 8. Bulk Electrolytic Cap (C_BULK1):
# West wing at (76.0, 85.0)
pos['C_BULK1'] = (76.0, 85.0, 180.0)

print(f"Base layout placed {len(pos)} primary components.")
