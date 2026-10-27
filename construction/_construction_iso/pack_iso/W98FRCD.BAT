@echo off
REM ISO Win98FR : premier demarrage. Lance par WINDOWS\W98FRGO.BAT depuis
REM la racine du CD (le pack y est, a cote de WIN98). Lit les composants coches pendant l'installation
REM de Windows (CHOIX.VBS ecrit C:\W98FR\CHOIX.BAT) puis lance le pack :
REM INSTALL.BAT repond alors tout seul a ses questions.
if not exist C:\W98FR\NUL md C:\W98FR
echo W98FRCD.BAT : lecture des composants coches>> C:\W98FR\JOURNAL.TXT
start /w CSCRIPT.EXE //NoLogo CHOIX.VBS
if not exist C:\W98FR\CHOIX.BAT echo   ATTENTION : choix introuvables, le pack posera ses questions.
call INSTALL.BAT
