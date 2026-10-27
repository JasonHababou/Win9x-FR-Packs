# Pilote la machine QEMU par sa console (moniteur TCP 127.0.0.1:4444) :
#   pilote.py ecran <fichier.png>      capture d'ecran
#   pilote.py touches <t1> <t2> ...     touches QEMU (ex. ret, 1, ctrl-alt-delete, spc)
#   pilote.py texte "dir c:"            tape un texte (minuscules, chiffres, espace, : \ . -)
#   pilote.py cmd "info status"         commande brute du moniteur
import os
import socket
import sys
import time
from pathlib import Path

from PIL import Image

SPECIAL = {" ": "spc", ":": "shift-semicolon", "\\": "backslash", ".": "dot", "-": "minus",
           "/": "slash", "_": "shift-minus", "=": "equal", ",": "comma"}


def moniteur(cmds):
    s = socket.create_connection(("127.0.0.1", int(os.environ.get("QEMU_PORT", 4444))), timeout=10)  # 2e VM : QEMU_PORT=4445
    time.sleep(0.3)
    s.recv(65536)
    sortie = b""
    for c in cmds:
        s.sendall(c.encode() + b"\n")
        time.sleep(0.15)
        try:
            sortie += s.recv(65536)
        except socket.timeout:
            pass
    s.close()
    return sortie.decode(errors="replace")


act = sys.argv[1]
if act == "ecran":
    sortie = Path(sys.argv[2])
    ppm = sortie.with_suffix(".ppm")
    moniteur([f"screendump {ppm.as_posix()}"])
    for _ in range(40):                       # attend la fin de l'ecriture par QEMU
        time.sleep(0.5)
        try:
            Image.open(ppm).load()
            break
        except Exception:
            pass
    Image.open(ppm).save(sortie)
    ppm.unlink()
elif act == "touches":
    moniteur([f"sendkey {t}" for t in sys.argv[2:]])
elif act == "texte":
    # clavier QEMU = QWERTY US ; Windows/DOS FR (AZERTY) : on envoie les touches physiques
    azerty = {"a": "q", "q": "a", "z": "w", "w": "z", "m": "semicolon"}
    seq = []
    for ch in sys.argv[2]:
        if ch.isalpha():
            k = azerty.get(ch.lower(), ch.lower())
            seq.append(("shift-" + k) if ch.isupper() else k)
        elif ch.isdigit():
            seq.append("shift-" + ch)                 # AZERTY : chiffres avec Maj
        else:
            seq.append({" ": "spc", ":": "dot", "\\": "alt_r-8", ".": "shift-comma",
                        "-": "6", "=": "equal", "/": "shift-dot", "~": "alt_r-2", ",": "m",
                        '"': "3", "*": "backslash", "_": "8", "@": "alt_r-0",
                        "&": "1", "$": "bracket_right", "(": "5", ")": "minus",
                        "%": "shift-apostrophe", "<": "less", ">": "shift-less", "|": "alt_r-6", "!": "slash"}[ch])
    moniteur([f"sendkey {t}" for t in seq])
elif act == "texteus":
    # clavier QWERTY US (DOS sans KEYB FR) : touches = caracteres
    us = {" ": "spc", ":": "shift-semicolon", "\\": "backslash", ".": "dot", "-": "minus",
          "/": "slash", "_": "shift-minus", "=": "equal", ",": "comma", '"': "shift-apostrophe",
          "*": "shift-8", ">": "shift-dot", "<": "shift-comma", "@": "shift-2", ";": "semicolon",
          "|": "shift-backslash", "&": "shift-7", "$": "shift-4", "'": "apostrophe"}
    seq = []
    for ch in sys.argv[2]:
        if ch.isalpha():
            seq.append(("shift-" + ch.lower()) if ch.isupper() else ch)
        elif ch.isdigit():
            seq.append(ch)
        else:
            seq.append(us[ch])
    moniteur([f"sendkey {t}" for t in seq])
else:
    print(moniteur([" ".join(sys.argv[2:])]))
