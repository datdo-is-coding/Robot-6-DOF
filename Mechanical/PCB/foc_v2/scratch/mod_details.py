import os, re

def get_pads_and_bounds(mod_name):
    path = os.path.join(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty", mod_name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"=== {mod_name} ===")
    pads = re.findall(r'\(pad "([^"]+)" [^\)]*?\(at ([-0-9.]+) ([-0-9.]+)', content)
    for p in pads:
        print(f"  Pad {p[0]} at ({p[1]}, {p[2]})")
    # find courtyard
    cy = re.findall(r'\(fp_line[\s\S]*?\(layer "F.CrtYd"\)', content)
    for c in cy:
        print(" ", c.replace("\n", " ").replace("\t", " "))
    rects = re.findall(r'\(fp_rect[\s\S]*?\(layer "F.CrtYd"\)', content)
    for r in rects:
        print("  Rect:", r.replace("\n", " ").replace("\t", " "))

get_pads_and_bounds("JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod")
get_pads_and_bounds("JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod")
