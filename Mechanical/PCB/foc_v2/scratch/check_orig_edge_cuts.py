import re

git_content = open('foc_v2.kicad_pcb', 'r', encoding='utf-8').read()

# Let's check git show a0922b7 for original edge cuts
import subprocess
try:
    res = subprocess.run(["git", "show", "a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb"], capture_output=True, text=True)
    orig_text = res.stdout
    print("Found original PCB in commit a0922b7, length:", len(orig_text))
    # Extract Edge.Cuts
    blocks = re.findall(r'\(gr_(?:line|arc|circle)[\s\S]*?\n\s+\(layer\s+\"Edge\.Cuts\"\)[\s\S]*?\)', orig_text)
    for b in blocks:
        print(b.strip())
except Exception as e:
    print(e)
