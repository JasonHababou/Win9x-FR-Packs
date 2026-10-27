# INSTALL.BAT (v3) : reponses automatiques pour l'ISO Win98FR. Quand
# C:\W98FR\CHOIX.BAT existe (ecrit par LANCE.BAT + CHOIX.VBS d'apres les
# composants coches pendant l'installation de Windows), il pose W98AUTO=1 et
# C_<code>=O pour chaque case cochee : chaque question O/N est alors repondue
# toute seule (case absente = N). Sans CHOIX.BAT, rien ne change (CD V3).
# Usage : patch_auto.py <INSTALL.BAT entree> <INSTALL.BAT sortie>
import sys
from pathlib import Path

# debut du texte de la question -> code de la case (C_<code>)
QUESTIONS = [
    ("Installer MS Agent 2.0", "AGENT"), ("WinTop, moniteur", "WINTOP"),
    ("Invite de commande ici", "DOSH"), ("Logos de demarrage", "LOGO"),
    ("Windows Script Host FR", "WSH"), ("Console MMC", "MMC"), ("RegClean", "REGCL"),
    ("Outil SharedDLLs", "SHDLL"), ("Fuseaux horaires", "TZ"), ("Dossiers compresses", "ZIP"),
    ("Extension TrueType", "TTF"), (".NET Framework 1.1", "NET11"), ("Detecter et installer", "CHIP"),
    ("Visual C++ 2005", "VC5"), ("Visual C++ 2008", "VC8"), ("QRes (jeux", "QRES"),
    ("7-Zip 9.20", "7Z"), ("DAEMON Tools", "DT"), ("RetroZilla", "RZ"), ("Jeu de Tarot", "TAROT"),
    ("Fraps 1.9D", "FRAPS"), ("Raccourci de bascule MSVCRT", "MSVC"),
    ("Installer la couche 3.66", "366"), ("Installer PATCHMEM", "PMEM"),
    ("Activer le DMA", "DMA"), ("Surveiller l'installation d'un pilote NVIDIA", "NVSURV"),
]
A = 'if "%W98AUTO%"=="1" '
L = Path(sys.argv[1]).read_bytes().decode("cp1252").split("\r\n")
assert not any(l.startswith(":OK") for l in L)
out, faits, rb = [], set(), 0
i = 0
while i < len(L):
    l = L[i]
    q = next((c for t, c in QUESTIONS if l.startswith(f'choice /C:ON /N "{t}')), None)
    if q:
        j = next(k for k in range(i + 1, i + 4) if L[k].startswith("if errorlevel 2 goto "))
        non = L[j].split()[-1]
        out += [f'{A}if not "%C_{q}%"=="O" goto {non}', f"{A}goto OK{q}"] + L[i:j + 1] + [f":OK{q}"]
        faits.add(q)
        i = j + 1
        continue
    if l.startswith('choice /C:ON /N "Redemarrer maintenant ?'):
        rb += 1
        assert L[i + 1].startswith("if errorlevel 2 goto ")
        out += [f"{A}goto OKRB{rb}", l, L[i + 1], f":OKRB{rb}"]
        i += 2
        continue
    if l.startswith("choice /C:123456 /N"):                      # DirectX : pack 2
        out += [f"{A}goto ST8", l]
    elif l.startswith('choice /C:CA /N /T:C,10'):                # reprise apres redemarrage
        out += [f"{A}goto %RSTEP%", l]
    elif l == ":MENU":
        out += [l, f"{A}goto MODET"]
    elif l == ":DEBUT":
        out += [l, "REM ISO Win98FR : composants coches pendant l'installation de Windows",
                r"if exist C:\W98FR\CHOIX.BAT call C:\W98FR\CHOIX.BAT"]
    elif l == r"if exist C:\W98FR\EXTRAS.TXT del C:\W98FR\EXTRAS.TXT" and out[-1].startswith("if exist C:\\W98FR\\REPRISE"):
        out += [l, r"if exist C:\W98FR\CHOIX.BAT del C:\W98FR\CHOIX.BAT",
                r"if exist %WINDIR%\W98FRGO.BAT del %WINDIR%\W98FRGO.BAT"]
    else:
        out.append(l)
    i += 1
manque = {c for _, c in QUESTIONS} - faits
assert not manque, manque
assert rb == 2
assert all(len(l) < 127 for l in out)
Path(sys.argv[2]).write_bytes("\r\n".join(out).encode("cp1252"))
print(len(faits), "questions automatisees,", rb, "redemarrages")
