import os, glob

# Search KiCad footprint libraries for JST XH Horizontal
lib_paths = [
    r"C:\Program Files\KiCad\10.0\share\kicad\footprints",
    r"C:\Program Files\KiCad\9.0\share\kicad\footprints",
    r"C:\Program Files\KiCad\8.0\share\kicad\footprints",
]

found = []
for lp in lib_paths:
    if os.path.exists(lp):
        matches = glob.glob(os.path.join(lp, "Connector_JST.pretty", "*XH*Horizontal*.kicad_mod"))
        found.extend(matches)

print(f"Found {len(found)} JST XH Horizontal footprints:")
for f in found[:5]:
    print(" ", os.path.basename(f))
