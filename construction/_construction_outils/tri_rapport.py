import itertools
import json
import sys

r = json.load(open(sys.argv[1], encoding="utf-8"))
print("== Doublons exacts (SHA-1)")
by = {}
for n, v in r.items():
    by.setdefault(v["sha1"], []).append(n)
for h, ns in by.items():
    if len(ns) > 1:
        print("  ", ns)
print("\n== Volume / dossiers racine")
for n, v in r.items():
    print(f"{n[:50]:50} {v['size'] / 1048576:6.0f} Mo vol={v['vol'][:18]:18} {', '.join(v['top'][:14])}")


def key(r_, n):
    return {(k.split("\\")[-1], s) for k, s in r_[n]["files"].items()}


print("\n== Recouvrements (nom+taille identiques, % du plus petit)")
for a, b in itertools.combinations(list(r), 2):
    fa, fb = key(r, a), key(r, b)
    if not fa or not fb:
        continue
    inter = fa & fb
    small = min(len(fa), len(fb))
    pct = 100 * len(inter) / small
    if pct >= 25 and len(inter) >= 10:
        sm, big = (a, b) if len(fa) <= len(fb) else (b, a)
        print(f"  {pct:5.1f}%  {sm[:44]:44} dans {big[:44]}  ({len(inter)}/{small})")
