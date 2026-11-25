with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Edge.Cuts' in l and i > 50:
        start = i
        while start > 0 and not lines[start].strip().startswith('(gr_'):
            start -= 1
        end = i
        paren_depth = 0
        for k in range(start, len(lines)):
            paren_depth += lines[k].count('(') - lines[k].count(')')
            if paren_depth == 0:
                end = k
                break
        print(''.join(lines[start:end+1]))
        print('=============================')
