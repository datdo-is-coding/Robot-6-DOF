import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    cur = f.read()

with open('work/2026-11-13-pcb-layout/before-grid.kicad_pcb', 'r', encoding='utf-8') as f:
    bg = f.read()

# Extract all via blocks from before-grid.kicad_pcb
# Each via is (via (at x y) ... (net ...) (uuid ...))
via_matches = re.findall(r'\(via\s+\(at\s+[\d\.-]+\s+[\d\.-]+\).*?\(uuid\s+"[^"]+"\)\s*\)', bg, re.DOTALL)
print(f"Extracted {len(via_matches)} vias from before-grid.kicad_pcb")

# Sample first 3 vias
for v in via_matches[:3]:
    print(v)
