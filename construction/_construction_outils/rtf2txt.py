# Conversion RTF -> texte (simple : groupes ignores, \par, \'xx, \uN).
import re
import sys

t = open(sys.argv[1], encoding="cp1252", errors="replace").read()
out, i, depth, skip = [], 0, 0, []
ignore_dest = re.compile(r"\\(\*|fonttbl|colortbl|stylesheet|info|pict|themedata|colorschememapping|latentstyles|datastore|xmlnstbl|listtable|listoverridetable|rsidtbl|generator|mmathPr)")
while i < len(t):
    c = t[i]
    if c == "{":
        depth += 1
        if ignore_dest.match(t, i + 1):
            skip.append(depth)
        i += 1
    elif c == "}":
        if skip and skip[-1] == depth:
            skip.pop()
        depth -= 1
        i += 1
    elif c == "\\":
        m = re.match(r"\\([a-zA-Z]+)(-?\d+)? ?", t[i:])
        if m:
            w = m.group(1)
            if not skip:
                if w in ("par", "line", "row"):
                    out.append("\n")
                elif w == "tab" or w == "cell":
                    out.append("\t")
                elif w == "u" and m.group(2):
                    out.append(chr(int(m.group(2)) % 65536))
                    i += len(m.group(0))
                    if i < len(t) and t[i] == "?":
                        i += 1
                    continue
            i += len(m.group(0))
        elif t[i + 1] == "'":
            if not skip:
                out.append(bytes([int(t[i + 2:i + 4], 16)]).decode("cp1252", "replace"))
            i += 4
        else:
            if not skip:
                out.append(t[i + 1])
            i += 2
    elif c in "\r\n":
        i += 1
    else:
        if not skip:
            out.append(c)
        i += 1
text = re.sub(r"\n\s*\n+", "\n", "".join(out))
sys.stdout.reconfigure(encoding="utf-8")
print(text)
