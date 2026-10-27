@echo off
REM ============================================================
REM  Theme Windows 2000 - icones (ResHack) + couleurs (INF).
REM  Syntaxe COMMAND.COM. Appele par INSTALL.BAT APRES un "cd"
REM  dans ce dossier.
REM  Methode SP3.0 B4 FR reproduite : ResHack patche des COPIES
REM  dans C:\W98FR\W2K, puis W2KSHELL.INF installe ces copies
REM  (remplacement au prochain demarrage, fichiers en cours
REM  d'utilisation). Bases utilisees, toutes FR :
REM    - SHELL32.DLL  : Shell98 FR revise 2007 (systeme\)
REM    - EXPLORER.EXE : SP2.CAB de SP3.0 B4 FR (4.72.3612.1710)
REM    - MYDOCS.DLL   : SP2.CAB de SP3.0 B4 FR
REM  Doit passer APRES SHELL98.INF et NUSB.INF (meme session) :
REM  le dernier remplacement programme est celui qui s'applique.
REM ============================================================
set T=C:\W98FR\W2K
if not exist %T%\NUL md %T%
for %%F in (RESHACK.EXE W2KSHELL.INF W2K_EX.TXT W2K_MD.TXT W2K_SH.TXT) do copy %%F %T% > NUL
copy _*.ICO %T% > NUL
copy _*.AVI %T% > NUL
REM  Fonds d'ecran de la 3.66 (theme Windows Me/2000), Affichage, Arriere-plan.
REM  Icones 18/30/31 et bande bleue du menu Demarrer de la 3.66 ecartees (choix
REM  utilisateur 2026-10-17 : bande verte de 98 gardee, icones sans effet visible)
copy WINME.BMP "%WINDIR%\Windows Me.bmp" > NUL
copy WIN2000.BMP "%WINDIR%\Windows 2000.bmp" > NUL
copy PLUS98.BMP "%WINDIR%\Plus! 98.bmp" > NUL
copy BASE\EXPLORER.EXE %T% > NUL
copy BASE\MYDOCS.DLL %T% > NUL
copy ..\..\03_SYST\SHELL32.DLL %T% > NUL
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\w2kcolor.inf,DefaultInstall
start /w %T%\RESHACK.EXE -script %T%\W2K_EX.TXT
start /w %T%\RESHACK.EXE -script %T%\W2K_MD.TXT
start /w %T%\RESHACK.EXE -script %T%\W2K_SH.TXT
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection %T%\W2KSHELL.INF,DefaultInstall
set T=
