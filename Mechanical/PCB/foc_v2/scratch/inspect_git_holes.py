import subprocess, re, math

res = subprocess.run(['git', 'show', '51d2e07:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], capture_output=True)
git_text = res.stdout.decode('utf-8', errors='ignore')

for h in ['H1', 'H2', 'H3', 'H4']:
    pos = 0
    while True:
        idx = git_text.find('(footprint ', pos)
        if idx == -1: break
        depth = 0
        end = idx
        for i in range(idx, len(git_text)):
            if git_text[i] == '(': depth += 1
            elif git_text[i] == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        fp_text = git_text[idx:end]
        if f'(property "Reference" "{h}"' in fp_text:
            m_at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', fp_text)
            if m_at:
                x, y = float(m_at.group(1)), float(m_at.group(2))
                r = ((x-100)**2 + (y-100)**2)**0.5
                angle = 180 * math.atan2(y-100, x-100) / math.pi
                print(f"Git {h}: at ({x:.2f}, {y:.2f}) -> r={r:.2f} (PCD={2*r:.2f}), angle={angle:.1f} deg")
            break
        pos = end
