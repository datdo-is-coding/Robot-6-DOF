import re

content = open('foc_v2.kicad_pcb', 'r', encoding='utf-8').read()
for line in content.splitlines():
    if 'Edge.Cuts' in line:
        print(line)
