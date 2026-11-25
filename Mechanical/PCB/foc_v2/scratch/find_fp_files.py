import os, glob

candidates = [
    r"C:\Program Files\KiCad\10.0\share\kicad\footprints",
    r"C:\Program Files\KiCad\9.0\share\kicad\footprints",
    r"C:\Program Files\KiCad\8.0\share\kicad\footprints",
    r"C:\Program Files\KiCad\share\kicad\footprints"
]
for p in candidates:
    if os.path.exists(p):
        print("Found:", p)
        matches = glob.glob(os.path.join(p, "Connector_JST.pretty", "*XH*Horizontal*"))
        for m in matches:
            if "3" in m or "5" in m or "2" in m:
                print("  ", os.path.basename(m))
