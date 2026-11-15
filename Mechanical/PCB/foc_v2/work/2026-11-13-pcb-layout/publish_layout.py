from pathlib import Path
import json,hashlib,shutil,os,tempfile
import pcbnew as p
W=Path(__file__).resolve().parent;ROOT=W.parent.parent;C=W/'candidate'
checks=json.loads((W/'final-checks.json').read_text())
for name,digest in checks['candidate_sha256'].items():assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,name
baseline=json.loads((W/'before-sha256.json').read_text())
for name,digest in baseline.items():
    if name not in ['foc_v2.kicad_pcb','foc_v2.kicad_pro']:assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('Concurrent change',name)
live=json.loads((W/'live-board-pro-sha256.json').read_text())
for name,digest in live.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('Concurrent change',name)
old=p.LoadBoard(str(ROOT/'foc_v2.kicad_pcb'))
assert not list(old.GetFootprints()) and not list(old.GetTracks()) and not list(old.GetDrawings()) and not list(old.Zones()),'Current PCB has new user geometry'
backup=W/'publish-backup';backup.mkdir(exist_ok=True)
def write(target,data):
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        saved=backup/target.relative_to(ROOT);saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
    fd,tmp=tempfile.mkstemp(prefix='.'+target.name+'.',dir=target.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data)
        os.replace(tmp,target)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
changed=[]
for name in checks['candidate_sha256']:
    if name=='src.ioc':continue
    source=C/name;target=ROOT/name
    if target.exists() and target.read_bytes()==source.read_bytes():continue
    if name.startswith('foc_v2.pretty/') or name=='fp-lib-table':assert not target.exists(),('New library path already exists',name)
    write(target,source.read_bytes());changed.append(name)
for name in ['VIPPO_REQUIRED.csv','FABRICATION_NOTES.md']:
    write(ROOT/name,(W/name).read_bytes());changed.append(name)
(W/'published-files.json').write_text(json.dumps(changed,indent=2)+'\n');print('Published:',', '.join(changed))
