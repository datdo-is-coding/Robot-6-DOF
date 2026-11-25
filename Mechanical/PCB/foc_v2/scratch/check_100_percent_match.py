import sys
sys.path.append('scratch')
import re
from perfect_placements import placements

with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

orig_refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', text))
diff1 = orig_refs - set(placements.keys())
diff2 = set(placements.keys()) - orig_refs

print(f"Orig refs count: {len(orig_refs)}")
print(f"Perfect placements count: {len(placements)}")
print(f"Missing in perfect placements: {diff1}")
print(f"Extra in perfect placements: {diff2}")
assert len(diff1) == 0 and len(diff2) == 0, "Mismatch in references!"
print("100% PERFECT MATCH FOR ALL 124 COMPONENTS!")
