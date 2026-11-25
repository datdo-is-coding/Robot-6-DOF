p3 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
with open(p3, "r", encoding="utf-8") as f:
    text = f.read()

import re
pads = re.findall(r'\(pad [^\)]+\)', text)
for p in pads:
    print(p)
