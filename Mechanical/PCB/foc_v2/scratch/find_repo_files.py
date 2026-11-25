import os, glob

base_dir = r"C:\Users\Tuan\Robot-6-DOF"
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith((".step", ".stp", ".sldprt", ".dxf", ".pdf", ".md", ".txt")):
            full = os.path.join(root, f)
            print(os.path.relpath(full, base_dir))
