import re

# 1. Update communication.kicad_sch
with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    comm = f.read()

# Replace Conn_01x03_MountingPin with Conn_01x03
comm = comm.replace('Connector:Conn_01x03_MountingPin', 'Connector_Generic:Conn_01x03')
comm = comm.replace('Conn_01x03_MountingPin', 'Conn_01x03')

with open("communication.kicad_sch", "w", encoding="utf-8") as f:
    f.write(comm)
print("Updated communication.kicad_sch")

# 2. Add LCSC Part # to J8 and J9 in foc_v2.kicad_pcb
with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

# In J8 and J9 footprint, add (property "LCSC Part #" "C293630" ...)
lcsc_prop = '''\t\t(property "LCSC Part #" "C293630"
\t\t\t(at 0 0 0)
\t\t\t(layer "F.SilkS")
\t\t\t(hide yes)
\t\t\t(effects (font (size 1 1) (thickness 0.15)))
\t\t)
'''

# Find J8 and J9 footprint blocks and insert lcsc_prop after Reference
for ref in ["J8", "J9"]:
    pat = r'(\(property "Reference" "' + ref + r'"[\s\S]*?\n\t\t\))'
    m = re.search(pat, pcb)
    if m:
        pcb = pcb[:m.end()] + "\n" + lcsc_prop + pcb[m.end():]
        print(f"Added LCSC Part # to {ref}")

with open("foc_v2.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(pcb)
print("Updated foc_v2.kicad_pcb")
