# Groupe "Pack Windows 98 FR" dans l'ecran des composants du programme
# d'installation de Windows 98 : W98FRPK.INF (charge par SETUPPP.INF [load_inf],
# copie dans PRECOPY2.CAB). Chaque case cochee ecrit HKLM\Software\Win98FR\Choix,
# valeur <code> = "O" ; le pack (W98FRCD.BAT a la racine du CD, puis CHOIX.VBS) les lit au
# premier demarrage et repond tout seul a ses questions.
# BaseWinOptions (toujours execute) copie W98FRGO.BAT dans WINDOWS et cree la
# valeur Run\W98FR qui le lance au premier demarrage.
# Usage : make_composants.py <dossier de sortie>   (ecrit W98FRPK.INF, W98FRGO.BAT)
import sys
from pathlib import Path

# (code = variable C_<code> dans INSTALL.BAT, nom affiche, info-bulle)
COMPOSANTS = [
    ("366", "Couche 3.66 FR", "Fichiers du Service Pack 3.66 plus récents que le SP3.0 (filtrés FR)."),
    ("PMEM", "Correctif mémoire PATCHMEM", "Indispensable au-delà de 512 Mo de mémoire vive (RLoew)."),
    ("DMA", "DMA des disques et lecteurs IDE", "Transferts 2 à 3 fois plus rapides. Carte CF : seulement si elle le gère."),
    ("NVSURV", "Surveillance des pilotes NVIDIA", "Corrige au démarrage l'arrêt des pilotes NVIDIA 81.x et 82.x."),
    ("CHIP", "Pilotes chipset", "Détection de la carte mère, puis choix du paquet au premier démarrage."),
    ("DOSH", "Invite de commande ici", "Menu des dossiers : ouvrir une fenêtre MS-DOS dans ce dossier."),
    ("WINTOP", "Moniteur de tâches WinTop", "Processeur et mémoire de chaque programme (PowerToys, SP3.0)."),
    ("FRAPS", "Fraps 1.9D", "Images par seconde dans les jeux (raccourci sur le Bureau)."),
    ("SIV", "SIV, informations système", "Matériel complet : mémoire et timings, PCI, USB, disques, capteurs (gratuit)."),
    ("LOGO", "Logos de démarrage et d'arrêt animés", "Logos du SP3.0 (sans effet si Plus! 98 pose déjà les siens)."),
    ("WSH", "Windows Script Host 5.6 et 5.7", "WSH 5.6 du SP3.0 puis moteurs de script 5.7, menus français gardés."),
    ("ZIP", "Dossiers compressés .zip", "Ouvre les fichiers .zip comme des dossiers (Q329048, FR)."),
    ("VC5", "Visual C++ 2005", "Bibliothèques nécessaires à de nombreux programmes."),
    ("VC8", "Visual C++ 2008", "Bibliothèques Visual C++ 2008 pour 98 (exige KernelEx)."),
    ("QRES", "QRes et Raccourci de jeu", "Raccourcis de jeux avec résolution, couleurs et carte son."),
    ("7Z", "7-Zip 9.20", "Archives 7z, zip, rar... interface française."),
    ("DT", "DAEMON Tools 3.47", "Lecteur CD virtuel pour les images de disques."),
    ("RZ", "RetroZilla 2.3", "Navigateur web."),
    ("MSVC", "Bascule MSVCRT 6.1 - 7.0", "Raccourci sur le Bureau pour changer de version de MSVCRT."),
    ("NET11", ".NET Framework 1.1 FR", ".NET 1.1 avec SP1 et KB886903 (10 à 20 minutes d'installation)."),
    ("TAROT", "Jeu de Tarot (Sybex)", "Jeu de Tarot en français, installé dans C:\\JEUX\\TAROT."),
]
# Mises a jour de composants systeme : toujours installees, sans case
# (P9X : patcher9x re-applique avant chaque redemarrage, comme dans les CAB de l'ISO)
# fuseaux horaires 2020 FR, extension TrueType, patcher9x (sans le correctif memoire)
TOUJOURS = ["TZ", "TTF", "P9X"]


out = Path(sys.argv[1])
K = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Setup\\OptionalComponents"
t = ["; W98FRPK.INF - composants du pack Windows 98 SE FR (ISO Win98FR)",
     "; Les cases ne font qu'enregistrer un choix (HKLM\\Software\\Win98FR\\Choix) :",
     "; le pack lu au premier demarrage (racine du CD) installe ce qui est coche.",
     "", "[version]", "LayoutFile= Layout.inf, Layout1.inf, Layout2.inf", 'signature="$CHICAGO$"',
     "SetupClass=BASE", "", "[BaseWinOptions]", "W98FR_Base", "",
     "[DestinationDirs]", "W98FR_Base.Inf = 17", "W98FR_Base.Win = 10", "",
     "[W98FR_Base]", "AddReg    = W98FR_Base.AddReg", "CopyFiles = W98FR_Base.Inf, W98FR_Base.Win",
     "UpdateInis = W98FR_Base.Mem", "",
     "[W98FR_Base.Inf]", "w98frpk.inf", "", "[W98FR_Base.Win]", "w98frgo.bat", "",
     "; Limite de memoire (512 Mo) tant que PATCHMEM n'est pas installe, comme l'UBCD :",
     "; Windows 98 plante au demarrage avec plus de 1 Go. Le SP3.0 la porte a 1 Go",
     "; (MaxPhysPage=40000), PATCHMEM (03_SYST\\rloew\\SYSINI.INF) la retire.",
     "[W98FR_Base.Mem]", 'system.ini, 386Enh,, "MaxPhysPage=20000"',
     'system.ini, vcache,, "MaxFileCache=65535"', "",
     "[W98FR_Base.AddReg]",
     'HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run","W98FR",,"command.com /c %10%\\W98FRGO.BAT"',
     # pas de fenetre "Saisie du mot de passe Windows" (comme l'UBCD)
     'HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Network\\Real Mode Net","autologon",1,00',
     f'HKLM,"{K}","W98FRTop",,"W98FRTop"', f'HKLM,"{K}\\W98FRTop",INF,,"w98frpk.inf"',
     f'HKLM,"{K}\\W98FRTop",Section,,"W98FRTop"', f'HKLM,"{K}\\W98FRTop",Installed,,"0"']
for c, _, _ in COMPOSANTS:
    s = f"W98FR_{c}"
    t += [f'HKLM,"{K}","{s}",,"{s}"', f'HKLM,"{K}\\{s}",INF,,"w98frpk.inf"',
          f'HKLM,"{K}\\{s}",Section,,"{s}"', f'HKLM,"{K}\\{s}",Installed,,"0"']
t += ["", "[Optional Components]", "W98FRTop"] + [f"W98FR_{c}" for c, _, _ in COMPOSANTS]
t += ["", "[W98FRTop]", "OptionDesc  = %W98FRTop_DESC%", "Tip         = %W98FRTop_TIP%", "IconIndex   = 4"]
for c, _, _ in COMPOSANTS:
    s = f"W98FR_{c}"
    t += ["", f"[{s}]", f"OptionDesc  = %{s}_DESC%", f"Tip         = %{s}_TIP%", "Parent      = W98FRTop",
          f"AddReg      = {s}.oui", "InstallType = 14", "IconIndex   = 4", f"Uninstall   = {s}.non",
          "", f"[{s}.oui]", f'HKLM,"SOFTWARE\\Win98FR\\Choix","{c}",,"O"', f'HKLM,"{K}\\{s}",Installed,,"1"',
          "", f"[{s}.non]", f"DelReg      = {s}.del", f"AddReg      = {s}.non.reg",
          "", f"[{s}.del]", f'HKLM,"SOFTWARE\\Win98FR\\Choix","{c}"',
          "", f"[{s}.non.reg]", f'HKLM,"{K}\\{s}",Installed,,"0"']
t += ["", "[Strings]", 'W98FRTop_DESC = "Pack Windows 98 FR"',
      'W98FRTop_TIP = "Mises à jour et outils du pack Win98FR, installés au premier démarrage depuis le CD."']
for c, nom, tip in COMPOSANTS:
    t += [f'W98FR_{c}_DESC = "{nom}"', f'W98FR_{c}_TIP = "{tip}"']
(out / "W98FRPK.INF").write_bytes(("\r\n".join(t) + "\r\n").encode("cp1252"))

# Lanceur du premier demarrage : cherche le CD (W98FRCD.BAT a la racine, pack a cote de WIN98).
# Ne fait plus rien une fois le pack lance (INSTALL.BAT remplace Run\W98FR par GO.BAT).
g = ["@echo off", "REM Pack Win98FR : lancement au premier demarrage (cree par W98FRPK.INF)",
     "if exist C:\\W98FR\\GO.BAT goto FIN", "set N=", ":CHERCHE", "set W98CD=",
     "for %%d in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do if exist %%d:\\W98FRCD.BAT set W98CD=%%d",
     'if not "%W98CD%"=="" goto LANCER', "set N=%N%x", 'if "%N%"=="xxxxxxxxxxxx" goto ECHEC',
     "echo Recherche du CD Windows 98 FR (W98FRCD.BAT)...", "choice /C:O /N /T:O,5 > NUL", "goto CHERCHE",
     ":LANCER", "%W98CD%:", "cd \\", "call W98FRCD.BAT", "goto FIN", ":ECHEC",
     "echo CD introuvable : inserez le CD puis lancez W98FRCD.BAT depuis le CD.", "pause",
     ":FIN", "set N=", "set W98CD="]
(out / "W98FRGO.BAT").write_bytes(("\r\n".join(g) + "\r\n").encode("cp1252"))

# CHOIX.VBS (racine du CD) : cases cochees -> C:\W98FR\CHOIX.BAT (W98AUTO=1, C_<code>=O)
v = ["' ISO Win98FR : composants du pack coches pendant l'installation de Windows",
     "' (W98FRPK.INF, HKLM\\Software\\Win98FR\\Choix) -> C:\\W98FR\\CHOIX.BAT",
     "' Genere par _construction_iso\\make_composants.py", "On Error Resume Next",
     'Set S = CreateObject("WScript.Shell")', 'Set F = CreateObject("Scripting.FileSystemObject")',
     'If Not F.FolderExists("C:\\W98FR") Then F.CreateFolder "C:\\W98FR"',
     'Set B = F.CreateTextFile("C:\\W98FR\\CHOIX.BAT", True)', 'B.WriteLine "set W98AUTO=1"',
     "' toujours installes (mises a jour de composants systeme)"]
v += [f'B.WriteLine "set C_{c}=O"' for c in TOUJOURS]
v += ['Set J = F.OpenTextFile("C:\\W98FR\\JOURNAL.TXT", 8, True)', f'M = "Choix : {" ".join(TOUJOURS)} (d\'office)"',
      "For Each C In Array(%s)" % ", ".join(f'"{c}"' for c, _, _ in COMPOSANTS), "  Err.Clear",
      '  V = S.RegRead("HKLM\\Software\\Win98FR\\Choix\\" & C)', '  If Err.Number = 0 And V = "O" Then',
      '    B.WriteLine "set C_" & C & "=O"', '    M = M & " " & C', "  End If", "Next", "B.Close",
      "J.WriteLine M", "J.Close"]
(out / "CHOIX.VBS").write_bytes(("\r\n".join(v) + "\r\n").encode("cp1252"))
print(len(COMPOSANTS), "composants")
