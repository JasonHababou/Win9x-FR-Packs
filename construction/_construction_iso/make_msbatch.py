# Fichier de reponses MSBATCH.INF pour l'ISO Win98FR : composants preselectionnes
# (tout coche sauf la liste de l'utilisateur), installation personnalisee avec
# ecrans visibles (Express=0) pour pouvoir verifier ; cle vide = Setup la demande.
# Noms des composants = descriptions FR des INF du CD (liste w98_composants.txt).
# Composants du pack (W98FRPK.INF, 4e argument) : tous coches.
# Usage : make_msbatch.py <w98_composants.txt> <MSBATCH.INF de sortie> [cle] [W98FRPK.INF]
import re
import sys
from pathlib import Path

NON = {"Porte-documents", "Carnet d'adresses", "Microsoft Chat 2.5", "NetMeeting",
       "Numéroteur téléphonique", "Réseau privé virtuel (VPN)", "Serveur d'accès réseau à dist.",
       "Support ATM pour l'accès à dist.", "Assistant Publication de sites Web",
       # WMI : recoche pour PNTFS.VBS (test12), sans effet (GetObject winmgmts toujours
       # en echec sous 98) ; le pack utilise maintenant NTFSCFG.VBS, sans WMI (2026-10-20)
       "Gestion système par interface Web",
       "Microsoft Wallet", "Partage de connexion Internet",
       "Serveur Web personnel", "Outlook Express", "AOL", "CompuServe", "France Telecom"}
cle = sys.argv[3] if len(sys.argv) > 3 else ""
comps = []
for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    m = re.match(r"\s*- (.+?)\s+\[type=(\d*)\]", l)
    if m and m.group(2):                       # type vide = groupe (pas une entree MSBATCH)
        comps.append(m.group(1))
pack = []
if len(sys.argv) > 4:
    pack = re.findall(r'^W98FR_\w+_DESC = "([^"]+)"', Path(sys.argv[4]).read_bytes().decode("cp1252"), re.M)
manque = NON - set(comps)
assert not manque, manque
t = ["; MSBATCH.INF - ISO Windows 98 SE FR (pack Win98FR)",
     "; Lu automatiquement par SETUP.EXE (dossier WIN98). Installation personnalisee :",
     "; les ecrans restent affiches, les composants sont deja coches comme voulu.",
     "; ProductKey vide : Setup demande la cle a l'ecran.",
     "", "[BatchSetup]", "Version=3.0 (32-bit)", "",
     "[Version]", 'Signature = "$CHICAGO$"', "AdvancedINF=2.5", "LayoutFile=layout.inf", "",
     "[Setup]", "Express=0", "InstallType=3", "OptionalComponents=1", "EBD=0",
     "Uninstall=0", "NoDirWarn=1", "ShowEula=0",            # pas d'ecran du contrat de licence
     # Dossier impose : sur un disque deja formate, W98FRMEM.BAT cree C:\WINDOWS\SYSTEM.INI
     # (limite memoire) avant Setup, qui s'installait alors dans C:\WINDOWS.000 (2026-10-21)
     r'InstallDir="C:\WINDOWS"',
     'TimeZone="Romance"',                      # Paris (TIMEZONE.INF) : plus de fenetre Date/Heure
     f'ProductKey="{cle}"' if cle else "ProductKey=",
     # Clavier et langue : sans eux, Setup prenait "Belge (point)" (premier de la liste,
     # SETUPLOG.TXT du GX240, ISO test15) -> keyb be dans AUTOEXEC.BAT (2026-10-27)
     "", "[System]", "Locale=L040C", "SelectedKeyboard=KEYBOARD_0000040C",
     "", "[OptionalComponents]"]
t += [f'"{c}"={0 if c in NON else 1}' for c in comps]
t += ["", "; Pack Windows 98 FR (W98FRPK.INF) : installe au premier demarrage"] + [f'"{c}"=1' for c in pack]
Path(sys.argv[2]).write_bytes(("\r\n".join(t) + "\r\n").encode("cp1252"))
print(len(comps), "composants,", sum(c in NON for c in comps), "decoches,", len(pack), "du pack")
