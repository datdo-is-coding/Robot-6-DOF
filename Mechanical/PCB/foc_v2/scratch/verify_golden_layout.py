import math, re, json
import test_courtyards

local_boxes = test_courtyards.parse_footprints()

cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 120.2
x_left = round(100.0 - math.sqrt(35**2 - (y_cut - 100)**2), 4)
x_right = round(100.0 + math.sqrt(35**2 - (y_cut - 100)**2), 4)

# 4 Holes
holes = {
    'H1': (115.556, 115.556),
    'H2': (84.444, 115.556),
    'H3': (84.444, 84.444),
    'H4': (115.556, 84.444)
}

# Define the complete P_golden layout for all 124 components
P_golden = {}

# 1. Mounting Holes
P_golden['H1'] = (115.556, 115.556, 0.0, 'F.Cu')
P_golden['H2'] = (84.444, 115.556, 0.0, 'F.Cu')
P_golden['H3'] = (84.444, 84.444, 0.0, 'F.Cu')
P_golden['H4'] = (115.556, 84.444, 0.0, 'F.Cu')

# 2. South Connectors (Flush at Y_front = 120.00 mm)
P_golden['J8']  = (74.0,  110.80, 0.0, 'F.Cu')   # CAN_IN
P_golden['J7']  = (92.5,  116.21, 0.0, 'F.Cu')   # Type-C
P_golden['J10'] = (100.0, 110.80, 0.0, 'F.Cu')   # SWD
P_golden['J9']  = (121.0, 110.80, 0.0, 'F.Cu')   # CAN_OUT

# 3. Motor Terminals
P_golden['J1'] = (85.0,  72.0, 0.0, 'F.Cu')
P_golden['J2'] = (100.0, 71.0, 0.0, 'F.Cu')
P_golden['J3'] = (115.0, 72.0, 0.0, 'F.Cu')

# 4. Inverter MOSFETs Q1..Q6
P_golden['Q1'] = (83.5,  78.5, 90.0,  'F.Cu')
P_golden['Q2'] = (90.1,  78.5, 270.0, 'F.Cu')
P_golden['Q3'] = (96.7,  78.5, 90.0,  'F.Cu')
P_golden['Q4'] = (103.3, 78.5, 270.0, 'F.Cu')
P_golden['Q5'] = (109.9, 78.5, 90.0,  'F.Cu')
P_golden['Q6'] = (116.5, 78.5, 270.0, 'F.Cu')

# DC Bus Caps
P_golden['C_BUS1'] = (84.0,  83.0, 0.0, 'F.Cu')
P_golden['C_BUS2'] = (100.0, 83.0, 0.0, 'F.Cu')
P_golden['C_BUS3'] = (116.0, 83.0, 0.0, 'F.Cu')

# Shunts
P_golden['R47'] = (93.0,  84.5, 90.0, 'F.Cu')
P_golden['R48'] = (100.0, 84.5, 90.0, 'F.Cu')
P_golden['R49'] = (107.0, 84.5, 90.0, 'F.Cu')

# Net ties
P_golden['NT1'] = (92.5,  84.5, 90.0, 'F.Cu')
P_golden['NT2'] = (93.5,  84.5, 90.0, 'F.Cu')
P_golden['NT3'] = (99.5,  84.5, 90.0, 'F.Cu')
P_golden['NT4'] = (100.5, 84.5, 90.0, 'F.Cu')
P_golden['NT5'] = (106.5, 84.5, 90.0, 'F.Cu')
P_golden['NT6'] = (107.5, 84.5, 90.0, 'F.Cu')

# Gate resistors
P_golden['R1'] = (83.5,  75.0, 0.0, 'F.Cu')
P_golden['R2'] = (89.5,  75.0, 0.0, 'F.Cu')
P_golden['R3'] = (96.0,  75.0, 0.0, 'F.Cu')
P_golden['R4'] = (102.5, 75.0, 0.0, 'F.Cu')
P_golden['R5'] = (109.5, 75.0, 0.0, 'F.Cu')
P_golden['R7'] = (116.5, 75.0, 0.0, 'F.Cu')

# Bulk caps
P_golden['C_BULK1'] = (74.0, 85.0, 180.0, 'F.Cu')
P_golden['C63']     = (126.0, 85.0, 0.0,   'F.Cu')

# Gate Driver IC1
P_golden['IC1'] = (100.0, 90.0, 0.0, 'F.Cu')

# Bootstrap & DRV caps
P_golden['C1']  = (94.0,  88.5, 0.0, 'F.Cu')
P_golden['C2']  = (94.0,  90.5, 0.0, 'F.Cu')
P_golden['C3']  = (94.0,  92.5, 0.0, 'F.Cu')
P_golden['C12'] = (94.0,  95.0, 0.0, 'F.Cu')
P_golden['C13'] = (94.0,  97.5, 0.0, 'F.Cu')

P_golden['C15'] = (106.0, 88.5, 0.0, 'F.Cu')
P_golden['C18'] = (106.0, 90.5, 0.0, 'F.Cu')
P_golden['C19'] = (106.0, 92.5, 0.0, 'F.Cu')
P_golden['C20'] = (106.0, 94.5, 0.0, 'F.Cu')
P_golden['C21'] = (106.0, 96.5, 0.0, 'F.Cu')
P_golden['C64'] = (106.0, 98.5, 0.0, 'F.Cu')

# DRV config resistors
P_golden['R6']  = (90.5, 88.5, 0.0, 'F.Cu')
P_golden['R8']  = (90.5, 90.5, 0.0, 'F.Cu')
P_golden['R9']  = (90.5, 92.5, 0.0, 'F.Cu')
P_golden['R10'] = (90.5, 94.5, 0.0, 'F.Cu')
P_golden['R50'] = (90.5, 96.5, 0.0, 'F.Cu')
P_golden['R51'] = (88.0, 94.5, 0.0, 'F.Cu')
P_golden['R52'] = (88.0, 96.5, 0.0, 'F.Cu')

P_golden['R55'] = (109.5, 88.5, 0.0, 'F.Cu')
P_golden['R56'] = (109.5, 90.5, 0.0, 'F.Cu')
P_golden['R57'] = (109.5, 92.5, 0.0, 'F.Cu')
P_golden['R58'] = (109.5, 94.5, 0.0, 'F.Cu')
P_golden['R59'] = (109.5, 96.5, 0.0, 'F.Cu')
P_golden['R60'] = (109.5, 98.5, 0.0, 'F.Cu')

# Power Input East Wing
P_golden['J11'] = (120.5, 96.0, 270.0, 'F.Cu')
P_golden['F1']  = (122.0, 105.0, 90.0,  'F.Cu')
P_golden['D6']  = (122.0, 112.0, 90.0,  'F.Cu')

# Buck Converter
P_golden['L1']  = (120.0, 89.0, 0.0,  'F.Cu')
P_golden['D4']  = (114.5, 90.0, 0.0,  'F.Cu')
P_golden['C16'] = (114.5, 93.0, 90.0, 'F.Cu')
P_golden['C17'] = (114.5, 96.0, 90.0, 'F.Cu')
P_golden['R53'] = (118.0, 93.0, 0.0,  'F.Cu')
P_golden['R54'] = (118.0, 95.0, 0.0,  'F.Cu')

# MCU U1
P_golden['U1']  = (100.0, 103.5, 0.0, 'F.Cu')

# MCU caps & pins
P_golden['C4']  = (96.5,  98.0, 0.0, 'F.Cu')
P_golden['C5']  = (103.5, 98.0, 0.0, 'F.Cu')
P_golden['C10'] = (90.0, 108.5, 0.0, 'F.Cu')
P_golden['C11'] = (110.0, 108.5, 0.0, 'F.Cu')

P_golden['C51'] = (91.5, 101.0, 90.0, 'F.Cu')
P_golden['C52'] = (91.5, 103.5, 90.0, 'F.Cu')
P_golden['C53'] = (91.5, 106.0, 90.0, 'F.Cu')

P_golden['C6']  = (108.5, 101.0, 90.0, 'F.Cu')
P_golden['C7']  = (108.5, 103.5, 90.0, 'F.Cu')
P_golden['C50'] = (108.5, 106.0, 90.0, 'F.Cu')

# 3.3V LDO
P_golden['U10'] = (114.0, 102.0, 0.0, 'F.Cu')
P_golden['C57'] = (114.0, 105.0, 0.0, 'F.Cu')
P_golden['C58'] = (114.0, 107.0, 0.0, 'F.Cu')

# Crystal Y1 & passives
P_golden['FB1'] = (88.5, 99.0, 0.0, 'F.Cu')
P_golden['Y1']  = (86.0, 102.5, 0.0, 'F.Cu')
P_golden['C8']  = (82.5, 101.0, 90.0, 'F.Cu')
P_golden['C9']  = (82.5, 103.5, 90.0, 'F.Cu')
P_golden['R44'] = (85.5, 105.5, 0.0, 'F.Cu')
P_golden['R32'] = (88.5, 105.5, 0.0, 'F.Cu')
P_golden['R34'] = (88.5, 107.5, 0.0, 'F.Cu')

# CAN Subsystem (West Wing)
P_golden['U9']  = (76.0, 99.0, 0.0, 'F.Cu')
P_golden['JP1'] = (76.0, 102.5, 0.0, 'F.Cu')
P_golden['R45'] = (76.0, 105.0, 0.0, 'F.Cu')
P_golden['R46'] = (76.0, 107.0, 0.0, 'F.Cu')
P_golden['C60'] = (72.0, 97.0, 90.0, 'F.Cu')
P_golden['C61'] = (72.0, 99.5, 90.0, 'F.Cu')
P_golden['C62'] = (72.0, 102.0, 90.0, 'F.Cu')

# Status LEDs
P_golden['D1']  = (76.0, 89.0, 0.0, 'F.Cu')
P_golden['R33'] = (79.0, 89.0, 0.0, 'F.Cu')
P_golden['D2']  = (76.0, 91.5, 0.0, 'F.Cu')
P_golden['R35'] = (79.0, 91.5, 0.0, 'F.Cu')
P_golden['D3']  = (76.0, 94.0, 0.0, 'F.Cu')
P_golden['R36'] = (79.0, 94.0, 0.0, 'F.Cu')

# Current sense filters & test points
P_golden['R37'] = (91.0, 99.0, 0.0, 'F.Cu')
P_golden['C54'] = (93.0, 99.0, 0.0, 'F.Cu')
P_golden['R38'] = (97.0, 99.0, 0.0, 'F.Cu')
P_golden['C55'] = (99.0, 99.0, 0.0, 'F.Cu')
P_golden['R39'] = (103.0, 99.0, 0.0, 'F.Cu')
P_golden['C56'] = (105.0, 99.0, 0.0, 'F.Cu')
P_golden['TP1'] = (86.0, 89.0, 0.0, 'F.Cu')
P_golden['TP2'] = (88.0, 99.0, 0.0, 'F.Cu')
P_golden['TP3'] = (109.5, 99.0, 0.0, 'F.Cu')

# Bottom USB Passives on B.Cu
P_golden['U8']  = (92.5, 110.0, 0.0, 'B.Cu')
P_golden['C59'] = (92.5, 113.0, 0.0, 'B.Cu')
P_golden['Q7']  = (100.0, 116.0, 0.0, 'B.Cu')
P_golden['U2']  = (92.5, 116.0, 0.0, 'B.Cu')
P_golden['R40'] = (88.0, 116.0, 0.0, 'B.Cu')
P_golden['R41'] = (89.5, 116.0, 0.0, 'B.Cu')
P_golden['R42'] = (95.5, 116.0, 0.0, 'B.Cu')
P_golden['R43'] = (97.0, 116.0, 0.0, 'B.Cu')

print(f"P_golden configured with {len(P_golden)} components.")

# Check missing
all_refs = set(local_boxes.keys())
missing = all_refs - set(P_golden.keys())
print(f"Missing from P_golden: {missing}")
