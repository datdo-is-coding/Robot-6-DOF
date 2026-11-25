with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

old_fp = "Connector_Molex:Molex_PicoBlade_53261-0371_1x03-1MP_P1.25mm_Horizontal"
new_fp = "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"

assert text.count(old_fp) == 2, f"Expected 2, got {text.count(old_fp)}"
text = text.replace(old_fp, new_fp)

with open("communication.kicad_sch", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated communication.kicad_sch exactly 2 times.")
