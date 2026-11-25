import re, math

# Let's read the official JST XH mod files
p3 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
p5 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod"

with open(p3, "r", encoding="utf-8") as f:
    mod3_raw = f.read()

with open(p5, "r", encoding="utf-8") as f:
    mod5_raw = f.read()

# Let's inspect how mod3 starts and ends
print("Mod 3 first 200 chars:")
print(mod3_raw[:200])
print("\nMod 3 last 100 chars:")
print(mod3_raw[-100:])
