"""Publish the reviewed files only if the saved project has not changed."""
import hashlib
import json
import os
import shutil
from pathlib import Path

W = Path(__file__).resolve().parent
ROOT = W.parent.parent
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = json.loads((W / 'before-sha256.json').read_text())
for name, expected in before.items():
    assert digest(ROOT / name) == expected, f'Project changed since backup: {name}'
names = [n for n in before if n != 'foc_v2.kicad_pcb'] + ['foc_v2.kicad_sym', 'sym-lib-table']
for name in ['foc_v2.kicad_sym', 'sym-lib-table']:
    assert not (ROOT / name).exists(), f'Unexpected existing file: {name}'
checked = json.loads((W / 'checks.json').read_text())
assert checked['critical_connectivity'] == 'passed'
assert all(n == 0 for n in checked['erc'].values())
validation = json.loads((W / 'cubemx-validation.json').read_text())[0]['result']['structuredContent']
assert validation['valid']
assert digest(W / 'candidate/src.ioc') == validation['source_sha256']
after = {n: digest(W / 'candidate' / n) for n in names}
for name in names:
    temp = ROOT / ('.' + name + '.codex-pending')
    shutil.copy2(W / 'candidate' / name, temp)
    os.replace(temp, ROOT / name)
    assert digest(ROOT / name) == after[name]
assert digest(ROOT / 'foc_v2.kicad_pcb') == before['foc_v2.kicad_pcb']
(W / 'applied-sha256.json').write_text(json.dumps({'before': before, 'after': after, 'pcb_unchanged': True}, indent=2) + '\n')
print(f'Applied {len(names)} files; PCB unchanged; backup: {W / "before"}')
