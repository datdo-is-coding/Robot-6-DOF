import re
with open('foc_v2.kicad_pcb', 'r') as f:
    text = f.read()

b = text.split('(footprint "foc_v2:AMASS_XT30PW-M_Edge_NoSilk"')[1].split('(property "Reference" "J11"')[0]
model_m = re.search(r'\(model\s+"[^"]+"[\s\S]*?\)', text.split('(property "Reference" "J11"')[0].split('(footprint "foc_v2:AMASS_XT30PW-M_Edge_NoSilk"')[-1])
if model_m:
    print(model_m.group(0))
