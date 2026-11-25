with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_fp = False
curr_ref = ""
curr_val = ""
curr_fp = ""
curr_pos = ""
all_components = []

for l in lines:
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        curr_fp = l.split('"')[1]
        curr_ref = ""
        curr_val = ""
        curr_pos = ""
    elif in_fp:
        if '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif '(property "Value" ' in l:
            curr_val = l.split('"')[3]
        elif l.strip().startswith("(at ") and curr_pos == "":
            curr_pos = l.strip()
        elif l.startswith("\t)") or l.startswith(")"):
            all_components.append((curr_ref, curr_val, curr_pos, curr_fp))
            in_fp = False

print(f"Total components: {len(all_components)}")
for ref, val, pos, fp in sorted(all_components, key=lambda x: x[0]):
    print(f"{ref:8s} {val:15s} {pos:25s} {fp}")
