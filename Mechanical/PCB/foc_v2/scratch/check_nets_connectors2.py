with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

def print_fp_pad_nets(ref_name):
    print(f"=== {ref_name} pads ===")
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
                    for i, l in enumerate(fp_lines):
                        if "(pad " in l:
                            # look for (net ...) in next few lines
                            net_str = ""
                            for k in range(i, min(len(fp_lines), i+6)):
                                if "(net " in fp_lines[k]:
                                    net_str = fp_lines[k].strip()
                                    break
                            print(" ", l.strip(), net_str)
                    return
                in_fp = False

print_fp_pad_nets("J8")
print_fp_pad_nets("J9")
print_fp_pad_nets("J10")
