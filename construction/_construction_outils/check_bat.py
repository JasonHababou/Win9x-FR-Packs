# Verificateur statique des .bat du pack Win98FR pour COMMAND.COM (Windows 98).
# Usage : check_bat.py <racine Win98FR>
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
ENV = {"WINDIR": r"C:\WINDOWS", "COMSPEC": r"C:\WINDOWS\COMMAND.COM", "R": r"C:\W98FR\RUNONCE.REG",
       "T": r"C:\W98FR\W2K", "S": r"C:\WINDOWS\SYSTEM", "B": r"C:\W98FR\BAK", "W98DRV": "T:",
       # chemin realiste et long pour tester la limite de 127 caracteres
       "W98DIR": r"<DOSSIER_WINDOWS>\win98se\Win98FR\w",
       "EXTRAS": "oui", "CHIPSET": "INCONNU", "W98ENV": "1"}
FORBIDDEN = [(r"%~", "extension %~ (cmd.exe)"), (r"\belse\b", "else"), (r"2>", "redirection 2>"),
             (r"&&|\|\|", "&& ou ||"), (r"(?i)\bfor\s+/f", "FOR /F"), (r"(?i)\bset\s+/p", "SET /P"),
             (r"(?i)\bcall\s+:", "CALL :etiquette"), (r"(?i)setlocal|endlocal", "SETLOCAL"),
             (r"(?i)\bchoice\b.*\s/m\b", "CHOICE /M"), (r"(?i)start\s+/wait", "start /wait"),
             (r"(?i)^(?!echo)\s*\(|^(?!echo).*\)\s*$", "bloc entre parentheses")]
WIN_PROGS = re.compile(r"(?i)^\s*(rundll32|regedit|regsvr32|cscript|control)(\.exe)?\b")


def expand(line):
    return re.sub(r"%([A-Za-z0-9_]+)%", lambda m: ENV.get(m.group(1).upper(), m.group(0)), line)


def find(cwd, name):
    """Recherche insensible a la casse (comme FAT/Windows 98)."""
    p = cwd
    for part in re.split(r"[\\/]", name):
        if part in ("", "."):
            continue
        if part == "..":
            p = p.parent
            continue
        if not p.is_dir():
            return None
        hit = [c for c in p.iterdir() if c.name.lower() == part.lower()]
        if not hit:
            return None
        p = hit[0]
    return p


def check(bat, start_dir):
    errs, warns = [], []
    raw = bat.read_bytes()
    if b"\r\n" not in raw or raw.count(b"\n") != raw.count(b"\r\n"):
        errs.append("fins de ligne non CRLF")
    lines = raw.decode("cp1252").split("\r\n")
    labels, gotos = {}, []
    for i, l in enumerate(lines, 1):
        m = re.match(r"^:(\S+)", l)
        if m:
            key = m.group(1).upper()[:8]
            if key in labels:
                errs.append(f"L{i}: etiquette '{m.group(1)}' en collision (8 car.) avec L{labels[key][0]} '{labels[key][1]}'")
            labels[key] = (i, m.group(1))
    cwd, label_cwd = start_dir, {}
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if s.upper().startswith("REM") and re.search(r"[<>|]", s):
            errs.append(f"L{i}: REM contenant < > ou | (COMMAND.COM redirige meme les REM) : {s[:60]}")
        if not s or s.upper().startswith("REM"):
            continue
        m = re.match(r"^:(\S+)", s)
        if m:
            cwd = label_cwd.get(m.group(1).upper(), cwd)
            continue
        for pat, what in FORBIDDEN:
            if re.search(pat, s):
                errs.append(f"L{i}: interdit ({what}) : {s}")
        if re.match(r"(?i)^echo[ .]", s):
            if len(expand(s)) > 126:
                errs.append(f"L{i}: {len(expand(s))} car. apres expansion (> 126) : {s[:70]}...")
            continue
        ex = expand(s)
        if len(ex) > 126:
            errs.append(f"L{i}: {len(ex)} car. apres expansion (> 126) : {s[:70]}...")
        if WIN_PROGS.match(s) and not s.lower().startswith("start"):
            errs.append(f"L{i}: programme Windows sans 'start /w' : {s}")
        if re.search(r"(?i)\bchoice\b", s) and "/" in s.split("/N", 1)[-1].replace('"', "", 0) and not re.search(r'/N\s+(/T:\w,\d+\s+)?"', s):
            errs.append(f"L{i}: texte CHOICE contenant '/' sans guillemets")
        for g in re.findall(r"(?i)\bgoto\s+(\S+)", s):
            gotos.append((i, g))
            label_cwd.setdefault(g.upper(), cwd)
        m = re.match(r'(?i)^cd\s+"?([^"]+)"?$', s)
        if m and "%" not in m.group(1):
            new = find(cwd, m.group(1))
            if new is None or not new.is_dir():
                errs.append(f"L{i}: dossier introuvable depuis {cwd.relative_to(ROOT.parent)} : {s}")
            else:
                cwd = new
            continue
        # fichiers references depuis le dossier courant
        refs = []
        m = re.match(r'(?i)^(?:if exist \S+ )?start(?: /w)? (?:"([^"]+)"|(\S+))', s)
        if m:
            refs.append(m.group(1) or m.group(2))
        refs += re.findall(r"(?i)LaunchINFSection (\.\\[^,]+),", s)
        m = re.match(r"(?i)^call (\S+)", s)
        if m:
            refs.append(m.group(1))
        m = re.match(r'(?i)^start /w regedit /s "?([^"]+)"?$', s)
        if m:
            refs.append(m.group(1))
        for r in refs:
            r = expand(r)
            if re.match(r"(?i)^(rundll32|regedit|cscript)(\.exe)?$", r) or r.upper().startswith("C:\\") or "%" in r:
                continue
            if find(cwd, r) is None:
                errs.append(f"L{i}: fichier introuvable dans {cwd.relative_to(ROOT.parent)} : {r}")
    for i, g in gotos:
        if g.startswith('%'):
            continue
        if g.upper()[:8] not in labels:
            errs.append(f"L{i}: goto vers etiquette inexistante '{g}'")
    return errs, warns


targets = [(ROOT / "PLUS.BAT", ROOT), (ROOT / "KEXCHK.BAT", ROOT / "applis/firefox")] if (ROOT / "PLUS.BAT").exists() else [(ROOT / "w/install.bat", ROOT / "w"),
           (ROOT / "systeme/copie363/copie.bat", ROOT / "systeme/copie363"),
           (ROOT / "systeme/copie363/_CP.BAT", ROOT / "systeme/copie363"),
           (ROOT / "extras/msagent/msagent_install.bat", ROOT / "extras/msagent"),
           (ROOT / "extras/w2kcolor/w2kcolor.bat", ROOT / "extras/w2kcolor")]
if (ROOT / "INSTALL.BAT").exists():          # architecture v2 (Win98FR_v2)
    ENV["W98SUB"] = str(ROOT / "02_SP30")
    targets = [(ROOT / "INSTALL.BAT", ROOT),
               (ROOT / "03_SYST/copie363/copie.bat", ROOT / "03_SYST/copie363"),
               (ROOT / "03_SYST/copie363/_CP.BAT", ROOT / "03_SYST/copie363"),
               (ROOT / "05_EXTRA/msagent/msagent_install.bat", ROOT / "05_EXTRA/msagent"),
               (ROOT / "05_EXTRA/w2kcolor/w2kcolor.bat", ROOT / "05_EXTRA/w2kcolor")]
total = 0
for bat, d in targets:
    errs, _ = check(bat, d)
    total += len(errs)
    print(f"== {bat.relative_to(ROOT)} : {'OK' if not errs else str(len(errs)) + ' probleme(s)'}")
    for e in errs:
        print("   ", e)
sys.exit(1 if total else 0)
