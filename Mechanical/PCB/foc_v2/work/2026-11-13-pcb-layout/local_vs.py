"""Use the installed KiCad MCP router with bounded planning time per branch."""
import json,signal,time
from pathlib import Path
from kcaa.router.router import RouteRequest,auto_route_pair
from kcaa.tools.pcb_routing_tools import _segment_to_sexp,_arc_to_sexp,_via_to_sexp,_apply_shoved_tracks
from kcaa.utils.pcb_sexp_utils import load_pcb,save_pcb
W=Path(__file__).resolve().parent
def expired(*_):raise TimeoutError('route planning time limit')
signal.signal(signal.SIGALRM,expired)
report=[]
for q in json.loads((W/'vs-mcp.requests.json').read_text())[1:]:
 a=q['arguments'];a.pop('algorithm',None)
 for alg in ['astar','pns']:
  start=time.monotonic();signal.alarm(15)
  try:
   r=auto_route_pair(RouteRequest(**a,algorithm=alg))
   data=load_pcb(a['pcb_path'])
   data.extend(_segment_to_sexp(x) for x in r.segments);data.extend(_arc_to_sexp(x) for x in r.arcs);data.extend(_via_to_sexp(x) for x in r.vias)
   _apply_shoved_tracks(data,r.moved_pairs);save_pcb(a['pcb_path'],data)
   v={'a':a['ref_a']+'.'+a['pad_a'],'b':a['ref_b']+'.'+a['pad_b'],'algorithm':alg,'segments':len(r.segments),'seconds':time.monotonic()-start}
   report.append(v);print(v,flush=True);break
  except Exception as e:
   v={'a':a['ref_a']+'.'+a['pad_a'],'b':a['ref_b']+'.'+a['pad_b'],'algorithm':alg,'error':str(e)[:500]}
   report.append(v);print(v,flush=True)
  finally:signal.alarm(0)
 (W/'local-vs.json').write_text(json.dumps(report,indent=2)+'\n')
