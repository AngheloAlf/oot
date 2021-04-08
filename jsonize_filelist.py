#!/usr/bin/python3

import json
import subprocess

#filename = "filelists/filelist_ntsc_1.0.txt"
#output_filename = "ntsc1.0.json"

#with open(filename) as f:
#    b = f.readlines()

version = 'ntsc_1.0'

lines = str(subprocess.check_output(['python3', 'extract_baserom.py', version]))

data = {
    "memory": dict(),
    "files": list()
}

print(lines)

for l in lines.split("\\n"):
    print(l)
    if len(l) < 10:
        continue
    l = l.split("/")[1]
    name, addresses = l.split(" (")
    vrom = addresses.split(", ")[0][2:]
    #vrom = None
    #name = l.strip()
    # type = "Object" if name.startswith("object_") else "Room" if "_room_" in l else "Scene" if l.endswith("_scene") else "Unknow"
    type = "Unknow"
    if name.startswith("object_"):
        type = "Object"
    elif "_room_" in name:
        type = "Room"
    elif name.endswith("_scene"):
        type = "Scene"
    elif name == "code":
        type = "Code"
    file = {"vrom": vrom, "name": name, "type": type}
    data["files"].append(file)

js = json.dumps(data, indent=4)

with open(version + ".json", "w") as f:
    f.write(js)
