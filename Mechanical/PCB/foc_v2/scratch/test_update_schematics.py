import re

# 1. Update MCU.kicad_sch
with open("MCU.kicad_sch", "r", encoding="utf-8") as f:
    mcu_sch = f.read()

old_j10_fp = "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical"
new_j10_fp = "Connector_JST:JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal"

assert mcu_sch.count(old_j10_fp) == 1, f"Expected 1 occurrence of old J10 fp, found {mcu_sch.count(old_j10_fp)}"
mcu_sch_updated = mcu_sch.replace(old_j10_fp, new_j10_fp)

with open("scratch/MCU_test.kicad_sch", "w", encoding="utf-8") as f:
    f.write(mcu_sch_updated)
print("Updated MCU schematic (test)")

# 2. Update communication.kicad_sch
with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    comm_sch = f.read()

# Let's inspect J8 and J9 in communication.kicad_sch
# We want to change J8 and J9:
# lib_id from "Connector_Generic_MountingPin:Conn_01x03_MountingPin" to "Connector_Generic:Conn_01x03"
# Footprint from "Connector_Molex:Molex_PicoBlade_53261-0371_1x03-1MP_P1.25mm_Horizontal" to "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"
# And remove (pin "MP" ...) from J8 and J9 instances.
# And add Connector_Generic:Conn_01x03 to lib_symbols.
print("Done test prep.")
