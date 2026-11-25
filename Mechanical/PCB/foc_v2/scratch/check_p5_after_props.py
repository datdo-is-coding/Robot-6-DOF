p5 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod"
with open(p5, "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(30, 65):
    print(f"Line {j+1}: {repr(lines[j])}")
