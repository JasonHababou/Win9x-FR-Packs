# Inventaire des images disque de win98se : SHA-1, volume, contenu, recouvrements.
# Usage : tri_iso.py <dossier> <sortie.json>
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = Path(sys.argv[1])
EXT = (".iso", ".bin", ".rar")
res = {}
for f in sorted(D.iterdir()):
    if not f.is_file() or f.suffix.lower() not in EXT:
        continue
    h = hashlib.sha1()
    with open(f, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 22), b""):
            h.update(chunk)
    out = subprocess.run(["7z", "l", "-slt", str(f)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout
    files, cur, vol, typ = {}, {}, "", ""
    for line in out.splitlines():
        if line.startswith("Path = ") and not cur and "Type = " not in out[:0]:
            pass
        m = re.match(r"^(\w[\w ]*) = (.*)$", line)
        if not m:
            if cur.get("Path") and cur.get("Folder") != "+" and cur.get("Size", "").isdigit():
                files[cur["Path"].upper().replace("/", "\\")] = int(cur["Size"])
            cur = {}
            continue
        k, v = m.groups()
        if k == "Type" and not typ:
            typ = v
        if k in ("Volume Label", "Comment") and not vol:
            vol = v
        cur[k] = v
    if cur.get("Path") and cur.get("Folder") != "+" and cur.get("Size", "").isdigit():
        files[cur["Path"].upper().replace("/", "\\")] = int(cur["Size"])
    files.pop(str(f).upper(), None)
    tops = sorted({p.split("\\")[0] for p in files})
    res[f.name] = {"size": f.stat().st_size, "sha1": h.hexdigest(), "type": typ, "vol": vol,
                   "nfiles": len(files), "data": sum(files.values()), "top": tops[:40],
                   "files": files}
    print(f"{f.name:60} {res[f.name]['nfiles']:6} fichiers  {typ}", flush=True)
json.dump(res, open(sys.argv[2], "w", encoding="utf-8"))
print("fin")
