import json,signal,time,contextlib,os,copy,math
from pathlib import Path
import sexpdata as sx
from kcaa.router.router import RouteRequest,auto_route_pair
from kcaa.tools.pcb_routing_tools import _segment_to_sexp,_arc_to_sexp,_via_to_sexp,_apply_shoved_tracks
from kcaa.utils.pcb_sexp_utils import load_pcb,save_pcb
W=Path(__file__).resolve().parent;path=str(W/'candidate/foc_v2.kicad_pcb')
S=sx.Symbol
def sub(n,k):return next((a for a in n if isinstance(a,list) and a and str(a[0])==k),None)
def port(name,endpoint,layer,code):
 x,y=endpoint['pos'];net=endpoint['net']
 return [S('footprint'),'RoutingPort',[S('layer'),layer],[S('at'),x,y],[S('property'),'Reference',name,[S('at'),x,y,0],[S('layer'),'F.Fab'],[S('effects'),[S('font'),[S('size'),1,1]]]],[S('pad'),'1',S('smd'),S('rect'),[S('at'),0,0],[S('size'),.35,.35],[S('layers'),layer],[S('net'),net]]]
def expired(*_):raise TimeoutError('planning limit')
signal.signal(signal.SIGALRM,expired)
report=[];null=open(os.devnull,'w')
for i,pair in enumerate(json.loads((W/'pairs.json').read_text())):
 a,z=pair['a'],pair['b'];net=a['net'];dist=math.dist(a['pos'],z['pos'])
 choices=[(la,lb) for la in a['layers'] for lb in z['layers'] if la in ['F.Cu','In2.Cu','B.Cu'] and lb in ['F.Cu','In2.Cu','B.Cu']]
 def rank(c):
  la,lb=c
  return (0 if la==lb=='B.Cu' else 1 if la==lb=='In2.Cu' else 2 if la!=lb else 3)
 choices.sort(key=rank);done=False
 for la,lb in choices[:5]:
  data=load_pcb(path);nc=0
  plan=[n for n in data if not(isinstance(n,list) and n and str(n[0])=='zone' and sub(n,'keepout') is None)]
  # Virtual endpoints replace same-net pad geometry for this planning call.
  for fp in plan:
   if isinstance(fp,list) and fp and str(fp[0])=='footprint':
    fp[:]=[n for n in fp if not(isinstance(n,list) and n and str(n[0])=='pad' and sub(n,'net') and sub(n,'net')[-1]==net)]
  plan=plan+[port('__A',a,la,nc),port('__B',z,lb,nc)]
  for width in [.2,.15]:
   start=time.monotonic();signal.alarm(10)
   try:
    req=RouteRequest(pcb_path=path,ref_a='__A',pad_a='1',ref_b='__B',pad_b='1',net=net,width=width,algorithm='astar',via_pairs=(('F.Cu','In2.Cu'),('In2.Cu','B.Cu'),('F.Cu','B.Cu')))
    with contextlib.redirect_stdout(null),contextlib.redirect_stderr(null):r=auto_route_pair(req,data=plan)
    out=load_pcb(path);out.extend(_segment_to_sexp(x) for x in r.segments);out.extend(_arc_to_sexp(x) for x in r.arcs);out.extend(_via_to_sexp(x) for x in r.vias);_apply_shoved_tracks(out,r.moved_pairs);save_pcb(path,out)
    report.append({'i':i,'net':net,'ok':True,'layers':[la,lb],'segments':len(r.segments),'seconds':round(time.monotonic()-start,2)})
    print(report[-1],flush=True);done=True;break
   except Exception as e:last=str(e)[:200]
   finally:signal.alarm(0)
  if done:break
 if not done:report.append({'i':i,'net':net,'ok':False,'error':last if choices else 'no layer'});print(report[-1],flush=True)
 (W/'point-routes.json').write_text(json.dumps(report,indent=2)+'\n')
print('Routed',sum(x['ok'] for x in report),'of',len(report),'native unconnected pairs.',flush=True)
