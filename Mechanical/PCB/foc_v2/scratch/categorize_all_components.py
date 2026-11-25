with open("scratch/foc_v2_orig.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_fp = False
curr_ref = ""
curr_val = ""
curr_fp = ""
curr_sheet = ""
curr_pos = None
components = []

for l in lines:
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        curr_fp = l.split('"')[1]
        curr_ref = ""
        curr_val = ""
        curr_sheet = ""
        curr_pos = None
    elif in_fp:
        if '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif '(property "Value" ' in l:
            curr_val = l.split('"')[3]
        elif '(sheetname "' in l:
            curr_sheet = l.split('"')[1]
        elif l.strip().startswith("(at ") and curr_pos is None:
            parts = l.strip().split()
            x = float(parts[1])
            y = float(parts[2].rstrip(')'))
            curr_pos = (x, y)
        elif l.startswith("\t)") or l.startswith(")"):
            components.append({
                "ref": curr_ref,
                "val": curr_val,
                "fp": curr_fp,
                "sheet": curr_sheet,
                "pos": curr_pos
            })
            in_fp = False

print(f"Total components: {len(components)}")

from collections import defaultdict
by_sheet = defaultdict(list)
for c in components:
    by_sheet[c["sheet"]].append(c)

for s, lst in sorted(by_sheet.items()):
    print(f"\n=== Sheet: {s} ({len(lst)} components) ===")
    for c in sorted(lst, key=lambda x: x["ref"]):
        print(f"  {c['ref']:8s} {c['val']:15s} {c['fp']}")
