@echo off
REM  Pack Win98FR / WinMeFR : DAEMON Tools 3.47 installe au demarrage suivant,
REM  quand les 2 essais du pack ont echoue (cle RunOnce, DTRETRY.REG).
REM  %1 = dossier du pack sur le disque (C:\W98FR ou C:\WMEFR)
echo.
echo  Installation de DAEMON Tools 3.47 (nouvel essai apres redemarrage)...
C:
cd %1\DAEMON
start /w %WINDIR%\SYSTEM\MSIEXEC.EXE /i DAEMON.MSI /qb REBOOT=ReallySuppress
if not exist C:\PROGRA~1\D-TOOLS\DAEMON.EXE goto ECHEC
echo DAEMON Tools : installe au demarrage suivant>> %1\JOURNAL.TXT
del DAEMON.MSI
goto FIN
:ECHEC
echo DAEMON Tools : echec au demarrage suivant>> %1\JOURNAL.TXT
echo.
echo  DAEMON Tools n'a pas pu s'installer. Pour reessayer plus tard,
echo  ouvrez %1\DAEMON\DAEMON.MSI
pause
:FIN
