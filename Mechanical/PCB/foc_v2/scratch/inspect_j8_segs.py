import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = text.split('(footprint ')
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    if ref in ['J8', 'J7', 'J10']:
        print(f"=== {ref} lines ===")
        # match (fp_line (start X Y) (end X Y) ... (layer "..."))
        lines = re.findall(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(layer\s+"([^"]+)"\)', b)
        by_layer = {}
        for x1, y1, x2, y2, l in lines:
            by_layer.setdefault(l, []).append((float(x1), float(y1), float(x2), float(y2)))
        for l, segs in by_layer.items():
            all_x = [s[0] for s in segs] + [s[2] for s in segs]
            all_y = [s[1] for s in segs] + [s[3] for s in segs]
            print(f"  layer {l}: {len(segs)} segments, X in [{min(all_x):.2f}, {max(all_x):.2f}], Y in [{min(all_y):.2f}, {max(all_y):.2f}]")
