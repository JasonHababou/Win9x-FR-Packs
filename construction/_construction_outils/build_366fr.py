# Construit la "couche 3.66 filtree FR" a partir de SPUPDATE.INF (U98SESP3.66).
# Base : etude Win98FR_v2\ETUDE_BASE_366.md (§4) + fichiers FR de
# WIN9X\Mise a jour\FR pour la 3.66. Rien n'est ecrit dans Win98FR_v2.
# Usage : build_366fr.py <racine win98se> <dossier de sortie>
#   sortie\sp366fr\        : fichiers + SP366FR.INF (cp1252 + CRLF)
#   sortie\RAPPORT_366FR.TXT : decision par fichier + effet sur la sauvegarde de reference
# 3e argument facultatif : dossier de la sauvegarde de reference (defaut : Sauvegarde 4)
import csv
import shutil
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from checkimports import exports  # noqa: E402
from imports import imports  # noqa: E402

R, OUT = Path(sys.argv[1]), Path(sys.argv[2])
A = R / "Sources/AfterLife Fr/U98SESP3.66"
SRC = A / "SP3"
FRD = R / "WIN9X/Mise a jour/FR pour la 3.66"
CSV = R / "Sources/AfterLife Fr/listingExtrait/etude366_fichiers.csv"
S4 = Path(sys.argv[3]) if len(sys.argv) > 3 else R / "bkpWin98/Sauvegarde 4 aprés gros patch"
BASE = S4.name
REF98 = R / "bkpWin98/Sauvegarde Saine 3 apres patch/WINDOWS"

# --- Exclusions (ETUDE_BASE_366.md §2 et §4) ---
EXCLU = {
    # DOS et demarrage : versions EN (messages FR du SP3.0 / CD perdus)
    "COMMAND.COM": "DOS EN", "IO.SYS": "IO.SYS RLoew EN (WINBOOT.SYS FR garde)",
    "FDISK.EXE": "DOS EN", "FORMAT.COM": "DOS EN", "SCANDISK.EXE": "DOS EN",
    "KEYB.COM": "DOS", "HELP.COM": "DOS EN", "HELP.HLP": "DOS EN", "QBASIC.EXE": "DOS EN",
    "QBASIC.HLP": "DOS EN", "DOSHELP.PIF": "DOS EN", "SMARTDRV.EXE": "DOS EN",
    "CMD.EXE": "cmd de NT, inutile sous 98",
    # Aide et textes EN
    "HARDWARE.HLP": "aide EN", "HYPERTRM.CHM": "aide EN", "HYPERTRM.HLP": "aide EN",
    "QFECHECK.HLP": "aide EN", "TSHOOT.OCX": "depanneurs EN", "TSHOOT98.CHM": "aide EN",
    "HTMLHELP.HTM": "aide EN", "RUNHELP.CAB": "aide EN", "GLOSSARY.HLP": "aide EN",
    "U98SESP3.CHM": "aide de la 3.66", "JETCOMP.DOC": "doc EN", "WINALI.TXT": "texte EN",
    "WINALX.TXT": "texte EN",
    # INF EN ou geres ailleurs
    "1394.INF": "INF EN", "NTMAP.INF": "INF EN", "SATA.INF": "INF EN (pas de SATA sur GX240)",
    "TWEAKS.INF": "reglages : 05_EXTRA\\tweaks", "MSHDC.INF": "SP3.0 >= 3.66", "RNA.INF": "SP3.0 >= 3.66",
    # Systeme
    "VMM32.VXD": "VMM32 generique : ecraserait celui construit pour la machine",
    "SP3.CAB": "archive de la 3.66 (PRECOPY), inutile",
    "CONVMEM.VXD": "a etudier a part (avec FILE64)", "FILE64.VXD": "fichiers > 4 Go : a etudier a part",
    "FILE64.DLL": "fichiers > 4 Go : a etudier a part",
    "VCOMP.DLL": "OpenMP : fonctions absentes de 98",
    "SMARTVSD.VXD": "SMART dans IOSUBSYS : choix d'origine de 98 SE garde (rien a gagner sur carte CF)",
    # Outils a interface EN (rien a gagner)
    "WINALIGN.EXE": "outil EN", "POLEDIT.EXE": "outil EN", "CERTMGR.EXE": "outil EN",
    "MSICUU.EXE": "outil EN", "JETCOMP.EXE": "outil EN", "U98SEUSB.EXE": "outil EN de la 3.66",
    "KEYREMAP.DLL": "Key Remap EN", "KEYREMAP.VXD": "Key Remap EN",
    "THEMES.EXE": "Plus! 98 FR garde", "THEMES.CPL": "Plus! 98 FR garde",
    "WRITE32.WPC": "pas de version FR",
    # Conflits deja equivalents en FR (code identique, ETUDE §2)
    "CONTROL.EXE": "FR deja equivalent", "REGEDIT.EXE": "FR deja equivalent",
    "SYSTRAY.EXE": "FR deja equivalent", "HOTPLUG.DLL": "FR deja equivalent",
    "GDI.EXE": "FR deja equivalent (03_SYST)",
    # Teste sur GX240 (2026-10-17) : MFC42 6.2.8092 de la 3.66 fait fermer les tests de
    # 3DMark 2001 SE et 03 des le lancement ; la 6.2.4131 du pack (SP3.0) les fait marcher.
    "MFC42.DLL": "fait planter 3DMark 2001/03 (test GX240) : version du SP3.0 gardee",
    # MSVCRT 7.0.9981 : bloque l'installation silencieuse de K-Lite 3.4.5 et celle de
    # 3DMark 2001 SE ("Initializing Texture conversion") ; RETOUR F les debloque (GX240).
    "MSVCRT.DLL": "bloque les installeurs K-Lite et 3DMark 2001 (test GX240) : version du SP3.0 gardee",
}
# Fichiers FR reconstruits : version FR < 3.66 -> copie sans controle de version
FR_FORCE = {"NOTEPAD.EXE", "SNDVOL32.EXE", "SYSMON.EXE", "COMDLG32.DLL", "KERNEL32.DLL"}
FLAG_FORCE = "36"  # 4 = pas de controle de version, 32 = pas de question

DEST_S4 = {"10": "WINDOWS", "11": "WINDOWS/SYSTEM", "12": "WINDOWS/SYSTEM/IOSUBSYS",
           "13": "WINDOWS/COMMAND", "17": "WINDOWS/INF", "18": "WINDOWS/HELP",
           "22": "WINDOWS/SYSTEM/VMM32", "30": "", "49001": "Program Files",
           "35353": "Program Files/Fichiers communs"}


def verlang(p):
    d = p.read_bytes()
    i = d.find(b"\xbd\x04\xef\xfe")
    v = ""
    if i >= 0:
        ms, ls = struct.unpack_from("<II", d, i + 8)
        v = f"{ms >> 16}.{ms & 0xffff}.{ls >> 16}.{ls & 0xffff}"
    lang = ""
    j = d.find("Translation".encode("utf-16-le"))
    if j >= 0:
        k = j + 24
        k += (-k) % 4
        lid = struct.unpack_from("<H", d, k)[0]
        lang = {0x40c: "FR", 0x409: "EN", 0: "neutre"}.get(lid, hex(lid))
    return v, lang


def vkey(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return ()


def find_ci(folder, name):
    if not folder.is_dir():
        return None
    for p in folder.iterdir():
        if p.name.upper() == name.upper():
            return p
    return None


def s4_path(dest, name):
    base, _, sub = dest.partition(",")
    rel = DEST_S4.get(base.strip())
    if rel is None:
        return None
    d = S4 / rel
    for part in sub.strip().split("\\") if sub.strip() else []:
        # noms courts 8.3 de la 3.66 (ACCESS~1, MICROS~1...) : premier dossier qui correspond
        stem = part.split("~")[0].upper()
        m = sorted(p for p in d.iterdir() if p.is_dir() and p.name.upper().startswith(stem)) if d.is_dir() else []
        if not m:
            return None
        d = m[0]
    return find_ci(d, name)


# --- Lecture de SPUPDATE.INF ---
lines = (A / "SPUPDATE.INF").read_bytes().decode("cp1252").replace("\r", "").split("\n")
sec, order = {}, []
cur = None
for l in lines:
    if l.startswith("[") and l.rstrip().endswith("]"):
        cur = l.strip()[1:-1]
        sec[cur] = []
        order.append(cur)
    elif cur is not None and l.strip() and not l.lstrip().startswith(";"):
        sec[cur].append(l)

verdict = {(r["Fichier"].upper(), r["Section"]): r for r in csv.DictReader(open(CSV, encoding="utf-8-sig"))}
idx98 = {}
for sub in ("SYSTEM", ""):
    for p in (REF98 / sub).iterdir():
        if p.is_file():
            idx98.setdefault(p.name.upper(), p)

copy_secs = [s.strip() for s in next(l for l in sec["DefaultInstall"] if l.startswith("CopyFiles")).split("=")[1].split(",")]
dests = {l.split("=")[0].strip(): l.split("=", 1)[1].strip() for l in sec["DestinationDirs"]}

pack = OUT / "sp366fr"
if pack.exists():
    shutil.rmtree(pack)
pack.mkdir(parents=True)

rapport, new_secs, kept_files = [], {}, set()
stats = {}
for s in copy_secs:
    for l in sec[s]:
        p = [x.strip() for x in l.split(",")]
        name, flag = p[0].upper(), (p[3] if len(p) > 3 else "")
        r = verdict.get((name, s), {})
        vd = r.get("Verdict", "")
        src, why = None, ""
        if name in EXCLU:
            why = "EXCLU : " + EXCLU[name]
        elif vd.startswith(("SP3.0 >=", "Couche1 >=", "W98FR >=")):
            why = "EXCLU : " + vd + " (rien a gagner)"
        elif vd.startswith("CONFLIT") or name == "DESK.CPL":
            f = find_ci(FRD, name)
            if f:
                src = f
                if name in FR_FORCE:
                    flag = FLAG_FORCE
                    why = "FR reconstruit (corrections 3.66 reportees), copie forcee"
                else:
                    why = "FR au meme numero ou plus recent (WIN9X\\...\\FR pour la 3.66)"
            else:
                why = "EXCLU : conflit FR sans version FR"
        elif vd == "source 3.66 introuvable":
            why = "EXCLU : " + vd
        else:
            src = find_ci(SRC, name)
            why = "3.66 : " + vd if src else "EXCLU : fichier absent de SP3"
        dst = dests.get(s, "")
        v366 = r.get("V366", "")
        vsrc, lsrc = verlang(src) if src else ("", "")
        s4 = s4_path(dst, name)
        vs4 = verlang(s4)[0] if s4 else ""
        effet = ""
        if src:
            if s4 is None:
                effet = ("absent de " + BASE + " -> ignore (drapeau 1056 : remplace seulement)"
                         if flag == "1056" else "nouveau fichier")
            elif not vsrc or not vs4:
                effet = "pas de numero de version : copie"
            elif vkey(vsrc) > vkey(vs4):
                effet = f"MISE A JOUR {vs4} -> {vsrc}"
            elif vkey(vsrc) == vkey(vs4):
                effet = "identique (deja installe)" if flag != FLAG_FORCE else f"copie forcee, meme numero {vs4}"
            else:
                effet = (f"!! RETROGRADE {vs4} -> {vsrc} (copie forcee)" if flag == FLAG_FORCE
                         else f"ignore : installe plus recent ({vs4})")
            miss = []
            if src.suffix.upper() in (".DLL", ".EXE", ".OCX", ".CPL") and src.read_bytes()[:2] == b"MZ":
                try:
                    for dll, funcs in imports(str(src)).items():
                        e = exports(idx98[dll.upper()]) if dll.upper() in idx98 else None
                        if e is not None:
                            miss += [f"{dll}:{x}" for x in funcs if x not in e]
                except Exception:
                    pass
            if miss:
                effet += "  | imports absents de 98 : " + " ".join(miss[:4])
            if name not in kept_files:
                shutil.copy2(src, pack / name)
                kept_files.add(name)
            new_secs.setdefault(s, []).append(name + (",,," + flag if flag else ""))
        key = why.split(" :")[0].split(" (")[0]
        stats[key] = stats.get(key, 0) + 1
        rapport.append((s, name, why, vsrc or v366, lsrc, vs4, effet))

# --- Registre et reglages filtres ---
EN_PAYS = {"Serbia": "Serbie", "Montenegro": "Monténégro", "Tajikistan": "Tadjikistan"}
arh = []
for l in sec["ARH"]:
    u = l.upper()
    # VXD\KEYREMAP : KEYREMAP.VXD est exclu ; la cle StaticVxD restante donnait
    # "Impossible de trouver un gestionnaire de peripherique" a chaque
    # demarrage (test GX240, 2026-10-17)
    if any(k in u for k in ("COMMAND PROCESSOR", "WINALIGN", "176AA2C0", "\\KEYBOARD\\SHELLEX",
                            "RENAMEFILES\\IO.SYS", "\\VXD\\KEYREMAP")):
        continue
    if "%KT%" in l and ",Name," in l:
        n = l.rsplit(",", 1)[1]
        l = l.rsplit(",", 1)[0] + "," + EN_PAYS.get(n, n)
    arh.append(l)
drh = [l for l in sec["DRH"] if not any(k in l for k in ("Setup\\Preserve", "Setup\\Updates",
                                                           "Uninstall\\Windows"))]
uif = [l for l in sec["UIF"] if "fontsubstitutes" in l]
dvf = []  # SMARTVSD reste ou 98 SE le met ; MSIEXEC et MSLS31 gardes
rnf = [l for l in sec["RNF"] if "TSHOOT" not in l.upper()]

out = ["; Win98FR : couche U98SESP3.66 filtree (fichiers 3.66 sans perte de FR).",
       "; Genere par _construction_outils\\build_366fr.py - ne pas modifier a la main.",
       "; Exclus : DOS/aide/INF EN, IO.SYS, VMM32.VXD, outils EN, date US, effacement de",
       "; Setup\\Updates, MSIEXEC EN, NOVOLTRK, convmem/file64. Detail : RAPPORT_366FR.TXT",
       "[Version]", "Signature=$CHICAGO$", "AdvancedINF=2.5", "",
       "[DefaultInstall]", "SmartReboot=N", "CustomDestination=CDD",
       "CopyFiles=" + ",".join(s for s in copy_secs if s in new_secs),
       "RegisterOCXs=RNF", "AddReg=ARH", "DelReg=DRH", "UpdateInis=UIF", ""]
for s in ("CDD", "ProgramFilesDir", "CommonFilesDir"):
    out += [f"[{s}]"] + sec[s] + [""]
out += ["[DestinationDirs]"] + [f"{s}={dests[s]}" for s in copy_secs if s in new_secs] + [""]
for s in copy_secs:
    if s in new_secs:
        out += [f"[{s}]"] + new_secs[s] + [""]
out += ["[RNF]"] + rnf + ["", "[ARH]"] + arh + ["", "[DRH]"] + drh
out += ["", "[UIF]"] + uif + [""]
strings = [l for l in sec["Strings"]]
strings = [('ShowAttributes="Afficher les attributs des fichiers dans la vue Détails"'
            if l.startswith("ShowAttributes") else l) for l in strings]
out += ["[Strings]"] + strings + ["", "[SourceDisksNames]", "1=,,0", ""]
(pack / "SP366FR.INF").write_bytes("\r\n".join(out).encode("cp1252"))

# --- Rapport ---
rp = ["Couche 3.66 filtree FR - rapport de construction (build_366fr.py)",
      "Effet calcule sur bkpWin98\\" + BASE + " (installation reelle du pack).",
      "Imports controles sur Sauvegarde Saine 3 (Windows 98 FR).", "",
      "Bilan : " + ", ".join(f"{k} = {v}" for k, v in sorted(stats.items())),
      f"Fichiers dans sp366fr : {len(kept_files)}", ""]
w = "{:5} {:14} {:16} {:7} {:16} {}"
for grp, test in (("RETENUS", lambda x: not x[2].startswith("EXCLU")), ("EXCLUS", lambda x: x[2].startswith("EXCLU"))):
    rp += ["=" * 100, grp, "=" * 100, w.format("Sect", "Fichier", "Version", "Langue", BASE[:16], "Decision / effet")]
    for s, n, why, v, lg, v4, eff in rapport:
        if test((s, n, why)):
            rp.append(w.format(s, n, v[:16], lg, v4[:16], why + ("  => " + eff if eff else "")))
    rp.append("")
rp += ["Registre : " + str(len(arh)) + " lignes gardees sur " + str(len(sec["ARH"])) +
       " (retire : CMD.EXE comme interpreteur, WinAlign, Key Remap, IO.SYS ; pays traduits en FR ;",
       "colonne Attributs de l'Explorateur traduite). DelReg : " + str(len(drh)) + "/" + str(len(sec["DRH"])) +
       " (garde l'historique Setup\\Updates et Uninstall\\Windows). UpdateInis : " + str(len(uif)) + "/" +
       str(len(sec["UIF"])) + " (pas de date US, ni convmem/file64, ni raccourcis d'outils EN).",
       "Commandes avant/apres de la 3.66 non reprises (2_4DATE, CRLUPD/ROOTSUPD deja dans 03_SYST,",
       "NOVOLTRK, PRESERVE, RVKROOTS, INSTMSIA EN, SPUPDATE.BAT, VERINST)."]
(OUT / "RAPPORT_366FR.TXT").write_bytes("\r\n".join(rp).encode("cp1252"))
print("\n".join(rp[:7]))
