with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

# find all footprints with their reference and at
fps = re.findall(r'\(footprint\s+"([^"]+)"[\s\S]*?\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"', text)

# Let's collect them into a dictionary
fp_map = {}
for m in re.finditer(r'\(footprint\s+"([^"]+)"[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"[\s\S]*?\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', text):
    fp_map[m.group(2)] = (m.group(3), m.group(4), m.group(5) or '0', m.group(1))

# Also search where Reference comes before 'at' or after 'at'
# Let's do line by line parse of footprint blocks:
lines = text.splitlines()
in_fp = False
curr_ref = None
curr_at = None
curr_fp = None
results = {}

for l in lines:
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        curr_ref = None
        curr_at = None
        curr_fp = l.split('"')[1]
    elif in_fp:
        if '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif l.strip().startswith("(at ") and curr_at is None:
            parts = l.strip().split()
            x = parts[1]
            y = parts[2].rstrip(')')
            rot = parts[3].rstrip(')') if len(parts) > 3 else '0'
            curr_at = (float(x), float(y), float(rot))
        elif l.startswith("\t)") or l.startswith(")"):
            if curr_ref and curr_at:
                results[curr_ref] = (curr_at, curr_fp)
            in_fp = False

for ref in ["H1", "H2", "H3", "H4", "J1", "J2", "J3", "J7", "J8", "J9", "J10", "J11", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "R47", "R48", "R49", "IC1", "U1", "U2", "U8", "U9", "U10", "F1", "D6"]:
    if ref in results:
        pos, fp = results[ref]
        print(f"{ref:6s}: at ({pos[0]:6.2f}, {pos[1]:6.2f}, rot={pos[2]:5.1f}) - {fp}")
    else:
        print(f"{ref:6s}: NOT FOUND")
