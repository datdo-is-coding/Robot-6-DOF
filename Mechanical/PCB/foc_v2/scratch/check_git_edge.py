import subprocess
import re

out = subprocess.check_output(['git', 'show', 'a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], text=True, encoding='utf-8')

for m in re.finditer(r'\(gr_(?:line|arc|circle) .*?layer "Edge\.Cuts".*?\)', out, re.DOTALL):
    print(m.group(0))
