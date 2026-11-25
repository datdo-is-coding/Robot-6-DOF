import re
import uuid
import subprocess

with open('scratch/foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

vs_items = []

# 1. 24V_IN before fuse: from J11 pad 1 at (112.50, 116.50)
# Go south to y=119.0 to clear J11 pad 2 at (117.50, 116.50), then east to x=127.0, then north into F1 pad 1 at (127.0, 107.0)
vs_items.append(f'(segment (start 112.50 116.50) (end 112.50 119.00) (width 2.0) (layer "B.Cu") (net "Net-(J11-Pin_1)") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 112.50 119.00) (end 128.50 119.00) (width 2.0) (layer "B.Cu") (net "Net-(J11-Pin_1)") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 128.50 119.00) (end 128.50 107.00) (width 2.0) (layer "B.Cu") (net "Net-(J11-Pin_1)") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 128.50 107.00) (end 127.00 107.00) (width 2.0) (layer "B.Cu") (net "Net-(J11-Pin_1)") (uuid "{uuid.uuid4()}"))')

# 2. F1 pad 2 (VS at 127.00, 116.92 and 123.60, 116.92) to D6 pad 1 (VS at 119.05, 111.60)
# Route from (123.60, 116.92) west to x=119.05, then north to (119.05, 111.60) (entering D6 pad 1 on the left, clearing pad 2 at 123.35!)
vs_items.append(f'(segment (start 127.00 116.92) (end 123.60 116.92) (width 1.5) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 123.60 116.92) (end 119.05 116.92) (width 1.5) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 119.05 116.92) (end 119.05 111.60) (width 1.5) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')

# 3. Connect F1 pad 2 / D6 to C63 pad 1 (VS at 126.80, 89.50)
# From (119.05, 111.60) north to y=89.50, then east to C63 pad 1 at (126.80, 89.50) (clearing F1 pad 1 at 127.0, 107.0 by > 7 mm!)
vs_items.append(f'(segment (start 119.05 111.60) (end 119.05 89.50) (width 1.5) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 119.05 89.50) (end 126.80 89.50) (width 1.5) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')

# 4. Connect C_BUS1 pad 1 (76.525, 94.00) to C_BULK1 pad 1 (74.00, 88.00)
vs_items.append(f'(segment (start 76.525 94.00) (end 74.00 91.475) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 74.00 91.475) (end 74.00 88.00) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')

# From C_BULK1 pad 1 (74.00, 88.00) to Q1 pad 5 (78.95, 77.50):
# Route west to x=71.0, north to y=77.50, then east to Q1 pad 5 at (78.95, 77.50) (clearing C_BULK1 pad 2 GND at 74.0, 83.0 by 3.0 mm!)
vs_items.append(f'(segment (start 74.00 88.00) (end 71.00 88.00) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 71.00 88.00) (end 71.00 77.50) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 71.00 77.50) (end 78.95 77.50) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')

# 5. Connect C_BUS2 pad 1 (91.025, 72.00) to Q3 pad 5 (93.95, 77.50)
vs_items.append(f'(segment (start 91.025 72.00) (end 93.95 74.925) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 93.95 74.925) (end 93.95 77.50) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')

# 6. Connect C_BUS3 pad 1 (106.025, 72.00) to Q5 pad 5 (108.95, 77.50)
vs_items.append(f'(segment (start 106.025 72.00) (end 108.95 74.925) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(segment (start 108.95 74.925) (end 108.95 77.50) (width 1.2) (layer "F.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')

# 7. Add Power Vias (0.8mm size, 0.4mm drill) connecting F.Cu to In2.Cu
vs_items.append(f'(via (at 77.50 77.50) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(via (at 93.95 77.50) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')
vs_items.append(f'(via (at 108.95 77.50) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net "VS") (uuid "{uuid.uuid4()}"))')

added_text = "\n\t" + "\n\t".join(vs_items) + "\n"
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
    '-o', 'scratch/drc_vs_routing_clean.json',
    'scratch/foc_v2.kicad_pcb'
], capture_output=True, text=True)

print(res.stdout)
