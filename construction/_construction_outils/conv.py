# Copie des fichiers texte UTF-8 (LF) vers le pack en cp1252 + CRLF (format Windows 98).
# Usage : conv.py <dossier_source> <dossier_pack>   ; le chemin relatif est conserve.
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
for f in sorted(p for p in src.rglob("*") if p.is_file()):
    rel = f.relative_to(src)
    text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.endswith("\n"):
        text += "\n"
    out = dst / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(text.replace("\n", "\r\n").encode("cp1252"))
    print("ecrit", rel, len(out.read_bytes()), "octets")
