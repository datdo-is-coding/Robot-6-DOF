# Update communication.kicad_sch
with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    comm = f.read()

# Replace PicoBlade with XH_S3B for J8 and J9
old_fp = 'Connector_Molex:Molex_PicoBlade_53261-0371_1x03-1MP_P1.25mm_Horizontal'
new_fp = 'Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal'

count_comm = comm.count(old_fp)
print(f"Occurrences of PicoBlade in communication.kicad_sch: {count_comm}")
comm_updated = comm.replace(old_fp, new_fp)

with open("communication.kicad_sch", "w", encoding="utf-8") as f:
    f.write(comm_updated)
print("Updated communication.kicad_sch successfully.")

# Update MCU.kicad_sch
with open("MCU.kicad_sch", "r", encoding="utf-8") as f:
    mcu = f.read()

old_mcu_fp = 'Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical'
new_mcu_fp = 'Connector_JST:JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal'

count_mcu = mcu.count(old_mcu_fp)
print(f"Occurrences of PinHeader_1x05 in MCU.kicad_sch: {count_mcu}")
mcu_updated = mcu.replace(old_mcu_fp, new_mcu_fp)

with open("MCU.kicad_sch", "w", encoding="utf-8") as f:
    f.write(mcu_updated)
print("Updated MCU.kicad_sch successfully.")
