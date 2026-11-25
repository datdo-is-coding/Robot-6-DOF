import csv
import uuid
import subprocess

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

items_to_add = []

# 1. Add Switch Nodes (SHA, SHB, SHC)
# Phase U
items_to_add.append(f'(segment (start 82.9 76.865) (end 82.9 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SHA") (uuid "{uuid.uuid4()}"))')
items_to_add.append(f'(segment (start 82.9 77.5) (end 86.45 77.5) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHA") (uuid "{uuid.uuid4()}"))')
items_to_add.append(f'(segment (start 84.5 77.5) (end 84.5 71.6) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHA") (uuid "{uuid.uuid4()}"))')
# Phase V
items_to_add.append(f'(segment (start 97.9 76.865) (end 97.9 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SHB") (uuid "{uuid.uuid4()}"))')
items_to_add.append(f'(segment (start 97.9 77.5) (end 101.45 77.5) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHB") (uuid "{uuid.uuid4()}"))')
items_to_add.append(f'(segment (start 99.5 77.5) (end 99.5 70.0) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHB") (uuid "{uuid.uuid4()}"))')
# Phase W
items_to_add.append(f'(segment (start 112.9 76.865) (end 112.9 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SHC") (uuid "{uuid.uuid4()}"))')
items_to_add.append(f'(segment (start 112.9 77.5) (end 116.45 77.5) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHC") (uuid "{uuid.uuid4()}"))')
items_to_add.append(f'(segment (start 114.5 77.5) (end 114.5 71.6) (width 1.2) (layer "F.Cu") (net "/GATE_DRV/SHC") (uuid "{uuid.uuid4()}"))')

# 2. Add 10 VIPPO Vias
with open('VIPPO_REQUIRED.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        x = float(row['x_mm'])
        y = float(row['y_mm'])
        d = float(row['via_diameter_mm'])
        drill = float(row['finished_hole_mm'])
        net = row['net']
        via_str = f'(via (at {x} {y}) (size {d}) (drill {drill}) (layers "F.Cu" "B.Cu") (net "{net}") (uuid "{uuid.uuid4()}"))'
        items_to_add.append(via_str)

added_text = "\n\t" + "\n\t".join(items_to_add) + "\n"
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
    '-o', 'scratch/drc_vippo_phases.json',
    'scratch/foc_v2.kicad_pcb'
], capture_output=True, text=True)

print(res.stdout)
