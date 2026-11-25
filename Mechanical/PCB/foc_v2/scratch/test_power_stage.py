import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

from solve_zero_drc_golden import P, HOLES, ALLOWED, get_custom_bbox, evaluate_all

P_perfect = dict(P)

# Tier 1 & 1.5 & 2 Power Stage:
# J1, J2, J3
P_perfect['J1'] = (85.5, 68.5, 0, 'F.Cu')
P_perfect['J2'] = (100.0, 66.5, 0, 'F.Cu')
P_perfect['J3'] = (114.5, 68.5, 0, 'F.Cu')

# DC Bus Caps
P_perfect['C_BUS1'] = (92.5, 69.0, 0, 'F.Cu')
P_perfect['C_BUS2'] = (107.5, 69.0, 0, 'F.Cu')
P_perfect['C_BUS3'] = (100.0, 71.0, 0, 'F.Cu')

# Gate Resistors
P_perfect['R1'] = (81.85, 72.0, 0, 'F.Cu')
P_perfect['R2'] = (89.10, 72.0, 0, 'F.Cu')
P_perfect['R3'] = (95.50, 72.0, 0, 'F.Cu')
P_perfect['R4'] = (104.50, 72.0, 0, 'F.Cu')
P_perfect['R5'] = (110.90, 72.0, 0, 'F.Cu')
P_perfect['R7'] = (118.15, 72.0, 0, 'F.Cu')

# MOSFETs
P_perfect['Q1'] = (81.85, 76.0, 0, 'F.Cu')
P_perfect['Q2'] = (89.10, 76.0, 0, 'F.Cu')
P_perfect['Q3'] = (96.35, 76.0, 0, 'F.Cu')
P_perfect['Q4'] = (103.65, 76.0, 0, 'F.Cu')
P_perfect['Q5'] = (110.90, 76.0, 0, 'F.Cu')
P_perfect['Q6'] = (118.15, 76.0, 0, 'F.Cu')

# Shunts
P_perfect['R47'] = (91.5, 81.2, 0, 'F.Cu')
P_perfect['R48'] = (100.0, 81.2, 0, 'F.Cu')
P_perfect['R49'] = (108.5, 81.2, 0, 'F.Cu')

P_perfect['NT1'] = (89.5, 81.2, 0, 'F.Cu')
P_perfect['NT2'] = (93.5, 81.2, 0, 'F.Cu')
P_perfect['NT3'] = (98.0, 81.2, 0, 'F.Cu')
P_perfect['NT4'] = (102.0, 81.2, 0, 'F.Cu')
P_perfect['NT5'] = (106.5, 81.2, 0, 'F.Cu')
P_perfect['NT6'] = (110.5, 81.2, 0, 'F.Cu')

# Bulk caps:
P_perfect['C_BULK1'] = (76.0, 86.5, 180, 'F.Cu')
P_perfect['C63']     = (124.0, 86.5, 0, 'F.Cu')

# IC1 at Y = 87.5:
P_perfect['IC1'] = (100.0, 87.5, 0, 'F.Cu')

P_perfect['C1']  = (94.0, 84.5, 0, 'F.Cu')
P_perfect['C2']  = (94.0, 86.2, 0, 'F.Cu')
P_perfect['C3']  = (94.0, 87.9, 0, 'F.Cu')
P_perfect['C12'] = (94.0, 89.7, 0, 'F.Cu')
P_perfect['C13'] = (94.0, 91.5, 0, 'F.Cu')

P_perfect['R6']  = (90.5, 84.5, 0, 'F.Cu')
P_perfect['R8']  = (90.5, 86.2, 0, 'F.Cu')
P_perfect['R9']  = (90.5, 87.9, 0, 'F.Cu')
P_perfect['R10'] = (90.5, 89.7, 0, 'F.Cu')
P_perfect['R50'] = (90.5, 91.5, 0, 'F.Cu')

P_perfect['TP1'] = (88.5, 87.0, 0, 'F.Cu')
P_perfect['R51'] = (87.5, 89.0, 0, 'F.Cu')
P_perfect['R52'] = (87.5, 91.0, 0, 'F.Cu')
P_perfect['TP2'] = (87.5, 93.0, 0, 'F.Cu')

P_perfect['C15'] = (106.0, 84.5, 0, 'F.Cu')
P_perfect['C18'] = (106.0, 86.2, 0, 'F.Cu')
P_perfect['C19'] = (106.0, 87.9, 0, 'F.Cu')
P_perfect['C20'] = (106.0, 89.7, 0, 'F.Cu')
P_perfect['C21'] = (106.0, 91.5, 0, 'F.Cu')

P_perfect['R55'] = (109.5, 84.5, 0, 'F.Cu')
P_perfect['R56'] = (109.5, 86.2, 0, 'F.Cu')
P_perfect['R57'] = (109.5, 87.9, 0, 'F.Cu')
P_perfect['R58'] = (109.5, 89.7, 0, 'F.Cu')
P_perfect['R59'] = (109.5, 91.5, 0, 'F.Cu')
P_perfect['R60'] = (109.5, 93.2, 0, 'F.Cu')
P_perfect['TP3'] = (109.5, 95.2, 0, 'F.Cu')

# MCU U1 at Y = 100.5:
P_perfect['U1'] = (100.0, 100.5, 0, 'F.Cu')

P_perfect['C4']  = (96.5, 93.0, 0, 'F.Cu')
P_perfect['C5']  = (103.5, 93.0, 0, 'F.Cu')

P_perfect['R37'] = (89.0, 95.0, 0, 'F.Cu')
P_perfect['C54'] = (91.5, 95.0, 0, 'F.Cu')
P_perfect['R38'] = (96.5, 94.8, 0, 'F.Cu')
P_perfect['C55'] = (100.0, 94.8, 0, 'F.Cu')
P_perfect['R39'] = (103.5, 94.8, 0, 'F.Cu')
P_perfect['C56'] = (106.5, 94.8, 0, 'F.Cu')
P_perfect['C64'] = (108.5, 93.0, 0, 'F.Cu')

P_perfect['C51'] = (92.5, 97.5, 90, 'F.Cu')
P_perfect['C52'] = (92.5, 100.5, 90, 'F.Cu')
P_perfect['C53'] = (92.5, 103.5, 90, 'F.Cu')

P_perfect['C6']  = (107.5, 97.5, 90, 'F.Cu')
P_perfect['C7']  = (107.5, 100.5, 90, 'F.Cu')
P_perfect['C50'] = (107.5, 103.5, 90, 'F.Cu')

P_perfect['C10'] = (91.0, 106.5, 0, 'F.Cu')
P_perfect['C11'] = (109.0, 106.5, 0, 'F.Cu')

P_perfect['FB1'] = (88.5, 97.5, 0, 'F.Cu')
P_perfect['Y1']  = (85.5, 100.5, 0, 'F.Cu')
P_perfect['C8']  = (82.5, 99.0, 90, 'F.Cu')
P_perfect['C9']  = (82.5, 102.0, 90, 'F.Cu')
P_perfect['R44'] = (85.5, 103.5, 0, 'F.Cu')
P_perfect['R32'] = (88.5, 103.5, 0, 'F.Cu')
P_perfect['R34'] = (88.5, 105.8, 0, 'F.Cu')

P_perfect['D1']  = (75.0, 101.5, 0, 'F.Cu')
P_perfect['R33'] = (78.5, 101.5, 0, 'F.Cu')
P_perfect['D2']  = (75.0, 103.5, 0, 'F.Cu')
P_perfect['R35'] = (78.5, 103.5, 0, 'F.Cu')
P_perfect['D3']  = (75.0, 105.5, 0, 'F.Cu')
P_perfect['R36'] = (78.5, 105.5, 0, 'F.Cu')

P_perfect['U9']  = (76.0, 94.5, 0, 'F.Cu')
P_perfect['JP1'] = (76.0, 98.0, 0, 'F.Cu')
P_perfect['R45'] = (79.0, 98.0, 0, 'F.Cu')
P_perfect['R46'] = (81.5, 98.0, 0, 'F.Cu')
P_perfect['C60'] = (72.0, 91.5, 90, 'F.Cu')
P_perfect['C61'] = (72.0, 94.5, 90, 'F.Cu')
P_perfect['C62'] = (72.0, 97.5, 90, 'F.Cu')

P_perfect['J8']  = (74.0,  110.30, 0, 'F.Cu')
P_perfect['J7']  = (92.25, 115.82, 0, 'F.Cu')
P_perfect['J10'] = (100.25, 110.30, 0, 'F.Cu')
P_perfect['J9']  = (121.0, 110.30, 0, 'F.Cu')

P_perfect['U2']  = (100.0, 100.0, 0, 'B.Cu')
P_perfect['C14'] = (100.0, 103.5, 0, 'B.Cu')
P_perfect['R61'] = (100.0, 96.0, 90, 'B.Cu')

P_perfect['U8']  = (92.25, 107.5, 0, 'B.Cu')
P_perfect['C59'] = (92.25, 110.5, 0, 'B.Cu')
P_perfect['Q7']  = (92.25, 113.5, 0, 'B.Cu')
P_perfect['R40'] = (86.0,  118.0, 0, 'B.Cu')
P_perfect['R41'] = (89.5,  118.0, 0, 'B.Cu')
P_perfect['R42'] = (95.0,  118.0, 0, 'B.Cu')
P_perfect['R43'] = (98.5,  118.0, 0, 'B.Cu')

ov, he, oob, _ = evaluate_all(P_perfect)
print(f"P_perfect (excluding East): Overlaps={len(ov)}, Holes={len(he)}, OOB={len(oob)}")
for r1, r2, dx, dy in ov:
    print(f"  OVERLAP: {r1} <--> {r2}: dx={dx:.2f}, dy={dy:.2f}")
for h, r, pen in he:
    print(f"  HOLE: {h} <--> {r}: pen={pen:.2f}")
for r, msg in oob:
    print(f"  OOB: {r}: {msg}")
