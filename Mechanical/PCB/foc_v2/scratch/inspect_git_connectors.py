import subprocess, re

res = subprocess.run(['git', 'show', '51d2e07:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], capture_output=True)
git_text = res.stdout.decode('utf-8', errors='ignore')

for ref in ['J7', 'J8', 'J9', 'J10', 'J11', 'J1', 'J2', 'J3']:
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
        if f'(property "Reference" "{ref}"' in fp_text:
            m_at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', fp_text)
            if m_at:
                x, y = float(m_at.group(1)), float(m_at.group(2))
                rot = float(m_at.group(3)) if m_at.group(3) else 0.0
                print(f"Git {ref:6s}: at ({x:6.2f}, {y:6.2f}) rot={rot:5.1f}")
            break
        pos = end
