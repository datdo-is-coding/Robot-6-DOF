import pcbnew as p
import math
from pathlib import Path
W=Path(__file__).resolve().parent;OUT=W/'candidate'
b=p.LoadBoard(str(OUT/'foc_v2.kicad_pcb'));mm=p.FromMM
z=p.ZONE(b);z.SetLayer(p.In1_Cu);z.SetNetCode(b.FindNet('GND').GetNetCode());z.SetZoneName('Continuous ground reference');z.SetAssignedPriority(0);z.SetLocalClearance(mm(.2));z.SetMinThickness(mm(.15));z.SetPadConnection(p.ZONE_CONNECTION_FULL)
poly=z.Outline();poly.NewOutline()
for n in range(128):
 a=2*math.pi*n/128;poly.Append(mm(100+34.4*math.cos(a)),mm(100+34.4*math.sin(a)))
b.Add(z);p.SaveBoard(str(OUT/'foc_v2.kicad_pcb'),b)
print('Dedicated In1.Cu ground plane added.')
