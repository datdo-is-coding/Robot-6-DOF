import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

from solve_zero_drc_golden import P, HOLES, ALLOWED, get_custom_bbox

# Clean up all minor overlaps across the board first:
P_base = dict(P)

# 1. Motor wire terminals (inside R=35mm circle):
P_base['J1'] = (90.0, 71.0, 0, 'F.Cu')
P_base['J2'] = (100.0, 70.0, 0, 'F.Cu')
P_base['J3'] = (110.0, 71.0, 0, 'F.Cu')

# DC Bus caps:
P_base['C_BUS1'] = (94.5, 70.0, 0, 'F.Cu')
P_base['C_BUS2'] = (105.5, 70.0, 0, 'F.Cu')
P_base['C_BUS3'] = (100.0, 71.5, 90, 'F.Cu')

# Gate resistors:
P_base['R1'] = (81.85, 72.0, 0, 'F.Cu')
P_base['R2'] = (89.10, 72.0, 0, 'F.Cu')
P_base['R3'] = (96.00, 72.0, 0, 'F.Cu')
P_base['R4'] = (104.00, 72.0, 0, 'F.Cu')
P_base['R5'] = (110.90, 72.0, 0, 'F.Cu')
P_base['R7'] = (118.15, 72.0, 0, 'F.Cu')

# MOSFETs:
P_base['Q1'] = (81.85, 76.0, 0, 'F.Cu')
P_base['Q2'] = (89.10, 76.0, 0, 'F.Cu')
P_base['Q3'] = (96.35, 76.0, 0, 'F.Cu')
P_base['Q4'] = (103.65, 76.0, 0, 'F.Cu')
P_base['Q5'] = (110.90, 76.0, 0, 'F.Cu')
P_base['Q6'] = (118.15, 76.0, 0, 'F.Cu')

# Shunts:
P_base['R47'] = (91.5, 81.2, 0, 'F.Cu')
P_base['R48'] = (100.0, 81.2, 0, 'F.Cu')
P_base['R49'] = (108.5, 81.2, 0, 'F.Cu')

P_base['NT1'] = (89.5, 81.2, 0, 'F.Cu')
P_base['NT2'] = (93.5, 81.2, 0, 'F.Cu')
P_base['NT3'] = (98.0, 81.2, 0, 'F.Cu')
P_base['NT4'] = (102.0, 81.2, 0, 'F.Cu')
P_base['NT5'] = (106.5, 81.2, 0, 'F.Cu')
P_base['NT6'] = (110.5, 81.2, 0, 'F.Cu')

# Bulk caps:
P_base['C_BULK1'] = (76.5, 86.5, 180, 'F.Cu')
P_base['C63']     = (123.5, 86.5, 0, 'F.Cu')

# IC1 at Y = 87.5:
P_base['IC1'] = (100.0, 87.5, 0, 'F.Cu')

P_base['C1']  = (94.0, 84.5, 0, 'F.Cu')
P_base['C2']  = (94.0, 86.2, 0, 'F.Cu')
P_base['C3']  = (94.0, 87.9, 0, 'F.Cu')
P_base['C12'] = (94.0, 89.7, 0, 'F.Cu')
P_base['C13'] = (94.0, 91.5, 0, 'F.Cu')

P_base['R6']  = (90.5, 84.5, 0, 'F.Cu')
P_base['R8']  = (90.5, 86.2, 0, 'F.Cu')
P_base['R9']  = (90.5, 87.9, 0, 'F.Cu')
P_base['R10'] = (90.5, 89.7, 0, 'F.Cu')
P_base['R50'] = (90.5, 91.5, 0, 'F.Cu')

P_base['TP1'] = (87.5, 87.0, 0, 'F.Cu')
P_base['R51'] = (87.5, 89.0, 0, 'F.Cu')
P_base['R52'] = (87.5, 91.0, 0, 'F.Cu')
P_base['TP2'] = (87.5, 93.0, 0, 'F.Cu')

P_base['C15'] = (106.0, 84.5, 0, 'F.Cu')
P_base['C18'] = (106.0, 86.2, 0, 'F.Cu')
P_base['C19'] = (106.0, 87.9, 0, 'F.Cu')
P_base['C20'] = (106.0, 89.7, 0, 'F.Cu')
P_base['C21'] = (106.0, 91.5, 0, 'F.Cu')

P_base['R55'] = (109.5, 84.5, 0, 'F.Cu')
P_base['R56'] = (109.5, 86.2, 0, 'F.Cu')
P_base['R57'] = (109.5, 87.9, 0, 'F.Cu')
P_base['R58'] = (109.5, 89.7, 0, 'F.Cu')
P_base['R59'] = (109.5, 91.5, 0, 'F.Cu')
P_base['R60'] = (109.5, 93.2, 0, 'F.Cu')
P_base['TP3'] = (109.5, 95.2, 0, 'F.Cu')

# MCU U1 at Y = 100.5:
P_base['U1'] = (100.0, 100.5, 0, 'F.Cu')

# MCU Top Decoupling caps (Y = 93.0):
P_base['C4']  = (96.5, 93.0, 0, 'F.Cu')
P_base['C5']  = (103.5, 93.0, 0, 'F.Cu')

# Current Sense Filters (Y = 94.5):
P_base['R37'] = (89.0, 95.0, 0, 'F.Cu')
P_base['C54'] = (91.5, 95.0, 0, 'F.Cu')
P_base['R38'] = (96.5, 94.8, 0, 'F.Cu')
P_base['C55'] = (100.0, 94.8, 0, 'F.Cu')
P_base['R39'] = (103.5, 94.8, 0, 'F.Cu')
P_base['C56'] = (106.5, 94.8, 0, 'F.Cu')
P_base['C64'] = (108.5, 93.0, 0, 'F.Cu')

# MCU Left/Right Decoupling caps:
P_base['C51'] = (92.5, 97.5, 90, 'F.Cu')
P_base['C52'] = (92.5, 100.5, 90, 'F.Cu')
P_base['C53'] = (92.5, 103.5, 90, 'F.Cu')

P_base['C6']  = (107.5, 97.5, 90, 'F.Cu')
P_base['C7']  = (107.5, 100.5, 90, 'F.Cu')
P_base['C50'] = (107.5, 103.5, 90, 'F.Cu')

# MCU Bottom Decoupling caps (flanks outside U1):
P_base['C10'] = (91.0, 106.5, 0, 'F.Cu')
P_base['C11'] = (109.0, 106.5, 0, 'F.Cu')

# Crystal & Reset:
P_base['FB1'] = (88.5, 97.5, 0, 'F.Cu')
P_base['Y1']  = (85.5, 100.5, 0, 'F.Cu')
P_base['C8']  = (82.5, 99.0, 90, 'F.Cu')
P_base['C9']  = (82.5, 102.0, 90, 'F.Cu')
P_base['R44'] = (85.5, 103.5, 0, 'F.Cu')
P_base['R32'] = (88.5, 103.5, 0, 'F.Cu')
P_base['R34'] = (88.5, 105.8, 0, 'F.Cu')

# Status LEDs (Y = 101..106):
P_base['D1']  = (75.0, 101.5, 0, 'F.Cu')
P_base['R33'] = (78.5, 101.5, 0, 'F.Cu')
P_base['D2']  = (75.0, 103.5, 0, 'F.Cu')
P_base['R35'] = (78.5, 103.5, 0, 'F.Cu')
P_base['D3']  = (75.0, 105.5, 0, 'F.Cu')
P_base['R36'] = (78.5, 105.5, 0, 'F.Cu')

# CAN Subsystem (Y = 92..99):
P_base['U9']  = (76.0, 94.5, 0, 'F.Cu')
P_base['JP1'] = (76.0, 98.0, 0, 'F.Cu')
P_base['R45'] = (79.0, 98.0, 0, 'F.Cu')
P_base['R46'] = (81.5, 98.0, 0, 'F.Cu')
P_base['C60'] = (72.0, 91.5, 90, 'F.Cu')
P_base['C61'] = (72.0, 94.5, 90, 'F.Cu')
P_base['C62'] = (72.0, 97.5, 90, 'F.Cu')

# South Connectors:
P_base['J8']  = (74.0,  110.30, 0, 'F.Cu')
P_base['J7']  = (92.25, 115.82, 0, 'F.Cu')
P_base['J10'] = (100.25, 110.30, 0, 'F.Cu')
P_base['J9']  = (121.0, 110.30, 0, 'F.Cu')

# Bottom layer:
P_base['U2']  = (100.0, 100.0, 0, 'B.Cu')
P_base['C14'] = (100.0, 103.5, 0, 'B.Cu')
P_base['R61'] = (100.0, 96.0, 90, 'B.Cu')

P_base['U8']  = (92.25, 107.5, 0, 'B.Cu')
P_base['C59'] = (92.25, 110.5, 0, 'B.Cu')
P_base['Q7']  = (92.25, 113.5, 0, 'B.Cu')
P_base['R40'] = (86.0,  118.0, 0, 'B.Cu')
P_base['R41'] = (89.5,  118.0, 0, 'B.Cu')
P_base['R42'] = (95.0,  118.0, 0, 'B.Cu')
P_base['R43'] = (98.5,  118.0, 0, 'B.Cu')

print("P_base initialized, evaluating fixed set...")
from solve_zero_drc_golden import evaluate_all
ov, he, oob, _ = evaluate_all(P_base)
print(f"P_base without East: Overlaps={len(ov)}, Holes={len(he)}, OOB={len(oob)}")
for r1, r2, dx, dy in ov:
    print(f"  OVERLAP: {r1} <--> {r2}: dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in he:
    print(f"  HOLE: {h} <--> {r}: pen={pen:.2f}")
for r, msg in oob:
    print(f"  OOB: {r}: {msg}")
