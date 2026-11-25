import subprocess
res = subprocess.run(['git', 'show', '51d2e07:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], capture_output=True)
text = res.stdout.decode('utf-8', errors='ignore')
pos = text.find('91badb81-7d1e-4643-8684-96ad252ea949')
print("Position in git file:", pos, "out of", len(text))
print(text[max(0, pos-400):min(len(text), pos+400)])
