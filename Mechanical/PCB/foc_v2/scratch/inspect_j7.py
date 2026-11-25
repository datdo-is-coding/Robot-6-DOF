import re

with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# find all (footprint ... with (property "Reference" "REF")
fps = re.findall(r'\(footprint\s+"([^"]+)"[\s\S]+?\(property "Reference"\s+"([^"]+)"[\s\S]+?\(at\s+([-0-9.]+)\s+([-0-9.]+)(?:\s+([-0-9.]+))?\)', text)
print(f"Found {len(fps)} footprints with pattern 1")

# Alternatively line-by-line:
lines = text.splitlines()
in_fp = False
curr_fp = {}
fp_list = []
for l in lines:
    if l.startswith('\t(footprint ') or l.startswith('(footprint '):
        in_fp = True
        curr_fp = {'line': l}
    elif in_fp:
        if '(property "Reference"' in l:
            curr_fp['ref'] = l.split('"')[3]
        elif '(at ' in l and 'pos' not in curr_fp:
            parts = l.strip().strip('()').split()
            curr_fp['pos'] = parts[1:]
        elif l.startswith('\t)') or l == ')':
            fp_list.append(curr_fp)
            in_fp = False

print(f"Found {len(fp_list)} footprints line-by-line")
for item in fp_list:
    if item.get('ref') in ['J1', 'J2', 'J3', 'H1', 'H2', 'H3', 'H4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'J7', 'J8', 'J9', 'J10', 'J11']:
        print(f"  {item.get('ref')}: {item.get('pos')}")
