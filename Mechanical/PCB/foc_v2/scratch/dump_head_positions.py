import subprocess, re

res = subprocess.run(["git", "show", "HEAD:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb"], capture_output=True, text=True)
text = res.stdout

parts = text.split('(footprint ')
print(f"Total parts in HEAD: {len(parts) - 1}")
orig_P = {}
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m:
        ref = ref_m.group(1)
        at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', p)
        layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
        layer = layer_m.group(1) if layer_m else 'F.Cu'
        rot = float(at_m.group(3)) if at_m and at_m.group(3) else 0.0
        x = float(at_m.group(1)) if at_m else 0.0
        y = float(at_m.group(2)) if at_m else 0.0
        orig_P[ref] = (x, y, rot, layer)

print("Parsed", len(orig_P), "footprints from HEAD")
for ref in sorted(orig_P.keys()):
    if ref.startswith('Q') or ref.startswith('R4') or ref.startswith('H') or ref.startswith('U'):
        print(f"{ref:6s}: {orig_P[ref]}")
