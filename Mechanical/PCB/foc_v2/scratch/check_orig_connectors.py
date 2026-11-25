import subprocess, re

res = subprocess.run(["git", "show", "a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb"], capture_output=True, text=True)
text = res.stdout

parts = text.split('(footprint ')
print("Footprints in a0922b7:", len(parts) - 1)
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m:
        ref = ref_m.group(1)
        if ref.startswith('J') or ref in ['H1', 'H2', 'H3', 'H4']:
            at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', p)
            rot = at_m.group(3) if at_m and at_m.group(3) else '0'
            print(f"{ref:6s}: at ({at_m.group(1)}, {at_m.group(2)}, {rot})")
