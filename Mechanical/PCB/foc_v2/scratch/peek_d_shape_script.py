with open('scratch/apply_clean_d_shape_pcb.py', 'r') as f:
    text = f.read()

import re
for line in text.splitlines():
    if 'JST_XH' in line or 'Connector' in line or 'replace' in line:
        print(line[:100])
