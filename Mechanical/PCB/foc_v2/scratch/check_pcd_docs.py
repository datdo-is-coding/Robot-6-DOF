with open(r"C:\Users\Tuan\.gemini\antigravity-cli\skills\bldc-foc-hardware\references\foc-v2.md", "r", encoding="utf-8") as f:
    text = f.read()

for l in text.splitlines():
    if "PCD" in l or "lỗ" in l or "H1" in l or "gá" in l:
        print(l)
