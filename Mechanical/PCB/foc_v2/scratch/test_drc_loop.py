import json, subprocess, re

def get_drc_errors():
    res = subprocess.run([
        r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe", "pcb", "drc",
        "--format", "json",
        "--severity-all",
        "-o", "scratch/drc_temp.json",
        "foc_v2.kicad_pcb"
    ], capture_output=True, text=True)
    with open("scratch/drc_temp.json") as f:
        d = json.load(f)
    crtyd = [v for v in d['violations'] if v['type'] == 'courtyards_overlap']
    return crtyd

print("Current courtyard overlaps:", len(get_drc_errors()))
