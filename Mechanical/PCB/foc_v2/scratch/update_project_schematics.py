import os, sys

# 1. Update MCU.kicad_sch
with open("MCU.kicad_sch", "r", encoding="utf-8") as f:
    mcu = f.read()

old_fp_j10 = "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical"
new_fp_j10 = "Connector_JST:JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal"

assert mcu.count(old_fp_j10) == 1
mcu = mcu.replace(old_fp_j10, new_fp_j10)

with open("MCU.kicad_sch", "w", encoding="utf-8") as f:
    f.write(mcu)
print("Updated MCU.kicad_sch (J10 footprint -> JST XH 5-pin horizontal)")

# 2. Update communication.kicad_sch
with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    comm = f.read()

# Load conn_01x03 symbol definition
with open("scratch/conn_01x03_sym.txt", "r", encoding="utf-8") as f:
    sym_01x03 = f.read().strip()

# Add to lib_symbols if not already present
if 'symbol "Connector_Generic:Conn_01x03"' not in comm:
    # insert before the closing paren of lib_symbols
    # find (lib_symbols ...
    ls_pos = comm.find("(lib_symbols")
    # find where lib_symbols ends
    # We can insert right after (lib_symbols\n
    insert_pos = comm.find("\n", ls_pos) + 1
    comm = comm[:insert_pos] + "\t\t" + sym_01x03 + "\n" + comm[insert_pos:]
    print("Inserted Connector_Generic:Conn_01x03 into lib_symbols")

# Update J8 and J9 symbol references, values, footprints, and remove pin MP
# For J8:
old_j8_block_start = comm.find('(property "Reference" "J8"')
# Find surrounding symbol block
sym_start_j8 = comm.rfind('(symbol', 0, old_j8_block_start)
# find end of symbol block
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
# Replace in j8_block:
# lib_id
j8_block_new = j8_block.replace('"Connector_Generic_MountingPin:Conn_01x03_MountingPin"', '"Connector_Generic:Conn_01x03"')
# Value
j8_block_new = j8_block_new.replace('(property "Value" "Conn_01x03_MountingPin"', '(property "Value" "Conn_01x03"')
# Footprint
j8_block_new = j8_block_new.replace('"Connector_Molex:Molex_PicoBlade_53261-0371_1x03-1MP_P1.25mm_Horizontal"', '"Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"')
# Remove pin MP
mp_pos = j8_block_new.find('(pin "MP"')
if mp_pos != -1:
    mp_end = j8_block_new.find(')', j8_block_new.find(')', mp_pos) + 1) + 1
    # also include enclosing parens if any
    # let's inspect pin "MP" syntax:
    # (pin "MP"\n\t\t\t(uuid "...")\n\t\t)
    p_end = j8_block_new.find(')\n', mp_pos)
    p_end = j8_block_new.find(')\n', p_end + 1) + 2
    j8_block_new = j8_block_new[:mp_pos] + j8_block_new[p_end:]

comm = comm[:sym_start_j8] + j8_block_new + comm[sym_end_j8:]

# For J9:
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
print("Updated communication.kicad_sch (J8/J9 symbols and footprints)")
