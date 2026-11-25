import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

# find all segments
segments = re.findall(r'\(segment\s+\(start\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(end\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(width\s+([\d\.-]+)\)\s+\(layer\s+"([^"]+)"\)\s+\(net\s+"([^"]+)"\)\s+\(uuid\s+"([^"]+)"\)\s*\)', content)

print(f"Total track segments: {len(segments)}")

power_nets = ['VS', '/GATE_DRV/SHA', '/GATE_DRV/SHB', '/GATE_DRV/SHC', '/GATE_DRV/SPA', '/GATE_DRV/SPB', '/GATE_DRV/SPC', 'Net-(Q1-G)', 'Net-(Q2-G)', 'Net-(Q3-G)', 'Net-(Q4-G)', 'Net-(Q5-G)', 'Net-(Q6-G)']

by_net = {}
for s in segments:
    net = s[6]
    if net in power_nets:
        if net not in by_net:
            by_net[net] = []
        by_net[net].append(s)

for net in power_nets:
    segs = by_net.get(net, [])
    print(f"\nNet {net}: {len(segs)} segments")
    for s in segs[:5]:
        print(f"   ({s[0]}, {s[1]}) -> ({s[2]}, {s[3]}) w={s[4]} layer={s[5]}")
