import os

def examine_mod(mod_name):
    path = os.path.join(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty", mod_name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"=== {mod_name} ===")
    lines = content.splitlines()
    for l in lines:
        if "fp_line" in l or "fp_rect" in l or "pad " in l or "model " in l:
            if "Courtyard" in l or "pad " in l or "model " in l:
                print(" ", l.strip())

examine_mod("JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod")
examine_mod("JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod")
