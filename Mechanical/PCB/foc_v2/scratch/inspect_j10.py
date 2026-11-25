with open('MCU.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('"J10"')
print('Index:', idx)
if idx != -1:
    print(text[max(0, idx-500):idx+500])
