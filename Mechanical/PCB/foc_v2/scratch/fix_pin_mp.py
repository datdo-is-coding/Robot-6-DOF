import re

# 1. Update communication.kicad_sch: remove pin MP and fix symbol name
with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    comm = f.read()

# Change symbol library name to Connector_Generic:Conn_01x03
comm = comm.replace('Connector_Generic_MountingPin:Conn_01x03', 'Connector_Generic:Conn_01x03')

# Remove pin MP from symbol Conn_01x03_1_1
pin_mp_pattern = r'\t\t\t\t\(pin passive line\n\t\t\t\t\t\(at 0 -7\.62 90\)[\s\S]*?\(number "MP"[\s\S]*?\n\t\t\t\t\)\n'
comm = re.sub(pin_mp_pattern, '', comm)

# Remove the polyline and text "Mounting"
comm = re.sub(r'\t\t\t\t\(polyline\n\t\t\t\t\t\(pts\n\t\t\t\t\t\t\(xy -1\.016 -4\.572\) \(xy 1\.016 -4\.572\)\n\t\t\t\t\t\)[\s\S]*?\t\t\t\t\)\n', '', comm)
comm = re.sub(r'\t\t\t\t\(text "Mounting"[\s\S]*?\t\t\t\t\)\n', '', comm)

with open("communication.kicad_sch", "w", encoding="utf-8") as f:
    f.write(comm)
print("Updated communication.kicad_sch")

# 2. Update foc_v2.kicad_pcb:
with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

# Ensure Value is "Conn_01x03" for J8 and J9
pcb = pcb.replace('(property "Value" "Conn_01x03_MountingPin"', '(property "Value" "Conn_01x03"')

with open("foc_v2.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(pcb)
print("Updated foc_v2.kicad_pcb")
