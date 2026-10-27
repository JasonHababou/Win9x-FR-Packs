# Pour un dossier d'application : fonctions importees absentes de Windows 98,
# et lesquelles KernelEx (jumper) declare dans ses tables d'API (nom present dans
# KEXBASES/KEXBASEN/KERNELEX). Approximation : un nom present = API fournie.
# Usage : kexcover.py <dossier_app> <dossier_kex> <ref1> [ref2...]
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from checkimports import exports  # noqa: E402
from imports import imports  # noqa: E402

app, kex, refs = Path(sys.argv[1]), Path(sys.argv[2]), [Path(p) for p in sys.argv[3:]]
index = {}
for r in refs:
    for f in r.iterdir():
        if f.is_file():
            index.setdefault(f.name.upper(), f)
own = {p.name.upper() for p in app.rglob("*") if p.suffix.lower() in (".dll", ".exe")}
kexnames = set()
for p in kex.iterdir():
    if p.suffix.upper() in (".DLL",):
        kexnames |= {m.group().decode() for m in re.finditer(rb"[A-Za-z_][A-Za-z0-9_]{3,}", p.read_bytes())}
cache, missing, absent_dll = {}, defaultdict(set), defaultdict(set)
for pe in sorted(app.rglob("*")):
    if pe.suffix.lower() not in (".dll", ".exe"):
        continue
    try:
        imp = imports(str(pe))
    except Exception:
        continue
    for dll, funcs in imp.items():
        D = dll.upper()
        if D in own:
            continue
        f = index.get(D)
        if not f:
            absent_dll[D].add(pe.relative_to(app).as_posix())
            continue
        if D not in cache:
            cache[D] = exports(f) or set()
        for fn in funcs:
            if fn not in cache[D]:
                missing[(D, fn)].add(pe.relative_to(app).as_posix())
print("DLL absentes de Windows 98 :")
for d, users in sorted(absent_dll.items()):
    print(f"  {d:28} ({len(users)} fichiers, ex. {sorted(users)[0]})")
cov = [k for k in missing if k[1] in kexnames]
unc = [k for k in missing if k[1] not in kexnames]
print(f"\nFonctions absentes de 98 : {len(missing)} ; fournies par KernelEx : {len(cov)} ; NON couvertes : {len(unc)}")
for d, fn in sorted(unc):
    users = sorted(missing[(d, fn)])
    print(f"  {d:14} {fn:40} {len(users):3} fichiers ex. {users[0]}")
