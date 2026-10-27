# Fichier de reponses MSBATCH.INF pour l'ISO Windows ME FR : composants preselectionnes
# selon les choix de l'utilisateur (2026-10-20), ecrans visibles (Express=0).
# Noms des composants = descriptions FR des INF du CD ME (liste me_composants.txt,
# produite par w98_composants.py sur les INF du CD ME).
# Usage : make_msbatch_me.py <me_composants.txt> <MSBATCH.INF de sortie> [cle]
import re
import sys
from pathlib import Path

NON = {"Jeux Internet",                       # serveurs fermes, pas de mode hors ligne
       "Partage de connexion Internet",       # Internet par le reseau local
       "Porte-documents", "MSN Messenger Service", "NetMeeting",
       "Numéroteur téléphonique", "Réseau privé virtuel (VPN)",
       "Serveur d'accès réseau à dist.", "Carnet d'adresses", "Outlook Express", "AOL"}
cle = sys.argv[3] if len(sys.argv) > 3 else ""
comps = []
for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    m = re.match(r"\s*- (.+?)\s+\[type=(\d*)\]", l)
    if m and m.group(2):                       # type vide = groupe (pas une entree MSBATCH)
        comps.append(m.group(1))
manque = NON - set(comps)
assert not manque, manque
t = ["; MSBATCH.INF - ISO Windows ME FR (pack WinMeFR)",
     "; Lu automatiquement par SETUP.EXE (dossier WIN9X). Installation personnalisee :",
     "; les ecrans restent affiches, les composants sont deja coches comme voulu.",
     "", "[BatchSetup]", "Version=3.0 (32-bit)", "",
     "[Version]", 'Signature = "$CHICAGO$"', "AdvancedINF=2.5", "LayoutFile=layout.inf", "",
     "[Setup]", "Express=0", "InstallType=3", "OptionalComponents=1", "EBD=0",
     "Uninstall=0", "NoDirWarn=1", "ShowEula=0",
     # Dossier impose, comme pour 98 : un SYSTEM.INI cree avant Setup sur un disque
     # deja formate l'envoyait dans C:\WINDOWS.000 (bug ISO 98 test13, 2026-10-21)
     r'InstallDir="C:\WINDOWS"',
     'TimeZone="Romance"',
     f'ProductKey="{cle}"' if cle else "ProductKey=",
     # clavier et langue imposes (ISO 98 test15 : Setup avait pris "Belge (point)")
     "", "[System]", "Locale=L040C", "SelectedKeyboard=KEYBOARD_0000040C",
     # nom d'utilisateur : sinon page "Informations utilisateur" (tests QEMU 2026-10-21/26)
     "", "[NameAndOrg]", 'Name="Utilisateur"', 'Org=""', "Display=0",
     # nom de l'ordinateur : sinon page "Identification reseau" (test QEMU 2026-10-26)
     "", "[Network]", 'ComputerName="WINMEFR"', 'Workgroup="WORKGROUP"', 'Description="Windows Me FR"',
     "Display=0",
     # ISO WinMeFR : pack lance a l'ouverture de session. Le CD est cherche par sa lettre :
     # WMEFRCD.BAT a la racine (%% = % dans un INF). Cle Run et non RunOnce : si le CD
     # n'est pas encore pret, nouvel essai a la session suivante ; WMEFRCD.BAT efface la
     # valeur avant de lancer le pack, qui pose ensuite sa propre reprise sous ce nom
     "", "[Install]", "AddReg=WMEFR.Run",
     "", "[WMEFR.Run]",
     'HKLM,"Software\\Microsoft\\Windows\\CurrentVersion\\Run","WMEFR",,'
     '"command.com /c for %%d in (D E F G H I J K L M N O P Q R) do if exist %%d:\\WMEFRCD.BAT %%d:\\WMEFRCD.BAT %%d"',
     "", "[OptionalComponents]"]
t += [f'"{c}"={0 if c in NON else 1}' for c in comps]
Path(sys.argv[2]).write_bytes(("\r\n".join(t) + "\r\n").encode("cp1252"))
print(len(comps), "composants,", sum(c in NON for c in comps), "decoches")
