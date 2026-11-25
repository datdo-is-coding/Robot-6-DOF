import subprocess

out = subprocess.check_output(['git', 'show', 'a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], text=True, encoding='utf-8')
lines = out.splitlines()
for i in range(32560, min(len(lines), 32620)):
    print(f"{i}: {lines[i]}")
