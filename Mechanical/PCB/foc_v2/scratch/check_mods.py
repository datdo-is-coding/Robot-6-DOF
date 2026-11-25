import os

p3 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
p5 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod"

with open(p3, "r", encoding="utf-8") as f:
    mod3 = f.read()

with open(p5, "r", encoding="utf-8") as f:
    mod5 = f.read()

print("Mod 3 length:", len(mod3))
print("Mod 5 length:", len(mod5))
