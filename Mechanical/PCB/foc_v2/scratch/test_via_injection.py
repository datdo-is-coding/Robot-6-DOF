import re
import subprocess

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    cur = f.read()

with open('work/2026-11-13-pcb-layout/before-grid.kicad_pcb', 'r', encoding='utf-8') as f:
    bg = f.read()

# Extract all via blocks from before-grid
via_matches = re.findall(r'\(via\s+\(at\s+[\d\.-]+\s+[\d\.-]+\).*?\(uuid\s+"[^"]+"\)\s*\)', bg, re.DOTALL)
print(f"Total vias to inject: {len(via_matches)}")

vias_block = "\n\t" + "\n\t".join(via_matches) + "\n"

# Insert right before the last closing parenthesis
idx = cur.rfind(')')
test_board = cur[:idx] + vias_block + cur[idx:]

with open('scratch/foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(test_board)

# Run DRC
res = subprocess.run([
    'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe',
    'pcb', 'drc',
    '--refill-zones',
    '--schematic-parity',
    '--format', 'json',
    '-o', 'scratch/drc_via_injection.json',
    'scratch/foc_v2.kicad_pcb'
], capture_output=True, text=True)

print("DRC output:")
print(res.stdout)
