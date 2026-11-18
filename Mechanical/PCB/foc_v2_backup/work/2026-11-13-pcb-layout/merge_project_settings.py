from pathlib import Path
import json,copy
W=Path(__file__).resolve().parent
ROOT=W.parent.parent
q=W/'candidate/foc_v2.kicad_pro'
candidate=json.loads(q.read_text())
live=json.loads((ROOT/'foc_v2.kicad_pro').read_text())
rules=live['board']['design_settings']['rules']
candidate_rules=candidate['board']['design_settings']['rules']
rules.update(candidate_rules)
classes=live['net_settings']['classes']
for source in candidate['net_settings']['classes']:
    existing=next((a for a in classes if a['name']==source['name']),None)
    if existing is None:classes.append(copy.deepcopy(source));continue
    for field in ['clearance','track_width','via_diameter','via_drill']:existing[field]=source[field]
# Keep the current KiCad display/default settings and all check severities.
assert not live['board']['design_settings']['drc_exclusions']
q.write_text(json.dumps(live,indent=2)+'\n')
print('Merged fabrication rules into current saved KiCad 10 project settings')
