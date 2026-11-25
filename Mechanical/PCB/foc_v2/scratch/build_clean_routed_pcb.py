import uuid
import csv
import subprocess

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

items = []

# =========================================================================
# 1. SWITCH NODES (Phase U, V, W): SHA, SHB, SHC
# =========================================================================
# Phase U (SHA)
items.append(f'(segment (start 82.9 76.865) (end 82.9 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SHA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 82.9 77.5) (end 86.45 77.5) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 84.5 77.5) (end 84.5 71.6) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHA") (uuid "{uuid.uuid4()}"))')

# Phase V (SHB)
items.append(f'(segment (start 97.9 76.865) (end 97.9 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SHB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 97.9 77.5) (end 101.45 77.5) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 99.5 77.5) (end 99.5 70.0) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHB") (uuid "{uuid.uuid4()}"))')

# Phase W (SHC)
items.append(f'(segment (start 112.9 76.865) (end 112.9 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SHC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 112.9 77.5) (end 116.45 77.5) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 114.5 77.5) (end 114.5 71.6) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHC") (uuid "{uuid.uuid4()}"))')

# =========================================================================
# 2. VIPPO VIAS (10 specified in VIPPO_REQUIRED.csv)
# =========================================================================
with open('VIPPO_REQUIRED.csv', 'r') as f_csv:
    reader = csv.DictReader(f_csv)
    for row in reader:
        x = float(row['x_mm'])
        y = float(row['y_mm'])
        d = float(row['via_diameter_mm'])
        drill = float(row['finished_hole_mm'])
        net = row['net']
        items.append(f'(via (at {x} {y}) (size {d}) (drill {drill}) (layers "F.Cu" "B.Cu") (net "{net}") (uuid "{uuid.uuid4()}"))')

# =========================================================================
# 3. SHUNT CONNECTIONS (Phase U, V, W): SPA, SPB, SPC
# =========================================================================
# Phase U (SPA)
items.append(f'(segment (start 90.4 76.865) (end 90.4 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 90.4 79.405) (end 90.4 80.30) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 90.4 80.30) (end 83.50 80.30) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 83.50 80.30) (end 83.50 84.80) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 83.50 84.80) (end 83.537 84.80) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 86.325 80.30) (end 86.325 81.80) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 83.50 84.80) (end 83.50 88.65) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 83.50 88.65) (end 84.50 88.65) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 84.50 88.65) (end 85.725 88.65) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 85.725 88.65) (end 85.725 88.00) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')

# Phase V (SPB)
items.append(f'(segment (start 105.4 76.865) (end 105.4 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 105.4 79.405) (end 105.4 80.30) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 105.4 80.30) (end 98.50 80.30) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 98.50 80.30) (end 98.50 84.80) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 98.50 84.80) (end 99.537 84.80) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 101.325 80.30) (end 101.325 81.80) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 98.50 84.80) (end 98.50 88.30) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 98.50 88.30) (end 100.50 88.30) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 100.50 88.30) (end 101.725 88.30) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 101.725 88.30) (end 101.725 87.55) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')

# Phase W (SPC)
items.append(f'(segment (start 120.4 76.865) (end 120.4 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 120.4 79.405) (end 120.4 80.30) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 120.4 80.30) (end 113.50 80.30) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 113.50 80.30) (end 113.50 84.80) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 113.50 84.80) (end 114.537 84.80) (width 0.5) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 116.325 80.30) (end 116.325 81.80) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 113.50 84.80) (end 113.50 88.65) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 113.50 88.65) (end 115.50 88.65) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 115.50 88.65) (end 116.725 88.65) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 116.725 88.65) (end 116.725 88.00) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')

# =========================================================================
# 4. MOSFET GATE CONNECTIONS (R1..R7 to Q1..Q6)
# =========================================================================
# Q1 Gate: R1 pad 2 at (82.325, 73.00) -> Q1 pad 4 at (82.90, 75.595)
items.append(f'(segment (start 82.325 73.00) (end 82.90 73.575) (width 0.25) (layer "F.Cu") (net "Net-(Q1-G)") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 82.90 73.575) (end 82.90 75.595) (width 0.25) (layer "F.Cu") (net "Net-(Q1-G)") (uuid "{uuid.uuid4()}"))')

# Q2 Gate: R2 pad 2 at (88.825, 73.00) -> Q2 pad 4 at (90.40, 75.595)
items.append(f'(segment (start 88.825 73.00) (end 90.40 74.575) (width 0.25) (layer "F.Cu") (net "Net-(Q2-G)") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 90.40 74.575) (end 90.40 75.595) (width 0.25) (layer "F.Cu") (net "Net-(Q2-G)") (uuid "{uuid.uuid4()}"))')

# Q3 Gate: R3 pad 2 at (97.325, 72.80) -> Q3 pad 4 at (97.90, 75.595)
items.append(f'(segment (start 97.325 72.80) (end 97.90 73.375) (width 0.25) (layer "F.Cu") (net "Net-(Q3-G)") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 97.90 73.375) (end 97.90 75.595) (width 0.25) (layer "F.Cu") (net "Net-(Q3-G)") (uuid "{uuid.uuid4()}"))')

# Q4 Gate: R4 pad 2 at (103.325, 72.80) -> Q4 pad 4 at (105.40, 75.595)
items.append(f'(segment (start 103.325 72.80) (end 105.40 74.875) (width 0.25) (layer "F.Cu") (net "Net-(Q4-G)") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 105.40 74.875) (end 105.40 75.595) (width 0.25) (layer "F.Cu") (net "Net-(Q4-G)") (uuid "{uuid.uuid4()}"))')

# Q5 Gate: R5 pad 2 at (112.325, 73.00) -> Q5 pad 4 at (112.90, 75.595)
items.append(f'(segment (start 112.325 73.00) (end 112.90 73.575) (width 0.25) (layer "F.Cu") (net "Net-(Q5-G)") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 112.90 73.575) (end 112.90 75.595) (width 0.25) (layer "F.Cu") (net "Net-(Q5-G)") (uuid "{uuid.uuid4()}"))')

# Q6 Gate: R7 pad 2 at (118.825, 73.00) -> Q6 pad 4 at (120.40, 75.595)
items.append(f'(segment (start 118.825 73.00) (end 120.40 74.575) (width 0.25) (layer "F.Cu") (net "Net-(Q6-G)") (uuid "{uuid.uuid4()}"))')
items.append(f'(segment (start 120.40 74.575) (end 120.40 75.595) (width 0.25) (layer "F.Cu") (net "Net-(Q6-G)") (uuid "{uuid.uuid4()}"))')

# Write clean scratch board
added_text = "\n\t" + "\n\t".join(items) + "\n"
idx = content.rfind(')')
test_board = content[:idx] + added_text + content[idx:]

with open('scratch/foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(test_board)

res = subprocess.run([
    'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe',
    'pcb', 'drc',
    '--refill-zones',
    '--schematic-parity',
    '--format', 'json',
    '-o', 'scratch/drc_gates_and_shunts.json',
    'scratch/foc_v2.kicad_pcb'
], capture_output=True, text=True)

print("DRC Result:")
print(res.stdout)
