with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("--- NET TABLE ---")
for l in lines:
    if l.strip().startswith("(net "):
        parts = l.strip().split()
        if len(parts) >= 3:
            net_id = parts[1]
            net_name = parts[2].strip('"')
            if any(k in net_name for k in ["CAN", "SWD", "NRST", "+3V3", "GND", "VS", "24V"]):
                print(f"Net {net_id}: {net_name}")
