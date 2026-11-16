import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
import sexpdata as sx

WORK = Path(__file__).resolve().parent
NETLIST = Path(sys.argv[1]) if len(sys.argv) > 1 else WORK / 'candidate.net.xml'
ERC = Path(sys.argv[2]) if len(sys.argv) > 2 else WORK / 'candidate-erc.json'
SCHEMATICS = Path(sys.argv[3]) if len(sys.argv) > 3 else WORK / 'candidate'

root = ET.parse(NETLIST).getroot()
lookup = {}
for net in root.findall('./nets/net'):
    for node in net.findall('node'):
        if node.get('ref') in {'U1', 'U2', 'IC1', 'U9'}:
            key = node.get('ref'), node.get('pin')
            assert key not in lookup, key
            lookup[key] = (net.get('name'), node.attrib)

connections = {
    'MA730_CS': ('50', 'U2', '5'),
    'MA730_SCK': ('55', 'U2', '12'),
    'MA730_MISO': ('52', 'U2', '7'),
    'MA730_MOSI': ('53', 'U2', '4'),
    'DRV8323_MISO': ('56', 'IC1', '29'),
    'DRV8323_MOSI': ('57', 'IC1', '30'),
    'DRV8323_SCK': ('21', 'IC1', '31'),
    'DRV8323_CS': ('51', 'IC1', '32'),
    'CAN_RX': ('61', 'U9', '4'),
    'CAN_TX': ('62', 'U9', '1'),
    'PWM_A': ('41', 'IC1', '37'),
    'PWM_AN': ('34', 'IC1', '38'),
    'PWM_B': ('42', 'IC1', '39'),
    'PWM_BN': ('35', 'IC1', '40'),
    'PWM_C': ('43', 'IC1', '41'),
    'PWM_CN': ('36', 'IC1', '42'),
    'ISENSE_A': ('11', 'IC1', '25'),
    'ISENSE_B': ('17', 'IC1', '24'),
    'ISENSE_C': ('20', 'IC1', '23'),
    'ENABLE': ('40', 'IC1', '33'),
    'FAULT': ('30', 'IC1', '28'),
}
results = {}
for name, (mcu_pin, reference, pin) in connections.items():
    actual = lookup['U1', mcu_pin][0]
    assert actual == lookup[reference, pin][0], (name, actual, lookup[reference, pin])
    results[name] = {'mcu_pin': mcu_pin, 'destination': f'{reference}.{pin}', 'net': actual}
for pin in ['14', '15', '16', '23', '26', '27', '33', '8', '9', '10', '37', '38', '39', '29']:
    assert 'no_connect' in lookup['U1', pin][1]['pintype'], ('unused MCU pin', pin)
for pin in ['1', '2', '3', '6', '9', '15']:
    assert 'no_connect' in lookup['U2', pin][1]['pintype'], ('unused MA730 pin', pin)


def descendants(value):
    if isinstance(value, list):
        yield value
        for item in value:
            yield from descendants(item)

for filename in ['MCU.kicad_sch', 'hall.kicad_sch', 'foc_v2.kicad_sch']:
    parsed = sx.loads((SCHEMATICS / filename).read_text())
    for node in descendants(parsed):
        if not node or str(node[0]) not in {'hierarchical_label', 'label', 'global_label', 'pin'} or len(node) < 2:
            continue
        name = str(node[1])
        assert not name.startswith(('ENCD1_', 'ENCD2_', 'PWM2_', 'ISENSE2_')), (filename, name)
        assert name not in {'EN_GATE2', 'NFAULT2', 'SPI1_SS1', 'HALL_SSCK', 'HALL_SSD'}, (filename, name)


def violations(path):
    report = json.loads(path.read_text())
    return [v for sheet in report['sheets'] for v in sheet['violations']]


def error_key(v):
    return v['type'], tuple(sorted(i['uuid'] for i in v.get('items', [])))

before = violations(WORK / 'saved-before-erc.json')
after = violations(ERC)
old_errors = {error_key(v) for v in before if v['severity'] == 'error'}
new_errors = [v for v in after if v['severity'] == 'error' and error_key(v) not in old_errors]
assert not new_errors, new_errors
summary = {
    'checked_connections': results,
    'unused_mcu_pins_checked': 14,
    'unused_ma730_pins_checked': 6,
    'obsolete_signals_removed': True,
    'erc_before': dict(Counter(v['severity'] for v in before)),
    'erc_after': dict(Counter(v['severity'] for v in after)),
    'new_erc_errors': new_errors,
    'remaining_erc_errors': [v for v in after if v['severity'] == 'error'],
}
(WORK / 'verification.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k not in {'checked_connections', 'remaining_erc_errors'}}, indent=2))
