import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse footprints blocks
blocks = re.findall(r'(\(footprint [^)]+?\n(?:\t|\s{2,}).*?\n\t\))', text, re.DOTALL)
print(f"Total block matches: {len(blocks)}")

# Let's see how each footprint is structured
f_cu_refs = []
b_cu_refs = []

for b in blocks:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    layer_m = re.search(r'\(layer "([^"]+)"\)', b)
    fp_m = re.search(r'\(footprint "([^"]+)"', b)
    at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
    val_m = re.search(r'\(property "Value" "([^"]+)"', b)
    
    if ref_m and layer_m:
        ref = ref_m.group(1)
        layer = layer_m.group(1)
        fp = fp_m.group(1) if fp_m else ""
        val = val_m.group(1) if val_m else ""
        x, y = float(at_m.group(1)), float(at_m.group(2))
        rot = float(at_m.group(3)) if at_m.group(3) else 0.0
        
        if layer == 'F.Cu':
            f_cu_refs.append((ref, val, fp, x, y, rot))
        else:
            b_cu_refs.append((ref, val, fp, x, y, rot))

print(f"F.Cu count: {len(f_cu_refs)}")
print(f"B.Cu count: {len(b_cu_refs)}")
print("\nB.Cu components:")
for r in b_cu_refs:
    print(f"  {r[0]} ({r[1]}): {r[2]} at ({r[3]}, {r[4]}) rot={r[5]}")
