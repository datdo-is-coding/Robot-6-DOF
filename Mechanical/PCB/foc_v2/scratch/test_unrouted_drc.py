with open("scratch/refined_step5.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Filter out all (segment ...) and (via ...) blocks
clean_lines = []
in_seg_or_via = False
for l in lines:
    if l.startswith("\t(segment ") or l.startswith("(segment ") or l.startswith("\t(via ") or l.startswith("(via "):
        in_seg_or_via = True
    elif in_seg_or_via:
        if l.startswith("\t)") or l.startswith(")"):
            in_seg_or_via = False
    else:
        clean_lines.append(l)

with open("scratch/unrouted_step5.kicad_pcb", "w", encoding="utf-8") as f:
    f.writelines(clean_lines)

print("Saved scratch/unrouted_step5.kicad_pcb without old tracks/vias.")
