import math, sys
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

P = {}

# 1. MOUNTING HOLES (PCD 44 mm -> R = 22.0 mm from 100, 100)
delta_h = 22.0 / math.sqrt(2) # 15.55635
HOLES = {
    "H3": (100.0 - delta_h, 100.0 - delta_h), # (84.444, 84.444)
    "H4": (100.0 + delta_h, 100.0 - delta_h), # (115.556, 84.444)
    "H2": (100.0 - delta_h, 100.0 + delta_h), # (84.444, 115.556)
    "H1": (100.0 + delta_h, 100.0 + delta_h)  # (115.556, 115.556)
}
for h, (hx, hy) in HOLES.items():
    P[h] = (hx, hy, 0, 'F.Cu')

# 2. MOTOR TERMINALS U, V, W (Intact circular pads, well inside R=35mm circle)
P['J1'] = (88.5, 70.0, 0, 'F.Cu')
P['J2'] = (100.0, 69.5, 0, 'F.Cu')
P['J3'] = (111.5, 70.0, 0, 'F.Cu')

# 3. DC BUS CERAMIC CAPS (1206)
P['C_BUS1'] = (93.5, 70.0, 0, 'F.Cu')
P['C_BUS2'] = (106.5, 70.0, 0, 'F.Cu')
P['C_BUS3'] = (100.0, 66.8, 0, 'F.Cu')

# 4. MOSFETS Q1..Q6 in a straight neat row at Y = 75.8
P['Q1'] = (82.5, 75.8, 0, 'F.Cu')
P['Q2'] = (89.5, 75.8, 0, 'F.Cu')
P['Q3'] = (96.5, 75.8, 0, 'F.Cu')
P['Q4'] = (103.5, 75.8, 0, 'F.Cu')
P['Q5'] = (110.5, 75.8, 0, 'F.Cu')
P['Q6'] = (117.5, 75.8, 0, 'F.Cu')

# 5. GATE RESISTORS R1..R7
P['R1'] = (82.5, 72.5, 0, 'F.Cu')
P['R2'] = (89.5, 72.5, 0, 'F.Cu')
P['R3'] = (96.5, 72.5, 0, 'F.Cu')
P['R4'] = (103.5, 72.5, 0, 'F.Cu')
P['R5'] = (110.5, 72.5, 0, 'F.Cu')
P['R7'] = (117.5, 72.5, 0, 'F.Cu')

# 6. SHUNTS (2512) & NET TIES at Y = 82.2
P['R47'] = (91.5, 82.2, 0, 'F.Cu')
P['R48'] = (100.0, 82.2, 0, 'F.Cu')
P['R49'] = (108.5, 82.2, 0, 'F.Cu')

P['NT1'] = (89.5, 82.2, 0, 'F.Cu')
P['NT2'] = (93.5, 82.2, 0, 'F.Cu')
P['NT3'] = (98.0, 82.2, 0, 'F.Cu')
P['NT4'] = (102.0, 82.2, 0, 'F.Cu')
P['NT5'] = (106.5, 82.2, 0, 'F.Cu')
P['NT6'] = (110.5, 82.2, 0, 'F.Cu')

# 7. BULK CAPACITORS (D10mm)
# Can centers at (74.0, 84.5) and (126.0, 84.5)
# rot=180: pin 1 at (76.5, 84.5). rot=0: pin 1 at (123.5, 84.5)
P['C_BULK1'] = (76.5, 84.5, 180, 'F.Cu')
P['C63']     = (123.5, 84.5, 0, 'F.Cu')

# 8. GATE DRIVER IC1 (QFN48) at (100.0, 89.0)
P['IC1'] = (100.0, 89.0, 0, 'F.Cu')

# DRV Passives around IC1:
# Left flank of IC1 (X in [88..95], Y in [85..93]):
P['C1']  = (94.5, 85.8, 0, 'F.Cu')
P['C2']  = (94.5, 87.5, 0, 'F.Cu')
P['C3']  = (94.5, 89.2, 0, 'F.Cu')
P['C12'] = (94.5, 90.9, 0, 'F.Cu')
P['C13'] = (94.5, 92.6, 0, 'F.Cu')

P['R6']  = (91.5, 85.8, 0, 'F.Cu')
P['R8']  = (91.5, 87.5, 0, 'F.Cu')
P['R9']  = (91.5, 89.2, 0, 'F.Cu')
P['R10'] = (91.5, 90.9, 0, 'F.Cu')
P['R50'] = (91.5, 92.6, 0, 'F.Cu')

P['TP1'] = (88.5, 88.5, 0, 'F.Cu')
P['R51'] = (88.5, 90.5, 0, 'F.Cu')
P['R52'] = (88.5, 92.5, 0, 'F.Cu')
P['TP2'] = (88.5, 94.5, 0, 'F.Cu')

# Right flank of IC1 (X in [105..110], Y in [85..95]):
P['C15'] = (105.5, 85.8, 0, 'F.Cu')
P['C18'] = (105.5, 87.5, 0, 'F.Cu')
P['C19'] = (105.5, 89.2, 0, 'F.Cu')
P['C20'] = (105.5, 90.9, 0, 'F.Cu')
P['C21'] = (105.5, 92.6, 0, 'F.Cu')

P['R55'] = (108.5, 85.8, 0, 'F.Cu')
P['R56'] = (108.5, 87.5, 0, 'F.Cu')
P['R57'] = (108.5, 89.2, 0, 'F.Cu')
P['R58'] = (108.5, 90.9, 0, 'F.Cu')
P['R59'] = (108.5, 92.6, 0, 'F.Cu')
P['R60'] = (108.5, 94.3, 0, 'F.Cu')
P['TP3'] = (108.5, 96.5, 0, 'F.Cu')

# Current sense RC filters (between IC1 and MCU at Y = 94.5..95.5):
P['R37'] = (92.0, 95.0, 0, 'F.Cu')
P['C54'] = (94.5, 95.0, 0, 'F.Cu')
P['R38'] = (97.5, 95.0, 0, 'F.Cu')
P['C55'] = (100.0, 95.0, 0, 'F.Cu')
P['R39'] = (103.0, 95.0, 0, 'F.Cu')
P['C56'] = (105.5, 95.0, 0, 'F.Cu')
P['C64'] = (106.5, 93.0, 0, 'F.Cu')

# 9. MCU U1 (LQFP-64) at (100.0, 101.0)
P['U1'] = (100.0, 101.0, 0, 'F.Cu')

# MCU Decoupling caps:
P['C4']  = (96.0, 93.5, 0, 'F.Cu')
P['C5']  = (104.0, 93.5, 0, 'F.Cu')
P['C51'] = (92.5, 98.5, 90, 'F.Cu')
P['C52'] = (92.5, 101.5, 90, 'F.Cu')
P['C53'] = (92.5, 104.5, 90, 'F.Cu')
P['C6']  = (107.5, 99.0, 90, 'F.Cu')
P['C7']  = (107.5, 102.0, 90, 'F.Cu')
P['C50'] = (107.5, 105.0, 90, 'F.Cu')
P['C10'] = (94.0, 107.8, 0, 'F.Cu')
P['C11'] = (106.0, 107.8, 0, 'F.Cu')

# MCU Crystal & Reset (West wing of MCU):
P['FB1'] = (88.5, 97.0, 0, 'F.Cu')
P['Y1']  = (85.5, 100.5, 0, 'F.Cu')
P['C8']  = (82.5, 99.0, 90, 'F.Cu')
P['C9']  = (82.5, 102.0, 90, 'F.Cu')
P['R44'] = (85.5, 104.0, 0, 'F.Cu')
P['R32'] = (88.5, 104.0, 0, 'F.Cu')
P['R34'] = (88.5, 106.5, 0, 'F.Cu')

# 10. STATUS LEDS & CAN SUBSYSTEM (Far West Wing):
P['D1']  = (76.0, 89.0, 0, 'F.Cu')
P['R33'] = (78.5, 89.0, 0, 'F.Cu')
P['D2']  = (76.0, 91.5, 0, 'F.Cu')
P['R35'] = (78.5, 91.5, 0, 'F.Cu')
P['D3']  = (76.0, 94.0, 0, 'F.Cu')
P['R36'] = (78.5, 94.0, 0, 'F.Cu')

P['U9']  = (76.0, 98.5, 0, 'F.Cu')
P['JP1'] = (76.0, 102.5, 0, 'F.Cu')
P['R45'] = (76.0, 105.0, 0, 'F.Cu')
P['R46'] = (76.0, 107.0, 0, 'F.Cu')
P['C60'] = (72.0, 97.0, 90, 'F.Cu')
P['C61'] = (72.0, 99.5, 90, 'F.Cu')
P['C62'] = (72.0, 102.0, 90, 'F.Cu')

# 11. POWER INPUT & BUCK CONVERTER (Far East Wing):
# XT30 J11:
P['J11'] = (118.0, 98.0, 270, 'F.Cu')
# Fuse F1:
P['F1']  = (113.0, 91.5, 90, 'F.Cu')
# TVS Diode D6:
P['D6']  = (124.0, 105.0, 0, 'F.Cu')

# Buck Converter:
P['L1']  = (114.5, 83.5, 0, 'F.Cu') # near H4? Let's check clearance!
P['D4']  = (122.0, 89.5, 0, 'F.Cu')
P['C16'] = (118.0, 89.5, 90, 'F.Cu')
P['C17'] = (118.0, 92.0, 90, 'F.Cu')
P['R53'] = (122.0, 92.5, 0, 'F.Cu')
P['R54'] = (122.0, 94.5, 0, 'F.Cu')

# 3.3V LDO:
P['U10'] = (112.5, 103.5, 0, 'F.Cu')
P['C57'] = (112.5, 106.0, 0, 'F.Cu')
P['C58'] = (115.5, 106.0, 0, 'F.Cu')

# 12. SOUTH CONNECTORS (Flush along flat cut Y = 120.00):
P['J8']  = (74.0,  110.30, 0, 'F.Cu') # CAN_IN 3-pin
P['J7']  = (92.25, 115.82, 0, 'F.Cu') # USB Type-C
P['J10'] = (100.25, 110.30, 0, 'F.Cu') # SWD 5-pin
P['J9']  = (121.0, 110.30, 0, 'F.Cu') # CAN_OUT 3-pin

# 13. BOTTOM LAYER COMPONENTS (B.Cu):
P['U2']  = (100.0, 100.0, 0, 'B.Cu') # MA730 Encoder
P['C14'] = (100.0, 103.5, 0, 'B.Cu')
P['R61'] = (100.0, 96.5, 90, 'B.Cu')

# USB Circuit on B.Cu:
P['U8']  = (92.25, 107.5, 0, 'B.Cu')
P['C59'] = (92.25, 110.5, 0, 'B.Cu')
P['Q7']  = (92.25, 113.5, 0, 'B.Cu')
P['R40'] = (87.5,  113.5, 0, 'B.Cu')
P['R41'] = (89.5,  113.5, 0, 'B.Cu')
P['R42'] = (95.0,  113.5, 0, 'B.Cu')
P['R43'] = (97.0,  113.5, 0, 'B.Cu')

print("Defined all 124 components!")
from test_custom_eval import custom_eval

ov, he, oob, _ = custom_eval(P)
print(f"==========================================")
print(f"TOTAL COMPONENTS: {len(P)} / 124")
print(f"OVERLAPS DETECTED: {len(ov)}")
print(f"HOLE COLLISIONS: {len(he)}")
print(f"OUT OF BOUNDS: {len(oob)}")
print(f"==========================================")
for r1, r2, dx, dy in ov:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in he:
    print(f"  HOLE: {h:8s} <--> {r:8s} : pen={pen:.2f}")
for r, msg in oob[:10]:
    print(f"  OOB: {r:8s} : {msg}")
