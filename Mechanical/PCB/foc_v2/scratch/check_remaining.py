from layout_optimizer import pos, local_boxes

all_refs = set(local_boxes.keys())
placed_refs = set(pos.keys())
remaining = sorted(list(all_refs - placed_refs))
print(f"Remaining components to place: {len(remaining)}")
print("Remaining:", remaining)
