import subprocess

out = subprocess.check_output(['git', 'show', 'a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], text=True, encoding='utf-8')
for i, line in enumerate(out.splitlines()):
    if 'Edge.Cuts' in line:
        print(f"{i}: {line}")
