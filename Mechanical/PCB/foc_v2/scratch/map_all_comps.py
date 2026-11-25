import json

# Let's inspect all 124 components in foc_v2_orig.kicad_pcb
with open("scratch/foc_v2_orig.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Collect footprints and their nets
lines = text.splitlines()
in_fp = False
curr_ref = ""
curr_fp = ""
curr_sheet = ""
pad_nets = {}
all_comps = {}

for l in lines:
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        curr_fp = l.split('"')[1]
        curr_ref = ""
        curr_sheet = ""
        pad_nets = {}
    elif in_fp:
        if '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif '(sheetname "' in l:
            curr_sheet = l.split('"')[1]
        elif '(pad "' in l and '(net "' in l:
            # single line pad with net
            p_m = re.search(r'\(pad\s+"([^"]+)"', l)
            n_m = re.search(r'\(net\s+"([^"]+)"', l)
            if p_m and n_m:
                pad_nets[p_m.group(1)] = n_m.group(1)
        elif l.strip().startswith('(net "'):
            # multi-line pad net
            n_m = re.search(r'\(net\s+"([^"]+)"', l)
            # associate with last pad if known
        elif l.startswith("\t)") or l.startswith(")"):
            if curr_ref:
                all_comps[curr_ref] = {
                    "fp": curr_fp,
                    "sheet": curr_sheet
                }
            in_fp = False

print(f"Total components found: {len(all_comps)}")
for ref, d in sorted(all_comps.items()):
    print(f"{ref:8s}: sheet={d['sheet']:15s} fp={d['fp']}")
