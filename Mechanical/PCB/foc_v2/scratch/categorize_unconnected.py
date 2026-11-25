import json
from collections import defaultdict

with open('scratch/drc_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

unconnected = d.get('unconnected_items', [])

categories = defaultdict(list)

for u in unconnected:
    items = u.get('items', [])
    desc_full = " <-> ".join([it.get('description', '') for it in items])
    
    # identify net
    net = "UNKNOWN"
    for it in items:
        d_str = it.get('description', '')
        if '[' in d_str and ']' in d_str:
            net = d_str.split('[')[1].split(']')[0]
            break
            
    if net == 'GND':
        cat = '1. GND'
    elif net in ['VS', 'Net-(D6-A)', 'Net-(F1-Pad2)', 'Net-(C63-Pad1)']:
        cat = '2. Power (VS/DC-link)'
    elif any(s in net for s in ['SHA', 'SHB', 'SHC', '/U', '/V', '/W']):
        cat = '3. Switch Nodes (Phase U/V/W)'
    elif any(s in net for s in ['SPA', 'SPB', 'SPC', 'SNA', 'SNB', 'SNC', 'ISENSE', 'CS_']):
        cat = '4. Shunt & Kelvin Sense'
    elif any(s in net for s in ['GH', 'GL', 'GATE', 'BST', 'VCP', 'CP']):
        cat = '5. Gate Drive'
    elif net in ['+3V3', '+5V', 'VBUS', '/COMMUNICATION/VBUS', '/COMMUNICATION/VBUS_GATE', 'Net-(D4-K)', '/COMMUNICATION/USB_VBUS']:
        cat = '6. Auxiliary Power (+3V3, +5V, VBUS)'
    elif any(s in net for s in ['SPI', 'PWM', 'NRST', 'SWD', 'CAN', 'UART', 'I2C', 'CAL', 'FAULT', 'ENABLE']):
        cat = '7. Control / Logic Signals'
    elif 'MA730' in desc_full or 'U2' in desc_full:
        cat = '8. Angle Sensor (U2)'
    else:
        cat = f'9. Other ({net})'
        
    categories[cat].append((net, desc_full, items))

print("=== UNCONNECTED ITEMS BY CATEGORY ===")
for cat in sorted(categories.keys()):
    print(f"\n{cat}: {len(categories[cat])} items")
    for net, desc, items in categories[cat][:4]:
        print(f"   [{net}] {desc[:100]}...")
