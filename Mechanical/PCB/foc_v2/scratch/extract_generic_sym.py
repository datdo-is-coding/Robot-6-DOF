p = r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Connector_Generic.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# Extract (symbol "Conn_01x03" ...) up to its matching parenthesis
idx = text.find('(symbol "Conn_01x03"')
paren = 0
end_idx = -1
for i in range(idx, len(text)):
    if text[i] == '(':
        paren += 1
    elif text[i] == ')':
        paren -= 1
        if paren == 0:
            end_idx = i + 1
            break

sym_text = text[idx:end_idx]
print(f"Extracted symbol text, len = {len(sym_text)}")
# In communication.kicad_sch, lib_symbols use full prefix, e.g. "Connector_Generic:Conn_01x03"
# Let's adjust prefix:
sym_text = sym_text.replace('(symbol "Conn_01x03"', '(symbol "Connector_Generic:Conn_01x03"')

with open("scratch/conn_01x03_sym.txt", "w", encoding="utf-8") as f:
    f.write(sym_text)
print("Saved scratch/conn_01x03_sym.txt")
