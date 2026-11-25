from search_horizontal_bank import valid_configs

for cfg in valid_configs:
    y_front, x_center, perm, placed = cfg
    print(f"=== Y_front: {y_front}, X_center: {x_center}, Order: {perm} ===")
    for c_name in perm:
        xmin, xmax, ymin, ymax = placed[c_name]
        print(f"  {c_name}: X [{xmin:.2f}, {xmax:.2f}], Y [{ymin:.2f}, {ymax:.2f}]")
