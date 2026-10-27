import json
import sys

r = json.load(open(sys.argv[1], encoding="utf-8"))
pairs = [p.split("|") for p in sys.argv[2:]]
for a, b in pairs:
    A = {(k, s) for k, s in r[a]["files"].items()}
    B = {(k, s) for k, s in r[b]["files"].items()}
    na = {k.split("\\")[-1]: (k, s) for k, s in A}
    nb = {k.split("\\")[-1]: (k, s) for k, s in B}
    oa = sorted(set(na) - set(nb))
    ob = sorted(set(nb) - set(na))
    diffsz = sorted(n for n in set(na) & set(nb) if na[n][1] != nb[n][1])
    print(f"\n### {a}  <->  {b}")
    print(f"  seulement dans 1er ({len(oa)}) : {[na[n][0] + ' ' + str(na[n][1]) for n in oa[:12]]}")
    print(f"  seulement dans 2e  ({len(ob)}) : {[nb[n][0] + ' ' + str(nb[n][1]) for n in ob[:12]]}")
    print(f"  meme nom, taille differente ({len(diffsz)}) : {[(n, na[n][1], nb[n][1]) for n in diffsz[:10]]}")
