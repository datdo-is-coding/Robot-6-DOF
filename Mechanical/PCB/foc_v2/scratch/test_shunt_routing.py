import uuid
import subprocess

with open('scratch/foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

segs = []

# --- Phase U Shunt SPA ---
# 1. Q2 source bar connecting pads 1, 2, 3
segs.append(f'(segment (start 90.4 76.865) (end 90.4 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
# 2. From Q2 source down to y=80.30
segs.append(f'(segment (start 90.4 79.405) (end 90.4 80.30) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
# 3. Across corridor at y=80.30 to x=83.537 (dead center between R55 at 82.325 and R56 at 84.675!)
segs.append(f'(segment (start 90.4 80.30) (end 83.537 80.30) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
# 4. Down at x=83.537 into R47 pad 1 at (83.537, 84.80)
segs.append(f'(segment (start 83.537 80.30) (end 83.537 84.80) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
# 5. Connect R47 pad 1 to C1 pad 1 at (85.725, 88.00):
segs.append(f'(segment (start 83.537 84.80) (end 83.537 86.50) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 83.537 86.50) (end 85.725 86.50) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 85.725 86.50) (end 85.725 88.00) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
# 6. From C1 pad 1 (85.725, 88.00) down to y=88.65, then across to NT1 pad 2 at (84.50, 88.65)
segs.append(f'(segment (start 85.725 88.00) (end 85.725 88.65) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 85.725 88.65) (end 84.50 88.65) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')
# 7. Connect R56 pad 2 at (86.325, 81.80) up to corridor at y=80.30
segs.append(f'(segment (start 86.325 80.30) (end 86.325 81.80) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPA") (uuid "{uuid.uuid4()}"))')

# --- Phase V Shunt SPB ---
# 1. Q4 source bar connecting pads 1, 2, 3
segs.append(f'(segment (start 105.4 76.865) (end 105.4 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
# 2. From Q4 source down to y=80.30
segs.append(f'(segment (start 105.4 79.405) (end 105.4 80.30) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
# 3. Across corridor at y=80.30 to x=98.50 (dead center between R57 at 97.325 and R58 at 99.675!)
segs.append(f'(segment (start 105.4 80.30) (end 98.50 80.30) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
# 4. Down at x=98.50 to y=84.80, then into R48 pad 1 at (99.537, 84.80)
segs.append(f'(segment (start 98.50 80.30) (end 98.50 84.80) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 98.50 84.80) (end 99.537 84.80) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
# 5. Connect R48 pad 1 to C2 pad 1 at (101.725, 87.55):
segs.append(f'(segment (start 99.537 84.80) (end 99.537 86.50) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 99.537 86.50) (end 101.725 86.50) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 101.725 86.50) (end 101.725 87.55) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
# 6. From C2 pad 1 at (101.725, 87.55) to y=88.30, across to NT3 pad 2 at (100.50, 88.30)
segs.append(f'(segment (start 101.725 87.55) (end 101.725 88.30) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 101.725 88.30) (end 100.50 88.30) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')
# 7. Connect R58 pad 2 at (101.325, 81.80) up to corridor at y=80.30
segs.append(f'(segment (start 101.325 80.30) (end 101.325 81.80) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPB") (uuid "{uuid.uuid4()}"))')

# --- Phase W Shunt SPC ---
# 1. Q6 source bar connecting pads 1, 2, 3
segs.append(f'(segment (start 120.4 76.865) (end 120.4 79.405) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
# 2. From Q6 source down to y=80.30
segs.append(f'(segment (start 120.4 79.405) (end 120.4 80.30) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
# 3. Across corridor at y=80.30 to x=113.50 (dead center between R59 at 112.325 and R60 at 114.675!)
segs.append(f'(segment (start 120.4 80.30) (end 113.50 80.30) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
# 4. Down at x=113.50 to y=84.80, then into R49 pad 1 at (114.537, 84.80)
segs.append(f'(segment (start 113.50 80.30) (end 113.50 84.80) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 113.50 84.80) (end 114.537 84.80) (width 0.6) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
# 5. Connect R49 pad 1 to C3 pad 1 at (116.725, 88.00):
segs.append(f'(segment (start 114.537 84.80) (end 114.537 86.50) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 114.537 86.50) (end 116.725 86.50) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 116.725 86.50) (end 116.725 88.00) (width 0.4) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
# 6. From C3 pad 1 (116.725, 88.00) down to y=88.65, across to NT5 pad 2 at (115.50, 88.65)
segs.append(f'(segment (start 116.725 88.00) (end 116.725 88.65) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
segs.append(f'(segment (start 116.725 88.65) (end 115.50 88.65) (width 0.25) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')
# 7. Connect R60 pad 2 at (116.325, 81.80) up to corridor at y=80.30
segs.append(f'(segment (start 116.325 80.30) (end 116.325 81.80) (width 0.3) (layer "F.Cu") (net "/GATE_DRV/SPC") (uuid "{uuid.uuid4()}"))')

added_text = "\n\t" + "\n\t".join(segs) + "\n"
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
    '-o', 'scratch/drc_shunt_routing_perfect.json',
    'scratch/foc_v2.kicad_pcb'
], capture_output=True, text=True)

print(res.stdout)
