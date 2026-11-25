import re, subprocess, json

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

with open('scratch/test_outline.sexpr', 'r') as f:
    edge_cuts = f.read()

# Replace Edge.Cuts in text
# First remove any existing Edge.Cuts elements:
cleaned_lines = []
skip = False
in_edge = False
for line in text.split('\n'):
    if '(layer "Edge.Cuts")' in line:
        in_edge = True
        continue
    cleaned_lines.append(line)

new_text = '\n'.join(cleaned_lines)
# Remove the old gr_arc/gr_line that had Edge.Cuts
# We can regex remove any (gr_arc ... (layer "Edge.Cuts") ...) and (gr_line ... (layer "Edge.Cuts") ...)
new_text = re.sub(r'\(gr_(?:arc|line|circle|rect)[\s\S]*?\(layer\s+"Edge\.Cuts"\)[\s\S]*?\n\t\)', '', text)
# Insert the clean edge_cuts right before the last closing paren
idx = new_text.rfind(')')
test_pcb = new_text[:idx] + edge_cuts + new_text[idx:]

with open('scratch/test_edge_drc.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(test_pcb)

# Run DRC
cmd = [
    r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe',
    'pcb', 'drc', '--format', 'json',
    '-o', 'scratch/test_edge_drc.json',
    'scratch/test_edge_drc.kicad_pcb'
]
res = subprocess.run(cmd, capture_output=True, text=True)
with open('scratch/test_edge_drc.json', 'r', encoding='utf-8') as f:
    drc = json.load(f)

outline_errs = [v for v in drc.get('violations', []) if v.get('type') == 'invalid_outline']
print("invalid_outline count:", len(outline_errs))
for v in outline_errs:
    print(v)
