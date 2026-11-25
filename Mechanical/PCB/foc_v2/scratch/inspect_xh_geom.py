p = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
for l in lines:
    if "fp_line" in l or "fp_rect" in l or "pad" in l:
        print(l)
