with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_fp = False
curr_ref = ""
curr_fp = ""
curr_pos = None

for l in lines:
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        curr_fp = l.split('"')[1]
        curr_ref = ""
        curr_pos = None
    elif in_fp:
        if '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif l.strip().startswith("(at ") and curr_pos is None:
            parts = l.strip().split()
            x = float(parts[1])
            y = float(parts[2].rstrip(')'))
            curr_pos = (x, y)
        elif l.startswith("\t)") or l.startswith(")"):
            if curr_pos and curr_pos[1] < 75:
                print(f"{curr_ref:8s} at {curr_pos} - {curr_fp}")
            in_fp = False
