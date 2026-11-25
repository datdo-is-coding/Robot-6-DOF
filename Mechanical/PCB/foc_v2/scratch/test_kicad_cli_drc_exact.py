import math, re, uuid, subprocess, json

# Let's test different layout configurations and run kicad-cli DRC on each!
# We want:
# 1. invalid_outline == 0
# 2. courtyards_overlap == 0
# 3. zero out-of-board components

# Let's read the base PCB
with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see what happens if we place all 124 components according to P_golden
# and test with kicad-cli!
