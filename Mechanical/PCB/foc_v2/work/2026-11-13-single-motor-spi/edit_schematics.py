import hashlib
import json
import re
import uuid
from pathlib import Path
import sexpdata as sx

WORK = Path(__file__).resolve().parent
SOURCE = WORK.parent.parent
STAGE = WORK / 'candidate'


def nodes(text):
    result = []
    depth = 0
    quoted = escaped = False
    start = None
    for i, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == '(':
            if depth == 1:
                start = i
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 1 and start is not None:
                block = text[start:i + 1]
                result.append((start, i + 1, sx.loads(block), block))
                start = None
    assert depth == 0 and not quoted
    return result


def child(node, key):
    found = [n for n in node if isinstance(n, list) and n and str(n[0]) == key]
    assert len(found) == 1, (key, found)
    return found[0]


def point(node, key='at'):
    return tuple(float(v) for v in child(node, key)[1:3])


def number(value):
    return f'{value:.4f}'.rstrip('0').rstrip('.')


def uid():
    return str(uuid.uuid4())


def nc(x, y):
    return f'(no_connect (at {number(x)} {number(y)}) (uuid "{uid()}"))'


def patch_child(filename, remove_names, rename):
    text = (WORK / 'saved-before' / filename).read_text()
    parsed = nodes(text)
    wires = [n for n in parsed if str(n[2][0]) == 'wire']
    removals = set()
    changes = []
    additions = []
    removed = []
    for start, end, node, block in parsed:
        if str(node[0]) != 'hierarchical_label':
            continue
        name = node[1]
        if name in rename:
            new_name, shape = rename[name]
            replacement = block.replace('"' + name + '"', '"' + new_name + '"', 1)
            replacement, count = re.subn(r'\(shape \w+\)', '(shape ' + shape + ')', replacement, count=1)
            assert count == 1
            changes.append((start, end, replacement))
        elif name in remove_names:
            xy = point(node)
            connected = []
            for wire in wires:
                ends = [tuple(float(v) for v in p[1:3]) for p in child(wire[2], 'pts')[1:]]
                if xy in ends:
                    connected.append((wire, ends))
            assert len(connected) == 1, (filename, name, connected)
            wire, ends = connected[0]
            far_end = ends[1] if ends[0] == xy else ends[0]
            assert abs(far_end[0] - xy[0]) > 0.01
            removals.add((wire[0], wire[1]))
            changes.append((start, end, ''))
            additions.append(nc(*far_end))
            removed.append({'label': name, 'unused_pin_at': far_end})
    for start, end in removals:
        changes.append((start, end, ''))
    assert len(removed) == len(remove_names)
    for start, end, replacement in sorted(changes, reverse=True):
        text = text[:start] + replacement + text[end:]
    text = text.rstrip()
    assert text.endswith(')')
    text = text[:-1] + '\n\t' + '\n\t'.join(additions) + '\n)\n'
    sx.loads(text)
    (STAGE / filename).write_text(text)
    return removed


def make_root():
    text = (WORK / 'saved-before/foc_v2.kicad_sch').read_text()
    parsed = nodes(text)
    old_sheets = {}
    for _, _, node, block in parsed:
        if str(node[0]) == 'sheet':
            props = {x[1]: x[2] for x in node if isinstance(x, list) and str(x[0]) == 'property'}
            old_sheets[props['Sheetname']] = (node, block, props['Sheetfile'])
    keep = [block for _, _, node, block in parsed if str(node[0]) not in {'sheet', 'wire', 'no_connect', 'junction', 'label', 'text'}]
    pin_positions = {}

    def sheet(name, x, y, width, height, pins):
        old, block, filename = old_sheets[name]
        sheet_id = child(old, 'uuid')[1]
        instance = next(raw for _, _, n, raw in nodes(block) if str(n[0]) == 'instances')
        old_pins = {p[1]: child(p, 'uuid')[1] for p in old if isinstance(p, list) and str(p[0]) == 'pin'}
        file_x = x + width + 5.08 if name == 'COMMUNICATION' else x
        file_y = y + 2.54 if name == 'COMMUNICATION' else y + height + 1.27
        parts = [f'(sheet (at {number(x)} {number(y)}) (size {number(width)} {number(height)})',
                 '(exclude_from_sim no) (in_bom yes) (on_board yes)',
                 '(stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0))',
                 f'(uuid "{sheet_id}")',
                 f'(property "Sheetname" "{name}" (at {number(x)} {number(y - 1.27)} 0) (effects (font (size 1.27 1.27)) (justify left bottom)))',
                 f'(property "Sheetfile" "{filename}" (at {number(file_x)} {number(file_y)} 0) (effects (font (size 1.27 1.27)) (justify left top)))']
        for pin, kind, edge, position in pins:
            if edge == 'left':
                px, py, angle, justify = x, position, 180, 'left'
            elif edge == 'right':
                px, py, angle, justify = x + width, position, 0, 'right'
            elif edge == 'top':
                px, py, angle, justify = position, y, 90, 'right'
            else:
                px, py, angle, justify = position, y + height, 270, 'left'
            pin_positions[name, pin] = (px, py)
            pin_id = old_pins.get(pin, uid())
            parts.append(f'(pin "{pin}" {kind} (at {number(px)} {number(py)} {angle}) (uuid "{pin_id}") (effects (font (size 1.27 1.27)) (justify {justify})))')
        parts.extend([instance, ')'])
        return '\n'.join(parts)

    gate_names = [('EN_GATE1', 'input', 73.66), ('NFAULT1', 'output', 76.2),
                  ('PWM1_A', 'input', 78.74), ('PWM1_AN', 'input', 81.28),
                  ('PWM1_B', 'input', 83.82), ('PWM1_BN', 'input', 86.36),
                  ('PWM1_C', 'input', 88.9), ('PWM1_CN', 'input', 91.44),
                  ('SPI1_MOSI', 'input', 99.06), ('SPI1_MISO', 'output', 101.6),
                  ('SPI1_SCK', 'input', 104.14), ('SPI1_SS0', 'input', 106.68),
                  ('ISENSE1_A', 'output', 114.3), ('ISENSE1_B', 'output', 116.84),
                  ('ISENSE1_C', 'output', 119.38)]
    mcu_pins = [(n, 'output' if kind == 'input' else 'input', 'right', y) for n, kind, y in gate_names]
    hall_pairs = [('HALL_CS', 'HALL_CS', 'input', 73.66),
                  ('SPI3_SCK', 'HALL_SCLK', 'input', 76.2),
                  ('SPI3_MOSI', 'HALL_MOSI', 'input', 78.74),
                  ('SPI3_MISO', 'HALL_MISO', 'output', 81.28)]
    mcu_pins += [(mcu, 'output' if kind == 'input' else 'input', 'left', y) for mcu, _, kind, y in hall_pairs]
    spare = [('IO_PB2', 'bidirectional', 96.52), ('IO_PC4', 'bidirectional', 99.06),
             ('IO_PC5', 'bidirectional', 101.6), ('IO_PC15', 'bidirectional', 104.14),
             ('IO_PD2', 'bidirectional', 106.68), ('PV_SENSE', 'input', 114.3),
             ('UART1_TX', 'output', 121.92), ('UART1_RX', 'input', 124.46)]
    mcu_pins += [(n, kind, 'left', y) for n, kind, y in spare]
    comm = [('USB_N', 'USB_N', 'bidirectional', 'bidirectional', 118.11),
            ('USB_P', 'USB_P', 'bidirectional', 'bidirectional', 129.54),
            ('CAN1_RX', 'CAN_RX', 'input', 'output', 140.97),
            ('CAN1_TX', 'CAN_TX', 'output', 'input', 152.4)]
    mcu_pins += [(mcu, mkind, 'top', x) for mcu, _, mkind, _, x in comm]
    additions = [
        sheet('MCU', 110.49, 60.96, 48.26, 71.12, mcu_pins),
        sheet('GATE_DRV', 187.96, 66.04, 48.26, 58.42, [(n, kind, 'left', y) for n, kind, y in gate_names]),
        sheet('HALL', 40.64, 68.58, 40.64, 25.4, [(hall, kind, 'right', y) for _, hall, kind, y in hall_pairs]),
        sheet('COMMUNICATION', 110.49, 25.4, 48.26, 25.4, [(name, ckind, 'bottom', x) for _, name, _, ckind, x in comm]),
    ]

    def wire(a, b):
        assert a[0] == b[0] or a[1] == b[1], (a, b)
        return f'(wire (pts (xy {number(a[0])} {number(a[1])}) (xy {number(b[0])} {number(b[1])})) (stroke (width 0) (type default)) (uuid "{uid()}"))'

    for name, _, _ in gate_names:
        additions.append(wire(pin_positions['MCU', name], pin_positions['GATE_DRV', name]))
    for mcu, hall, _, _ in hall_pairs:
        additions.append(wire(pin_positions['MCU', mcu], pin_positions['HALL', hall]))
    for mcu, comm_pin, _, _, _ in comm:
        additions.append(wire(pin_positions['MCU', mcu], pin_positions['COMMUNICATION', comm_pin]))
    for name, _, _ in spare:
        if name != 'PV_SENSE':
            additions.append(nc(*pin_positions['MCU', name]))
    for label, x, y in [('MA730: SPI3 / 5.25 MHz', 40.64, 100.33),
                        ('Mode 3 / 16-bit / CS active low', 40.64, 104.14),
                        ('DRV8323: SPI1 / 5.25 MHz', 187.96, 132.08)]:
        additions.append(f'(text "{label}" (at {number(x)} {number(y)} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{uid()}"))')
    output = '(kicad_sch\n\t' + '\n\t'.join(keep + additions) + '\n)\n'
    sx.loads(output)
    (STAGE / 'foc_v2.kicad_sch').write_text(output)


def main():
    checked = json.loads((WORK / 'cubemx-stage-init.json').read_text())[-1]['result']['structuredContent']
    assert checked['cubemx_validated'] and checked['changed'], checked
    assert checked['applied_sha256'] == hashlib.sha256((STAGE / 'src.ioc').read_bytes()).hexdigest()
    obsolete = {'ENCD2_A', 'ENCD2_B', 'ENCD2_I', 'ISENSE2_A', 'ISENSE2_B', 'ISENSE2_C',
                'PWM2_A', 'PWM2_AN', 'PWM2_B', 'PWM2_BN', 'PWM2_C', 'PWM2_CN', 'EN_GATE2', 'ENCD1_I'}
    changed = patch_child('MCU.kicad_sch', obsolete, {
        'ENCD1_A': ('HALL_CS', 'output'), 'ENCD1_B': ('SPI3_SCK', 'output'),
        'SPI1_SS1': ('SPI3_MISO', 'input'), 'NFAULT2': ('SPI3_MOSI', 'output')})
    patch_child('hall.kicad_sch', {'HALL_SSCK', 'HALL_SSD'}, {})
    for filename in ['gatedrv.kicad_sch', 'communication.kicad_sch', 'foc_v2.kicad_pro']:
        (STAGE / filename).write_bytes((WORK / 'saved-before' / filename).read_bytes())
    make_root()
    (WORK / 'removed-mcu-signals.json').write_text(json.dumps(changed, indent=2) + '\n')
    for filename in ['MCU.kicad_sch', 'hall.kicad_sch', 'foc_v2.kicad_sch']:
        sx.loads((STAGE / filename).read_text())
    print('Candidate schematics created after successful CubeMX validation')

if __name__ == '__main__':
    main()
