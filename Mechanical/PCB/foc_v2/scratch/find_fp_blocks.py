with open("scratch/pcb_step2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Collect footprint blocks: (start_line, end_line, ref)
fp_blocks = []
in_fp = False
start_idx = -1
curr_ref = None

for i, l in enumerate(lines):
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        start_idx = i
        curr_ref = None
    elif in_fp:
        if '(property "Reference" ' in l:
            ref = l.split('"')[3]
            curr_ref = ref
        elif l.startswith("\t)") or l.startswith(")"):
            fp_blocks.append((start_idx, i, curr_ref))
            in_fp = False

print(f"Total footprint blocks found: {len(fp_blocks)}")
for start, end, ref in fp_blocks:
    if ref in ["J8", "J9", "J10", "J7", "J11"]:
        print(f"Ref {ref}: lines {start+1} to {end+1}")
