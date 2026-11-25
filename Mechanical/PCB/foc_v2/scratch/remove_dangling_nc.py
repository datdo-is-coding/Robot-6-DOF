with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Let's see the no_connect blocks for these two UUIDs:
# (no_connect (at ...) (uuid "a5cff69f-bcfb-4625-853a-16298f5a6f7b"))
# (no_connect (at ...) (uuid "3ac5a795-dbde-4abd-8c78-84beafc1b30f"))

import re

text_clean = re.sub(r'\(no_connect\s+\(at\s+226\.06\s+119\.38\)\s+\(uuid\s+"a5cff69f-bcfb-4625-853a-16298f5a6f7b"\)\s*\)\n?', '', text)
text_clean = re.sub(r'\(no_connect\s+\(at\s+226\.06\s+147\.32\)\s+\(uuid\s+"3ac5a795-dbde-4abd-8c78-84beafc1b30f"\)\s*\)\n?', '', text_clean)

with open("communication.kicad_sch", "w", encoding="utf-8") as f:
    f.write(text_clean)
print("Removed 2 dangling no_connect flags.")
