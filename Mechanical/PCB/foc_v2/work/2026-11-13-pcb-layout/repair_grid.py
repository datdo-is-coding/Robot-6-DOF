"""Finish disconnected copper using native pad geometry and through-via clearance."""
from pathlib import Path
import json, math, heapq, time, sys, ctypes, os
import numpy as np
import shapely as sh
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
import pcbnew as p

W = Path(__file__).resolve().parent
path = W/'candidate/foc_v2.kicad_pcb'
b = p.LoadBoard(str(path))
layers = [p.F_Cu, p.In2_Cu, p.B_Cu, p.In1_Cu]
step = float(os.environ.get('FOC_GRID_STEP','.05'))
origin = 65.
n = round(70/step)+1
axis = origin + np.arange(n)*step
xx, yy = np.meshgrid(axis, axis)
edge = (xx-100)**2+(yy-100)**2 > 34.4**2
width = .15
clearance = .15
shapes = [[] for _ in layers]
guides = [[] for _ in layers]
drill_guards=[]
pad_guards=[]
engine=ctypes.CDLL(str(W/'grid_search.so')).search_grid
engine.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_int]
engine.restype=ctypes.c_int

def xy(v): return p.ToMM(v.x), p.ToMM(v.y)
def vec(v): return p.VECTOR2I(p.FromMM(v[0]),p.FromMM(v[1]))
def polygons(s):
    out=[]
    for i in range(s.OutlineCount()):
        c=s.COutline(i)
        poly=Polygon([xy(c.CPoint(j)) for j in range(c.PointCount())])
        if poly.is_valid and not poly.is_empty: out.append(poly)
    return unary_union(out)
def add_shape(g, net, indices):
    if g.is_empty:return
    for i in indices:shapes[i].append((net,g))

for f in b.GetFootprints():
    for a in f.Pads():
        if f.GetReference() in ['IC1','U1','U2'] and a.GetNetname() not in ['', 'GND','VS','+3V3','+5V']:
            x,y=xy(a.GetPosition());cx,cy=xy(f.GetPosition());dx,dy=x-cx,y-cy
            if max(abs(dx),abs(dy))>1.0:
                ux,uy=(math.copysign(1,dx),0) if abs(dx)>abs(dy) else (0,math.copysign(1,dy))
                guide=LineString([(x+ux*.35,y+uy*.35),(x+ux*2,y+uy*2)]).buffer(.01)
                guides[layers.index(f.GetLayer())].append((a.GetNetname(),guide))
        for i,l in enumerate(layers):
            if a.IsOnLayer(l):
                s=p.SHAPE_POLY_SET()
                a.TransformShapeToPolygon(s,l,0,p.FromMM(.003),p.ERROR_OUTSIDE)
                add_shape(polygons(s),a.GetNetname(),[i])
                if a.GetAttribute()==p.PAD_ATTRIB_SMD:pad_guards.append(polygons(s).buffer(.2))
        if a.GetDrillSize().x:
            s=p.SHAPE_POLY_SET()
            a.TransformHoleToPolygon(s,0,p.FromMM(.003),p.ERROR_OUTSIDE)
            # Only NPTH holes block their own net; PTH annular rings are copper.
            net=None if a.GetAttribute()==p.PAD_ATTRIB_NPTH else a.GetNetname()
            add_shape(polygons(s),net,range(4))
            drill_guards.append(polygons(s).buffer(.355))
for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA):
        add_shape(Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2),t.GetNetname(),range(4))
        drill_guards.append(Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetDrill())/2+.355))
    else:
        s=p.SHAPE_POLY_SET()
        t.TransformShapeToPolygon(s,t.GetLayer(),0,p.FromMM(.003),p.ERROR_OUTSIDE)
        add_shape(polygons(s),t.GetNetname(),[layers.index(t.GetLayer())])
for z in b.Zones():
    if not z.GetIsRuleArea():continue
    for i,l in enumerate(layers):
        if z.IsOnLayer(l):add_shape(polygons(z.Outline()),None,[i])

def mask(g):
    out=edge.copy()
    if g.is_empty:return out
    x0,y0,x1,y1=g.bounds
    ix0=max(0,int((x0-origin)/step)-1);ix1=min(n,int((x1-origin)/step)+2)
    iy0=max(0,int((y0-origin)/step)-1);iy1=min(n,int((y1-origin)/step)+2)
    out[iy0:iy1,ix0:ix1] |= sh.intersects_xy(g,xx[iy0:iy1,ix0:ix1],yy[iy0:iy1,ix0:ix1])
    return out

def connect(pair):
    net=pair['a']['net']
    foreign=[unary_union([g for other,g in ls if other!=net]) for ls in shapes]
    terminal_access=unary_union([Point(pair[k]['pos']).buffer(.4) for k in ['a','b']])
    track_geoms=[unary_union([g.buffer(clearance+width/2),unary_union([v for other,v in guides[i] if other!=net]).buffer(clearance+width/2).difference(terminal_access)]) for i,g in enumerate(foreign)]
    blocked=np.array([mask(g) for g in track_geoms])
    via_geom=unary_union([unary_union(foreign).buffer(clearance+.2),*drill_guards,*pad_guards])
    via_block=mask(via_geom)
    via_block |= (xx-100)**2+(yy-100)**2>34.15**2
    ends=[]
    for e in [pair['a'],pair['b']]:
        x,y=e['pos'];ix=round((x-origin)/step);iy=round((y-origin)/step)
        cand=[]
        for i,l in enumerate(layers):
            if b.GetLayerName(l) not in e['layers']:continue
            for dy in range(-2,3):
                for dx in range(-2,3):
                    j,k=ix+dx,iy+dy
                    if not(0<=j<n and 0<=k<n) or blocked[i,k,j]:continue
                    pos=(axis[j],axis[k])
                    if not LineString([(x,y),pos]).intersects(track_geoms[i]):cand.append((math.dist((x,y),pos),i,j,k))
        if not cand:return None,'endpoint blocked'
        cand.sort();ends.append(cand[:8])
    starts=np.array([(i*n+k)*n+j for _,i,j,k in ends[0]],dtype=np.int32)
    targets=np.array([(i*n+k)*n+j for _,i,j,k in ends[1]],dtype=np.int32)
    result=np.empty(n*n*4,dtype=np.int32)
    count=engine(blocked.ctypes.data,via_block.ctypes.data,n,starts.ctypes.data,len(starts),targets.ctypes.data,len(targets),result.ctypes.data,len(result))
    if count<=0:return None,'no grid path'
    route=[]
    for key in result[:count]:
        j=int(key)%n;q=int(key)//n;k=q%n;i=q//n;route.append((i,float(axis[j]),float(axis[k])))
    return route,f'{count} grid points'
    targets=set(targets)
    tx,ty=pair['b']['pos']
    def heuristic(i,j,k):
        dx=abs(axis[j]-tx)/step;dy=abs(axis[k]-ty)/step
        return 10*max(dx,dy)+4.14213562*min(dx,dy)
    parent={};score={};heap=[]
    for d,i,j,k in ends[0]:
        key=(i*n+k)*n+j;score[key]=d/step*10;parent[key]=None
        heapq.heappush(heap,(score[key]+heuristic(i,j,k),score[key],key))
    dirs=[(1,0,10),(-1,0,10),(0,1,10),(0,-1,10),(1,1,14.14213562),(1,-1,14.14213562),(-1,1,14.14213562),(-1,-1,14.14213562)]
    count=0;start=time.monotonic()
    while heap:
        _,cost,key=heapq.heappop(heap)
        if cost!=score.get(key):continue
        if key in targets:
            route=[]
            while key is not None:
                j=key%n;q=key//n;k=q%n;i=q//n;route.append((i,float(axis[j]),float(axis[k])));key=parent[key]
            return route[::-1],f'{count} cells'
        j=key%n;q=key//n;k=q%n;i=q//n
        choices=[]
        for dx,dy,dc in dirs:
            nj,nk=j+dx,k+dy
            if not(0<=nj<n and 0<=nk<n) or blocked[i,nk,nj]:continue
            if dx and dy and (blocked[i,k,nj] or blocked[i,nk,j]):continue
            choices.append(((i*n+nk)*n+nj,dc,i,nj,nk))
        if not via_block[k,j]:
            for ni in range(4):
                if ni!=i:choices.append(((ni*n+k)*n+j,45,ni,j,k))
        for nk,dc,ni,nj,ny in choices:
            new=cost+dc
            if new+1e-8<score.get(nk,float('inf')):
                score[nk]=new;parent[nk]=key
                heapq.heappush(heap,(new+heuristic(ni,nj,ny),new,nk))
        count+=1
        if count>500000 or time.monotonic()-start>30:return None,'search limit'
    return None,'no path'

def commit(route,pair):
    net=pair['a']['net'];code=b.FindNet(net).GetNetCode()
    route=[(route[0][0],*pair['a']['pos']),*route,(route[-1][0],*pair['b']['pos'])]
    simplified=[]
    for pt in route:
        if simplified and pt==simplified[-1]:continue
        if len(simplified)>1 and simplified[-1][0]==pt[0]==simplified[-2][0]:
            a,z=simplified[-2:]
            if abs((z[1]-a[1])*(pt[2]-z[2])-(z[2]-a[2])*(pt[1]-z[1]))<1e-7:
                simplified.pop()
        simplified.append(pt)
    for a,z in zip(simplified,simplified[1:]):
        if a[0]!=z[0]:
            v=p.PCB_VIA(b);v.SetPosition(vec(a[1:]));v.SetWidth(p.FromMM(.4));v.SetDrill(p.FromMM(.2));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(code);b.Add(v)
            add_shape(Point(a[1:]).buffer(.2),net,range(4))
            drill_guards.append(Point(a[1:]).buffer(.455))
        elif math.dist(a[1:],z[1:])>1e-6:
            t=p.PCB_TRACK(b);t.SetStart(vec(a[1:]));t.SetEnd(vec(z[1:]));t.SetWidth(p.FromMM(width));t.SetLayer(layers[a[0]]);t.SetNetCode(code);b.Add(t)
            add_shape(LineString([a[1:],z[1:]]).buffer(width/2),net,[a[0]])
    p.SaveBoard(str(path),b)
    return len(simplified)

if __name__=='__main__':
    pairs=json.loads((W/'pairs.json').read_text());report=[]
    for j,pair in enumerate(pairs):
        if pair['a']['kind']=='ZONE' or pair['b']['kind']=='ZONE':continue
        route,detail=connect(pair)
        result={'index':j,'net':pair['a']['net'],'ok':route is not None,'detail':detail}
        if route:result['vertices']=commit(route,pair)
        print(result,flush=True);report.append(result)
        (W/'grid-results.json').write_text(json.dumps(report,indent=2)+'\n')
