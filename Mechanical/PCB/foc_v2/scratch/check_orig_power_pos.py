import re, subprocess

res = subprocess.run(["git", "show", "a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb"], capture_output=True, text=True)
text = res.stdout

for ref in ['J1', 'J2', 'J3', 'C_BUS1', 'C_BUS2', 'C_BUS3', 'C_BULK1', 'C63', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']:
    m = re.search(r'\(footprint [^\n]+\n(?:[^\n]+\n)+?\s+\(property "Reference" "' + ref + r'"(?:[^\n]+\n)+?\)', text)
    if m:
        at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', m.group(0))
        rot = at_m.group(3) if at_m and at_m.group(3) else '0'
        print(f"{ref:8s}: at ({at_m.group(1)}, {at_m.group(2)}, {rot})")
