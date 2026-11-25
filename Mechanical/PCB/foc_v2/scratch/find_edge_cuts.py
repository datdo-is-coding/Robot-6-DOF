with open('scratch/test_edge.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 0
target = '"Edge.Cuts"'
while True:
    pos = text.find(target, pos)
    if pos == -1:
        break
    print(text[max(0, pos-100):min(len(text), pos+150)])
    print('*****************')
    pos += len(target)
