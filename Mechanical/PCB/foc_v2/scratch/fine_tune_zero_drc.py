import re, subprocess, json

def set_fp(ref, x, y, rot=None, layer=None):
    with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
        text = f.read()

    # match footprint for ref
    pattern = rf'(\(footprint\s+"[^"]+"\s+(?:\(locked yes\)\s+)?\(layer\s+"[^"]+"\)\s+\(uuid\s+"[^"]+"\)\s+\(at\s+)[0-9.-]+\s+[0-9.-]+(?:\s+[0-9.-]+)?(\).*?\(property\s+"Reference"\s+"{ref}")'
    m = re.search(pattern, text, flags=re.DOTALL)
    if not m:
        # try without locked
        pattern2 = rf'(\(footprint\s+"[^"]+"\s+(?:.*?)\(at\s+)[0-9.-]+\s+[0-9.-]+(?:\s+[0-9.-]+)?(\).*?\(property\s+"Reference"\s+"{ref}")'
        m = re.search(pattern2, text, flags=re.DOTALL)
        if not m:
            print(f"Could not find footprint {ref}")
            return False

    rot_str = f" {rot}" if rot is not None else ""
    new_at = f"{x:.4f} {y:.4f}{rot_str}"
    
    # Also handle layer change if provided
    sub_text = m.group(1)
    if layer:
        sub_text = re.sub(r'\(layer\s+"[^"]+"\)', f'(layer "{layer}")', sub_text)
    
    # replace
    start = m.start()
    end = m.end()
    full_match = text[start:end]
    # replace at
    replaced = re.sub(r'\(at\s+[0-9.-]+\s+[0-9.-]+(?:\s+[0-9.-]+)?\)', f'(at {new_at})', full_match)
    if layer:
        replaced = re.sub(r'\(layer\s+"[^"]+"\)', f'(layer "{layer}")', replaced)
    text = text[:start] + replaced + text[end:]

    with open('foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
        f.write(text)
    return True

def run_drc():
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

print("Initial overlaps:")
for c in run_drc():
    print(" ", [i['description'] for i in c['items']])
