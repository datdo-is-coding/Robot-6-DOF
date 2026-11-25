import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)

# 1. South Connectors (Flush, Aligned bank at South edge Y = 132.2)
P['J8']  = (74.5, 122.5, 0, 'F.Cu')  # CAN_IN (S3B-XH-A horizontal)
P['J9']  = (86.0, 122.5, 0, 'F.Cu')  # CAN_OUT (S3B-XH-A horizontal)
P['J7']  = (100.0, 128.0, 0, 'F.Cu') # Type-C
P['J10'] = (109.5, 122.5, 0, 'F.Cu') # SWD (S5B-XH-A horizontal)

# 2. Motor wire pads (U, V, W): deep inside North circle
P['J1'] = (88.0, 69.5, 0, 'F.Cu')
P['J2'] = (100.0, 69.0, 0, 'F.Cu')
P['J3'] = (112.0, 69.5, 0, 'F.Cu')

# 3. High-voltage Bus Decoupling Caps (1206 across high-side FETs)
P['C_BUS1'] = (82.5, 70.0, 0, 'F.Cu')
P['C_BUS2'] = (94.0, 70.0, 0, 'F.Cu')
P['C_BUS3'] = (106.0, 70.0, 0, 'F.Cu')

# 4. MOSFETs (6 in a row at Y = 75.8)
P['Q1'] = (83.5, 75.8, 90, 'F.Cu')
P['Q2'] = (90.1, 75.8, 270, 'F.Cu')
P['Q3'] = (96.7, 75.8, 90, 'F.Cu')
P['Q4'] = (103.3, 75.8, 270, 'F.Cu')
P['Q5'] = (109.9, 75.8, 90, 'F.Cu')
P['Q6'] = (116.5, 75.8, 270, 'F.Cu')

# 5. Gate Resistors & Bleeders (paired neatly under FETs)
# Series gate resistors (0603 at Y = 80.6)
P['R1'] = (83.5, 80.6, 0, 'F.Cu')
P['R2'] = (90.1, 80.6, 0, 'F.Cu')
P['R3'] = (96.7, 80.6, 0, 'F.Cu')
P['R4'] = (103.3, 80.6, 0, 'F.Cu')
P['R5'] = (109.9, 80.6, 0, 'F.Cu')
P['R7'] = (116.5, 80.6, 0, 'F.Cu')

# Gate-Source bleeders (0603 at Y = 82.3)
P['R55'] = (83.5, 82.5, 0, 'F.Cu')
P['R56'] = (90.1, 82.5, 0, 'F.Cu')
P['R57'] = (96.7, 82.5, 0, 'F.Cu')
P['R58'] = (103.3, 82.5, 0, 'F.Cu')
P['R59'] = (109.9, 82.5, 0, 'F.Cu')
P['R60'] = (116.5, 82.5, 0, 'F.Cu')

# 6. Bulk Capacitors (10mm radial)
# C_BULK1 on West, C63 on East
# At (75.5, 84.5) and (124.5, 84.5): dist to (100, 100) = sqrt(24.5^2 + 15.5^2) = 28.98 mm <= 29.75 mm!
# Clearance to board edge = 35.0 - (28.98 + 5.25) = 0.77 mm!
P['C_BULK1'] = (75.0, 84.5, 0, 'F.Cu')
P['C63']     = (125.0, 84.5, 0, 'F.Cu')

# 7. Shunt Resistors (2512 at Y = 85.3)
P['R47'] = (93.0, 85.3, 90, 'F.Cu')
P['R48'] = (100.0, 85.3, 90, 'F.Cu')
P['R49'] = (107.0, 85.3, 90, 'F.Cu')

# Net Ties
P['NT1'] = (92.5, 85.3, 90, 'F.Cu')
P['NT2'] = (93.5, 85.3, 90, 'F.Cu')
P['NT3'] = (99.5, 85.3, 90, 'F.Cu')
P['NT4'] = (100.5, 85.3, 90, 'F.Cu')
P['NT5'] = (106.5, 85.3, 90, 'F.Cu')
P['NT6'] = (107.5, 85.3, 90, 'F.Cu')

# 8. DRV8323 Gate Driver IC1
P['IC1'] = (100.0, 93.5, 0, 'F.Cu')

# 9. Buck Converter (neatly placed to the right of IC1)
P['L1']  = (114.0, 91.5, 0, 'F.Cu')
P['D4']  = (114.0, 96.5, 0, 'F.Cu')
P['C16'] = (118.5, 93.0, 90, 'F.Cu')
P['C17'] = (118.5, 96.0, 90, 'F.Cu')
P['R53'] = (118.5, 98.5, 0, 'F.Cu')
P['R54'] = (118.5, 100.5, 0, 'F.Cu')

# 10. East Power Input
P['J11'] = (122.0, 103.5, 270, 'F.Cu') # XT30 facing East
P['F1']  = (124.5, 121.5, 90, 'F.Cu')   # Keystone Fuseholder
P['D6']  = (126.5, 127.5, 0, 'F.Cu')    # TVS Diode

# Test point TP1, TP2, TP3
P['TP1'] = (86.0, 90.0, 0, 'F.Cu')
P['TP2'] = (87.5, 101.5, 0, 'F.Cu')
P['TP3'] = (109.5, 101.5, 0, 'F.Cu')

# Check everything
all_bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = s.parse_shapes(s.fps[ref])
    all_bboxes[ref] = s.get_world_bbox(ref, is_b, shapes, x, y, rot)

def check_box_overlap(b1, b2):
    return (b1['x1'] < b2['x2'] - 0.01 and b1['x2'] > b2['x1'] + 0.01 and
            b1['y1'] < b2['y2'] - 0.01 and b1['y2'] > b2['y1'] + 0.01)

overlaps = []
refs = list(all_bboxes.keys())
for i in range(len(refs)):
    for j in range(i + 1, len(refs)):
        r1, r2 = refs[i], refs[j]
        if (r1, r2) in s.ALLOWED or (r2, r1) in s.ALLOWED: continue
        b1, b2 = all_bboxes[r1], all_bboxes[r2]
        if b1['layer'] != b2['layer']: continue
        if check_box_overlap(b1, b2):
            dx = min(b1['x2'], b2['x2']) - max(b1['x1'], b2['x1'])
            dy = min(b1['y2'], b2['y2']) - max(b1['y1'], b2['y1'])
            overlaps.append((r1, r2, dx, dy))

holes = []
for hname, (hx, hy) in s.HOLES.items():
    for r, b in all_bboxes.items():
        if r in ['H1', 'H2', 'H3', 'H4']: continue
        cx = max(b['x1'], min(hx, b['x2']))
        cy = max(b['y1'], min(hy, b['y2']))
        d = math.hypot(cx - hx, cy - hy)
        if d < s.R_KO:
            holes.append((hname, r, d))

print(f"==========================================")
print(f"TOTAL COMPONENTS: {len(P)} / 124")
print(f"OVERLAPS DETECTED: {len(overlaps)}")
print(f"HOLE COLLISIONS: {len(holes)}")
print(f"==========================================")
for r1, r2, dx, dy in overlaps:
    print(f"  OVERLAP: {r1:8s} <--> {r2:8s} : dx={dx:.2f}, dy={dy:.2f}")
for h, r, d in holes:
    print(f"  HOLE: {h:8s} <--> {r:8s} : dist={d:.2f}")
