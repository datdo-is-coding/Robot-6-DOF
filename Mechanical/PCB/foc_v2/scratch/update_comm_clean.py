# Clean update to communication.kicad_sch
with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    comm = f.read()

# Load conn_01x03 symbol definition
with open("scratch/conn_01x03_sym.txt", "r", encoding="utf-8") as f:
    sym_01x03 = f.read().strip()

# Add to lib_symbols if not already present
if 'symbol "Connector_Generic:Conn_01x03"' not in comm:
    ls_pos = comm.find("(lib_symbols")
    insert_pos = comm.find("\n", ls_pos) + 1
    comm = comm[:insert_pos] + "\t\t" + sym_01x03 + "\n" + comm[insert_pos:]
    print("Inserted Connector_Generic:Conn_01x03 into lib_symbols")

# Update J8:
old_j8_block_start = comm.find('(property "Reference" "J8"')
sym_start_j8 = comm.rfind('(symbol', 0, old_j8_block_start)
paren = 0
sym_end_j8 = -1
for i in range(sym_start_j8, len(comm)):
    if comm[i] == '(':
        paren += 1
    elif comm[i] == ')':
        paren -= 1
        if paren == 0:
            sym_end_j8 = i + 1
            break

j8_block = comm[sym_start_j8:sym_end_j8]
j8_block_new = j8_block.replace('"Connector_Generic_MountingPin:Conn_01x03_MountingPin"', '"Connector_Generic:Conn_01x03"')
j8_block_new = j8_block_new.replace('(property "Value" "Conn_01x03_MountingPin"', '(property "Value" "Conn_01x03"')
j8_block_new = j8_block_new.replace('"Connector_Molex:Molex_PicoBlade_53261-0371_1x03-1MP_P1.25mm_Horizontal"', '"Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"')
mp_pos = j8_block_new.find('(pin "MP"')
if mp_pos != -1:
    p_end = j8_block_new.find(')\n', mp_pos)
    p_end = j8_block_new.find(')\n', p_end + 1) + 2
    j8_block_new = j8_block_new[:mp_pos] + j8_block_new[p_end:]

comm = comm[:sym_start_j8] + j8_block_new + comm[sym_end_j8:]

# Update J9:
old_j9_block_start = comm.find('(property "Reference" "J9"')
sym_start_j9 = comm.rfind('(symbol', 0, old_j9_block_start)
paren = 0
sym_end_j9 = -1
for i in range(sym_start_j9, len(comm)):
    if comm[i] == '(':
        paren += 1
    elif comm[i] == ')':
        paren -= 1
        if paren == 0:
            sym_end_j9 = i + 1
            break

j9_block = comm[sym_start_j9:sym_end_j9]
j9_block_new = j9_block.replace('"Connector_Generic_MountingPin:Conn_01x03_MountingPin"', '"Connector_Generic:Conn_01x03"')
j9_block_new = j9_block_new.replace('(property "Value" "Conn_01x03_MountingPin"', '(property "Value" "Conn_01x03"')
j9_block_new = j9_block_new.replace('"Connector_Molex:Molex_PicoBlade_53261-0371_1x03-1MP_P1.25mm_Horizontal"', '"Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"')
mp_pos = j9_block_new.find('(pin "MP"')
if mp_pos != -1:
    p_end = j9_block_new.find(')\n', mp_pos)
    p_end = j9_block_new.find(')\n', p_end + 1) + 2
    j9_block_new = j9_block_new[:mp_pos] + j9_block_new[p_end:]

comm = comm[:sym_start_j9] + j9_block_new + comm[sym_end_j9:]

with open("communication.kicad_sch", "w", encoding="utf-8") as f:
    f.write(comm)
print("Updated communication.kicad_sch cleanly!")
