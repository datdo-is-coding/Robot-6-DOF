import subprocess, re

res = subprocess.run(["git", "show", "HEAD:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb"], capture_output=True, text=True)
text = res.stdout

parts = text.split('(footprint ')
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m:
        ref = ref_m.group(1)
        if ref in ['L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58', 'J11', 'F1', 'D6']:
            at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', p)
            if at_m:
                rot = at_m.group(3) if at_m.group(3) else '0'
                print(f"{ref:6s}: at ({at_m.group(1)}, {at_m.group(2)}, {rot})")
