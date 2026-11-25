with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

def print_fp(ref_name):
    print(f"=== {ref_name} ===")
    in_fp = False
    fp_lines = []
    for line in lines:
        if line.startswith("\t(footprint ") or line.startswith("(footprint "):
            in_fp = True
            fp_lines = [line]
        elif in_fp:
            fp_lines.append(line)
            if line.startswith("\t)") or line.startswith(")"):
                text = "".join(fp_lines)
                if f'(property "Reference" "{ref_name}"' in text:
                    for l in fp_lines:
                        if "at " in l or "layer " in l or "CrtYd" in l or "Reference" in l:
                            print(" ", l.strip())
                    return
                in_fp = False

print_fp("J7")
print_fp("J11")
