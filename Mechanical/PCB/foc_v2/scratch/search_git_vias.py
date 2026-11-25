import subprocess

# get all commits
commits = subprocess.check_output(['git', 'log', '--format=%H %s'], text=True).strip().split('\n')
print(f"Total commits in repo: {len(commits)}")

for line in commits:
    h, s = line.split(' ', 1)
    # check if foc_v2.kicad_pcb exists in this commit
    try:
        content = subprocess.check_output(['git', 'show', f'{h}:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], text=True, errors='ignore')
        c = content.count('(via ')
        print(f"Commit {h[:7]} ({s[:40]}): {c} vias")
    except Exception as e:
        # try without path prefix
        try:
            content = subprocess.check_output(['git', 'show', f'{h}:foc_v2.kicad_pcb'], text=True, errors='ignore')
            c = content.count('(via ')
            print(f"Commit {h[:7]} ({s[:40]}): {c} vias")
        except:
            pass
