import sys
import os
sys.path.append(os.path.dirname(__file__))

import solve_all_placements
import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pcb_refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', text))
solved_refs = set(solve_all_placements.placements.keys())

print(f"PCB refs count: {len(pcb_refs)}")
print(f"Solved refs count: {len(solved_refs)}")

missing_in_solved = pcb_refs - solved_refs
print(f"Missing in solve_all_placements: {len(missing_in_solved)}")
print(sorted(missing_in_solved))
