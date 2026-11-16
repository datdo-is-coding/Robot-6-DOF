import json, subprocess, sys
from pathlib import Path
import sexpdata as sx
W=Path(__file__).resolve().parent
q=W/'candidate/foc_v2.kicad_pcb'
report=W/'pruned-drc.json'
def sub(n,k):return next((a for a in n if isinstance(a,list) and a and str(a[0])==k),None)
for j in range(120):
    fill=j%10==0
    subprocess.run(['kicad-cli','pcb','drc','--format','json',*(['--refill-zones','--save-board'] if fill else []),'-o',str(report),str(q)],check=True,stdout=subprocess.DEVNULL)
    r=json.loads(report.read_text())
    drop={i['uuid'] for v in r['violations'] if v['type'] in ['track_dangling','via_dangling'] for i in v['items']}
    if not drop:
        if not fill:
            subprocess.run(['kicad-cli','pcb','drc','--format','json','--refill-zones','--save-board','-o',str(report),str(q)],check=True,stdout=subprocess.DEVNULL)
            r=json.loads(report.read_text());drop={i['uuid'] for v in r['violations'] if v['type'] in ['track_dangling','via_dangling'] for i in v['items']}
        if not drop:break
    data=sx.loads(q.read_text());removed=[]
    for a in data:
        if not(isinstance(a,list) and a and str(a[0]) in ['segment','via'] and sub(a,'uuid') and sub(a,'uuid')[1] in drop):continue
        if str(a[0])=='segment' and sub(a,'width')[1]>=.8:continue
        removed.append(a)
    if not removed:break
    data[:]=[a for a in data if a not in removed];q.write_text(sx.dumps(data)+'\n')
    print('Pruned',len(removed),'unused copper stubs',flush=True)
print('Remaining unconnected:',len(r['unconnected_items']),flush=True)
