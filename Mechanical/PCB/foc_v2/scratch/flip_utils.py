import re

def flip_footprint_layers_to_back(chunk):
    # In a footprint placed on B.Cu, child layers must be on B.*
    # Replace (layer "F.
    chunk = re.sub(r'\(layer "F\.Cu"\)', '(layer "B.Cu")', chunk)
    chunk = re.sub(r'\(layer "F\.Mask"\)', '(layer "B.Mask")', chunk)
    chunk = re.sub(r'\(layer "F\.Paste"\)', '(layer "B.Paste")', chunk)
    chunk = re.sub(r'\(layer "F\.SilkS"\)', '(layer "B.SilkS")', chunk)
    chunk = re.sub(r'\(layer "F\.CrtYd"\)', '(layer "B.CrtYd")', chunk)
    chunk = re.sub(r'\(layer "F\.Fab"\)', '(layer "B.Fab")', chunk)
    # Also in pad layers: "F.Cu" "F.Mask" "F.Paste"
    chunk = re.sub(r'"F\.Cu"', '"B.Cu"', chunk)
    chunk = re.sub(r'"F\.Mask"', '"B.Mask"', chunk)
    chunk = re.sub(r'"F\.Paste"', '"B.Paste"', chunk)
    return chunk

def flip_footprint_layers_to_front(chunk):
    chunk = re.sub(r'\(layer "B\.Cu"\)', '(layer "F.Cu")', chunk)
    chunk = re.sub(r'\(layer "B\.Mask"\)', '(layer "F.Mask")', chunk)
    chunk = re.sub(r'\(layer "B\.Paste"\)', '(layer "F.Paste")', chunk)
    chunk = re.sub(r'\(layer "B\.SilkS"\)', '(layer "F.SilkS")', chunk)
    chunk = re.sub(r'\(layer "B\.CrtYd"\)', '(layer "F.CrtYd")', chunk)
    chunk = re.sub(r'\(layer "B\.Fab"\)', '(layer "F.Fab")', chunk)
    chunk = re.sub(r'"B\.Cu"', '"F.Cu"', chunk)
    chunk = re.sub(r'"B\.Mask"', '"F.Mask"', chunk)
    chunk = re.sub(r'"B\.Paste"', '"F.Paste"', chunk)
    return chunk

print("Defined robust layer flipping functions.")
