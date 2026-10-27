# Mode MS-DOS pour Windows ME FR : prepare dosmode_fr\ a partir de TPC-WinMe-DOSMODE
# 0.9.1 (iMic / gpdm). Changements :
#  - WINBOOT.SY_ : IO.SYS FR des outils d'usine du CD ME FR (TOOLS\NETTOOLS\FAC\CBS.DTA,
#    winboot.lf), decompresse par IO8DCOMP (RLoew) ; message d'usine "Preparation du
#    demarrage de votre nouvel ordinateur" remplace par "Demarrage de Windows Millennium"
#    (meme longueur). Ce fichier est deja dans dosmode_fr\ (prepare a part).
#  - "Exit to DOS.pif" -> "Sortie de Dos.pif" : le SHELL32 de ME FR cherche ce nom.
#  - messages de l'installeur en francais ; INSTALL.BAT FR (attributs, KEYB FR, COUNTRY).
# Usage : make_dosmode_fr.py <dossier DOSMODE de TPC> <dosmode_fr> <pif_fr> <UIDE.SYS> <CTMOUSE.EXE> <KEYB.COM>
import shutil
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(exist_ok=True)
for f in src.iterdir():
    if f.is_file() and f.name.upper() != "WINBOOT.SY_" and f.name.upper() != "DOSMODE.INF":
        shutil.copy2(f, dst / f.name)
assert (dst / "WINBOOT.SY_").stat().st_size == 280064
t = (src / "DOSMODE.INF").read_bytes().decode("cp1252")
nl = "\r\n" if "\r\n" in t else "\n"
rempl = [
    ('"Exit to DOS.pif",EXIT_DOS.PI_,,4', '"Sortie de Dos.pif",EXIT_DOS.PI_,,4'),
    ('[Uninstall.Del.Windows]' + nl + '"Exit to DOS.pif"', '[Uninstall.Del.Windows]' + nl + '"Sortie de Dos.pif"'),
    ('UpdName="Windows Millennium Edition MS-DOS Mode Patch"', 'UpdName="Mode MS-DOS pour Windows Millennium"'),
    ('AdvPackWarn="You need a newer version of advpack.dll."',
     'AdvPackWarn="Une version plus recente de ADVPACK.DLL est necessaire."'),
    ('SrcDiskName="MS-DOS Mode Patch"', 'SrcDiskName="Mode MS-DOS pour Windows Millennium"'),
    ('BeginPromptInstall="[PRE-RELEASE BUILD] Install MS-DOS Mode support for Windows Millennium Edition?"',
     'BeginPromptInstall="Installer le mode MS-DOS (vrai DOS, comme Windows 98) pour Windows Millennium ?"'),
    ('BeginPromptUninstall="Remove MS-DOS Mode support for Windows Millennium Edition?"',
     'BeginPromptUninstall="Retirer le mode MS-DOS de Windows Millennium ?"'),
    ('"IO8EMMOK XMS Driver Wrapper"', '"IO8EMMOK : pilote XMS pour EMM386"'),
    ('"Allows EMM386 to operate with the Windows XMS driver included in IO.SYS."',
     '"Permet a EMM386 de fonctionner avec le pilote XMS integre a IO.SYS."'),
]
for o, n in rempl:
    assert t.count(o) == 1, o
    t = t.replace(o, n)

# Ajouts pack WinMeFR (tests QEMU 2026-10-20) :
#  - PIF FR (make_pif_dos_fr.py) : clavier AZERTY, CD-ROM, souris, EMS ;
#  - UIDE.SYS (CD-ROM sous EMM386 ; OAKCDROM bloquait), CTMOUSE.EXE (CuteMouse 2.1 FR,
#    GPL), KEYB.COM FR (ME n'en a pas, copie de la disquette de demarrage FR) ;
#  - KEYB FR dans AUTOEXEC.BAT : l'IO.SYS "vrai DOS" ne charge plus le clavier FR du
#    registre, les fenetres DOS de Windows etaient passees en QWERTY.
PIF = Path(sys.argv[3])
for f in ("EXIT_DOS.PI_", "JEUXXMS.PI_", "JEUXSANS.PI_"):
    shutil.copy2(PIF / f, dst / f)
for f in sys.argv[4:]:                               # UIDE.SYS, CTMOUSE.EXE, KEYB.COM
    shutil.copy2(f, dst / Path(f).name.upper())
ajouts = [
    ("[Install.Copy.Windows]" + nl,
     "[Install.Copy.Windows]" + nl + "UIDE.SYS,,,4" + nl + "CTMOUSE.EXE,,,4" + nl + "KEYB.COM,,,4" + nl
     + '"Mode MS-DOS pour jeux (XMS).pif",JEUXXMS.PI_,,4' + nl
     + '"Mode MS-DOS sans EMM386.pif",JEUXSANS.PI_,,4' + nl),
    ("[Uninstall.Del.Windows]" + nl,
     "[Uninstall.Del.Windows]" + nl + "UIDE.SYS" + nl + "CTMOUSE.EXE" + nl + "KEYB.COM" + nl
     + '"Mode MS-DOS pour jeux (XMS).pif"' + nl + '"Mode MS-DOS sans EMM386.pif"' + nl),
    ("COMMAND.CO_=55" + nl,
     "COMMAND.CO_=55" + nl + "UIDE.SYS=55" + nl + "CTMOUSE.EXE=55" + nl + "KEYB.COM=55" + nl
     + "JEUXXMS.PI_=55" + nl + "JEUXSANS.PI_=55" + nl),
]
for o, n in ajouts:
    assert t.count(o) == 1, o
    t = t.replace(o, n)
# ATTRIB lances par l'INF : la fenetre restait bloquee ("Pas de reinitialisation du
# fichier cache C:\command.com", test QEMU 2026-10-20) -> faits par INSTALL.BAT
for o in ("RunPreSetupCommands=RunCommands.PreSetup" + nl, "RunPostSetupCommands=RunCommands.PostSetup" + nl):
    assert t.count(o) == 2, o
    t = t.replace(o, "")
(dst / "DOSMODE.INF").write_bytes(t.encode("cp1252"))
bat = r"""@ECHO OFF
REM Mode MS-DOS (vrai DOS) pour Windows Millennium FR - pack WinMeFR
REM D'apres TPC-WinMe-DOSMODE 0.9.1 (iMic, gpdm) : COMMAND.COM et REGENV32.EXE
REM sont corriges sur place (langue conservee), puis DOSMODE.INF installe le reste.
ECHO Mode MS-DOS pour Windows Millennium : preparation...
copy %WINDIR%\COMMAND.COM > NUL
copy %WINDIR%\SYSTEM\REGENV32.EXE > NUL
REM REGENV32 : ecrit AUTOEXEC.WIN et CONFIG.WIN au lieu d'ecraser les vrais fichiers
GSAR -o -s:x43:x4F:x4E:x46:x49:x47:x2E:x53:x59:x53 -r:x43:x4F:x4E:x46:x49:x47:x2E:x57:x49:x4E regenv32.exe > NUL
GSAR -o -s:x41:x55:x54:x4F:x45:x58:x45:x43:x2E:x42:x41:x54 -r:x41:x55:x54:x4F:x45:x58:x45:x43:x2E:x57:x49:x4E regenv32.exe > NUL
REM COMMAND.COM : mode reel, et fichiers caches visibles dans les sous-dossiers
GSAR -o -s:x75:x10:xB8:x0E -r:xEB:x10:xB8:x0E command.com > NUL
GSAR -o -s:x03:x00:x75:x0B:x8B -r:x03:x00:xEB:x0B:x8B command.com > NUL
GSAR -o -s:x12:x8B:x16:x08 -r:x44:x8B:x16:x08 command.com > NUL
GSAR -o -s:xD4:xB9:x10:x00:xB4 -r:xD4:xB9:x16:x00:xB4 command.com > NUL
GSAR -o -s:xFC:xB9:x10:x00:xB4 -r:xFC:xB9:x16:x00:xB4 command.com > NUL
move /Y COMMAND.COM COMMAND.CO_ > NUL
move /Y REGENV32.EXE REGENV32.EX_ > NUL
REM Attributs des fichiers remplaces (avant, faits par l'INF : fenetre bloquee)
attrib -r -s -h C:\AUTOEXEC.BAT
attrib -r -s -h C:\CONFIG.SYS
attrib -r -s -h C:\IO.SYS
attrib -r -s -h C:\COMMAND.COM
attrib -r %WINDIR%\COMMAND.COM
REM Clavier AZERTY : l'IO.SYS "vrai DOS" ne charge plus le clavier FR du registre ;
REM AUTOEXEC.BAT est de nouveau lu au demarrage (comme sous Windows 98)
if not exist C:\AUTOEXEC.BAT echo @ECHO OFF> C:\AUTOEXEC.BAT
find /i "KEYB.COM" C:\AUTOEXEC.BAT > NUL
if errorlevel 1 echo C:\WINDOWS\KEYB.COM FR,,C:\WINDOWS\COMMAND\KEYBOARD.SYS>> C:\AUTOEXEC.BAT
if not exist C:\CONFIG.SYS echo REM> C:\CONFIG.SYS
find /i "COUNTRY=" C:\CONFIG.SYS > NUL
if errorlevel 1 echo COUNTRY=033,850,C:\WINDOWS\COMMAND\COUNTRY.SYS>> C:\CONFIG.SYS
ECHO Installation (DOSMODE.INF)...
REM  sans START /W : sinon cette fenetre DOS empeche le redemarrage demande par l'INF
RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection DOSMODE.INF,DefaultInstall
EXIT
"""
(dst / "INSTALL.BAT").write_bytes(bat.replace("\n", "\r\n").encode("cp1252"))
print("ok", len(list(dst.iterdir())), "fichiers")
