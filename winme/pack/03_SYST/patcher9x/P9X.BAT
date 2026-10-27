@echo off
REM patcher9x 0.9.91 (JHRobotics, licence MIT) : correctifs pour processeurs
REM recents (AMD Ryzen 3000 et plus, Intel Core 11e generation et plus) et
REM vitesse du processeur. Sans le correctif memoire (mem) : il bloquait le
REM SP3.0 (tests QEMU 2026-10-18) ; la memoire reste a PATCHMEM (03_SYST\rloew).
REM Appele par INSTALL.BAT avant chaque redemarrage et a la fin, en mode ISO :
REM le SP3.0 et la 3.66 posent un VMM.VXD non corrige. Deja corrige = rien.
REM Lance depuis la racine du pack, sur %WINDIR%\SYSTEM (avec %WINDIR% seul,
REM patcher9x refuse : "please choose Windows\system directory"). Reponses :
REM P9XREP.TXT = 2 (VMM32.VXD corrige directement, choix par defaut pour SYSTEM,
REM comme dans les CAB de l'ISO), Y, Entree. Tests QEMU 2026-10-18.
echo   - Correctif processeurs recents (patcher9x)
echo patcher9x : lance>> C:\W98FR\JOURNAL.TXT
03_SYST\patcher9x\PATCH9X.EXE -auto -unselect mem %WINDIR%\SYSTEM < 03_SYST\patcher9x\P9XREP.TXT >> C:\W98FR\JOURNAL.TXT
echo patcher9x : termine>> C:\W98FR\JOURNAL.TXT
