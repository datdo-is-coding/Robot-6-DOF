import re, subprocess

res = subprocess.run(["git", "show", "HEAD:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb"], capture_output=True, text=True)
text = res.stdout

for ref in ['L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58', 'J11', 'F1', 'D6']:
    pos_m = re.search(r'\(property "Reference" "' + ref + r'"[\s\S]*?\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)', text)
    if not pos_m:
        # Search footprint header
        pos_m = re.search(r'\(footprint [^\n]+\n\s+\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)[\s\S]*?\(property "Reference" "' + ref + r'"', text)
    if pos_m:
        rot = pos_m.group(3) if pos_m.group(3) else '0'
        print(f"{ref:6s}: at ({pos_m.group(1)}, {pos_m.group(2)}, {rot})")
    else:
        print(f"{ref:6s}: NOT FOUND")
