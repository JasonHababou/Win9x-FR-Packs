@ECHO OFF
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
