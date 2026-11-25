import math, json
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
print(f"Loaded {len(fps)} footprints.")

# Let's inspect all 124 footprint refs
all_refs = sorted(list(fps.keys()))
print("All refs:", all_refs)
