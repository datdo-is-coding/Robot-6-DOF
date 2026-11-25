with open("scratch/clean_step3.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

components = []
in_fp = False
curr_ref = ""
curr_val = ""
curr_pos = (0, 0, 0)
curr_layer = ""

for l in lines:
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        curr_ref = ""
        curr_val = ""
        curr_pos = (0, 0, 0)
        curr_layer = "F.Cu"
    elif in_fp:
        if l.strip().startswith('(layer "'):
            curr_layer = l.strip().split('"')[1]
        elif l.strip().startswith('(at '):
            if curr_pos == (0, 0, 0):
                parts = l.strip().replace(")", "").split()
                x = float(parts[1])
                y = float(parts[2])
                rot = float(parts[3]) if len(parts) > 3 else 0.0
                curr_pos = (x, y, rot)
        elif '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif '(property "Value" ' in l:
            curr_val = l.split('"')[3]
        elif l.startswith("\t)") or l.startswith(")"):
            components.append((curr_ref, curr_val, curr_pos[0], curr_pos[1], curr_pos[2], curr_layer))
            in_fp = False

print(f"Total components: {len(components)}")
# Sort by Reference
for ref, val, x, y, rot, layer in sorted(components, key=lambda c: c[0]):
    if y > 110:
        print(f"  {ref:8s} ({val:20s}): ({x:6.2f}, {y:6.2f}) rot={rot:3.0f} layer={layer}")
