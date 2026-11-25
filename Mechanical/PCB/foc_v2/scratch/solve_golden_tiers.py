import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

P = {}

# 1. MOUNTING HOLES (PCD Ø44.0 mm, R = 22.0 mm from 100, 100)
delta_h = 22.0 / math.sqrt(2) # 15.55635
HOLES = {
    "H3": (100.0 - delta_h, 100.0 - delta_h), # (84.444, 84.444)
    "H4": (100.0 + delta_h, 100.0 - delta_h), # (115.556, 84.444)
    "H2": (100.0 - delta_h, 100.0 + delta_h), # (84.444, 115.556)
    "H1": (100.0 + delta_h, 100.0 + delta_h)  # (115.556, 115.556)
}
for h, (hx, hy) in HOLES.items():
    P[h] = (hx, hy, 0, 'F.Cu')

# 2. MOTOR TERMINALS (Tier 1: Y = 68.5..69.5)
P['J1'] = (88.5, 69.5, 0, 'F.Cu')
P['J2'] = (100.0, 69.0, 0, 'F.Cu')
P['J3'] = (111.5, 69.5, 0, 'F.Cu')

# DC Bus Ceramic Caps (1206)
P['C_BUS1'] = (94.0, 69.5, 0, 'F.Cu')
P['C_BUS2'] = (106.0, 69.5, 0, 'F.Cu')
P['C_BUS3'] = (100.0, 66.0, 0, 'F.Cu')

# 3. GATE RESISTORS (Tier 1.5: Y = 72.0)
P['R1'] = (81.85, 72.0, 0, 'F.Cu')
P['R2'] = (89.10, 72.0, 0, 'F.Cu')
P['R3'] = (96.35, 72.0, 0, 'F.Cu')
P['R4'] = (103.65, 72.0, 0, 'F.Cu')
P['R5'] = (110.90, 72.0, 0, 'F.Cu')
P['R7'] = (118.15, 72.0, 0, 'F.Cu')

# 4. 6 MOSFETS (Tier 2: Y = 75.8)
P['Q1'] = (81.85, 75.8, 0, 'F.Cu')
P['Q2'] = (89.10, 75.8, 0, 'F.Cu')
P['Q3'] = (96.35, 75.8, 0, 'F.Cu')
P['Q4'] = (103.65, 75.8, 0, 'F.Cu')
P['Q5'] = (110.90, 75.8, 0, 'F.Cu')
P['Q6'] = (118.15, 75.8, 0, 'F.Cu')

# 5. SHUNTS (Tier 3: Y = 81.5)
P['R47'] = (91.5, 81.5, 0, 'F.Cu')
P['R48'] = (100.0, 81.5, 0, 'F.Cu')
P['R49'] = (108.5, 81.5, 0, 'F.Cu')

P['NT1'] = (89.5, 81.5, 0, 'F.Cu')
P['NT2'] = (93.5, 81.5, 0, 'F.Cu')
P['NT3'] = (98.0, 81.5, 0, 'F.Cu')
P['NT4'] = (102.0, 81.5, 0, 'F.Cu')
P['NT5'] = (106.5, 81.5, 0, 'F.Cu')
P['NT6'] = (110.5, 81.5, 0, 'F.Cu')

# Bulk Electrolytic Caps (D10mm)
# Can center at (74.0, 84.5) and (126.0, 84.5)
P['C_BULK1'] = (76.5, 84.5, 180, 'F.Cu')
P['C63']     = (123.5, 84.5, 0, 'F.Cu')

# 6. GATE DRIVER IC1 (Tier 4: Y = 88.0)
P['IC1'] = (100.0, 88.0, 0, 'F.Cu')

# Passives on Left Flank of IC1:
P['C1']  = (94.0, 85.0, 0, 'F.Cu')
P['C2']  = (94.0, 86.8, 0, 'F.Cu')
P['C3']  = (94.0, 88.6, 0, 'F.Cu')
P['C12'] = (94.0, 90.4, 0, 'F.Cu')
P['C13'] = (94.0, 92.2, 0, 'F.Cu')

P['R6']  = (90.5, 85.0, 0, 'F.Cu')
P['R8']  = (90.5, 86.8, 0, 'F.Cu')
P['R9']  = (90.5, 88.6, 0, 'F.Cu')
P['R10'] = (90.5, 90.4, 0, 'F.Cu')
P['R50'] = (90.5, 92.2, 0, 'F.Cu')

P['TP1'] = (87.0, 87.0, 0, 'F.Cu')
P['R51'] = (87.0, 89.0, 0, 'F.Cu')
P['R52'] = (87.0, 91.0, 0, 'F.Cu')
P['TP2'] = (87.0, 93.0, 0, 'F.Cu')

# Passives on Right Flank of IC1:
P['C15'] = (106.0, 85.0, 0, 'F.Cu')
P['C18'] = (106.0, 86.8, 0, 'F.Cu')
P['C19'] = (106.0, 88.6, 0, 'F.Cu')
P['C20'] = (106.0, 90.4, 0, 'F.Cu')
P['C21'] = (106.0, 92.2, 0, 'F.Cu')

P['R55'] = (109.5, 85.0, 0, 'F.Cu')
P['R56'] = (109.5, 86.8, 0, 'F.Cu')
P['R57'] = (109.5, 88.6, 0, 'F.Cu')
P['R58'] = (109.5, 90.4, 0, 'F.Cu')
P['R59'] = (109.5, 92.2, 0, 'F.Cu')
P['R60'] = (109.5, 94.0, 0, 'F.Cu')
P['TP3'] = (109.5, 96.0, 0, 'F.Cu')

# 7. MCU U1 (Tier 5: Y = 99.5)
P['U1'] = (100.0, 99.5, 0, 'F.Cu')

# MCU Top Decoupling caps:
P['C4']  = (96.5, 92.5, 0, 'F.Cu')
P['C5']  = (103.5, 92.5, 0, 'F.Cu')

# Current Sense Filters (between IC1 and MCU at Y = 92.5..94.0):
P['R37'] = (90.0, 94.0, 0, 'F.Cu')
P['C54'] = (92.5, 94.0, 0, 'F.Cu')
P['R38'] = (97.0, 94.0, 0, 'F.Cu')
P['C55'] = (100.0, 94.0, 0, 'F.Cu')
P['R39'] = (103.0, 94.0, 0, 'F.Cu')
P['C56'] = (106.0, 94.0, 0, 'F.Cu')
P['C64'] = (107.0, 92.5, 0, 'F.Cu')

# MCU Left/Right Decoupling caps:
P['C51'] = (92.5, 97.0, 90, 'F.Cu')
P['C52'] = (92.5, 99.5, 90, 'F.Cu')
P['C53'] = (92.5, 102.0, 90, 'F.Cu')

P['C6']  = (107.5, 97.5, 90, 'F.Cu')
P['C7']  = (107.5, 100.0, 90, 'F.Cu')
P['C50'] = (107.5, 102.5, 90, 'F.Cu')

# MCU Bottom Decoupling caps:
P['C10'] = (94.0, 106.5, 0, 'F.Cu')
P['C11'] = (106.0, 106.5, 0, 'F.Cu')

# MCU Crystal & Reset (West wing of MCU):
P['FB1'] = (88.5, 96.0, 0, 'F.Cu')
P['Y1']  = (85.5, 99.0, 0, 'F.Cu')
P['C8']  = (82.5, 97.5, 90, 'F.Cu')
P['C9']  = (82.5, 100.5, 90, 'F.Cu')
P['R44'] = (85.5, 102.5, 0, 'F.Cu')
P['R32'] = (88.5, 102.5, 0, 'F.Cu')
P['R34'] = (88.5, 105.0, 0, 'F.Cu')

# 8. STATUS LEDS & CAN SUBSYSTEM (Far West Wing):
P['D1']  = (76.0, 89.0, 0, 'F.Cu')
P['R33'] = (78.5, 89.0, 0, 'F.Cu')
P['D2']  = (76.0, 91.5, 0, 'F.Cu')
P['R35'] = (78.5, 91.5, 0, 'F.Cu')
P['D3']  = (76.0, 94.0, 0, 'F.Cu')
P['R36'] = (78.5, 94.0, 0, 'F.Cu')

P['U9']  = (76.0, 98.0, 0, 'F.Cu')
P['JP1'] = (76.0, 101.5, 0, 'F.Cu')
P['R45'] = (76.0, 104.0, 0, 'F.Cu')
P['R46'] = (76.0, 106.0, 0, 'F.Cu')
P['C60'] = (72.0, 96.5, 90, 'F.Cu')
P['C61'] = (72.0, 99.0, 90, 'F.Cu')
P['C62'] = (72.0, 101.5, 90, 'F.Cu')

# 9. POWER INPUT & BUCK CONVERTER (Far East Wing):
# XT30 J11 (rot=270, outer East):
P['J11'] = (120.0, 98.0, 270, 'F.Cu')
# Fuse F1 (rot=0, horizontal above J9):
P['F1']  = (114.5, 104.0, 0, 'F.Cu')
# TVS Diode D6:
P['D6']  = (124.0, 105.0, 0, 'F.Cu')

# Buck Converter:
P['L1']  = (122.5, 90.0, 0, 'F.Cu')
P['D4']  = (115.5, 88.5, 0, 'F.Cu')
P['C16'] = (115.5, 92.0, 90, 'F.Cu')
P['C17'] = (118.0, 92.0, 90, 'F.Cu')
P['R53'] = (122.0, 84.5, 0, 'F.Cu')
P['R54'] = (122.0, 86.5, 0, 'F.Cu')

# 3.3V LDO:
P['U10'] = (112.5, 97.0, 0, 'F.Cu')
P['C57'] = (112.5, 100.0, 0, 'F.Cu')
P['C58'] = (115.5, 100.0, 0, 'F.Cu')

# 10. SOUTH CONNECTORS (Tier 6: Flush along flat cut Y = 120.00):
P['J8']  = (74.0,  110.30, 0, 'F.Cu') # CAN_IN 3-pin
P['J7']  = (92.25, 115.82, 0, 'F.Cu') # USB Type-C
P['J10'] = (100.25, 110.30, 0, 'F.Cu') # SWD 5-pin
P['J9']  = (121.0, 110.30, 0, 'F.Cu') # CAN_OUT 3-pin

# 11. BOTTOM LAYER COMPONENTS (B.Cu):
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
