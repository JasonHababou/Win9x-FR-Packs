@echo off
REM ISO WinMeFR : appele par la disquette de demarrage (menu "Installer Windows
REM Millennium Edition depuis le CD-ROM"), avec la lettre du CD en parametre.
REM L'installation de Me (WIN9X\INSTALL.EXE) ne partitionne ni ne formate : sur un
REM disque vierge elle s'arrete ("Impossible de creer un repertoire temporaire",
REM test QEMU 2026-10-26). On verifie donc C: avant, sans rien effacer sans accord :
REM  - pas de partition FAT : le disque virtuel en memoire a pris la lettre C
REM    (RAMD=C), FORMAT C: viserait ce disque virtuel : FDISK seulement ;
REM  (pas de signe "plus grand que" dans ces REM : COMMAND.COM y voit une
REM  redirection et ecrit sur A:, protegee en ecriture, test 2026-10-26)
REM  - partition pas formatee : test par WMEFRC.BAT sous COMMAND /F (sinon
REM    "Abandon, Reprise, Echec" sur chaque acces a C:, comme l'ISO 98).
if "%RAMD%"=="C" goto PARTITION
if exist %RAMD%:\COK.TXT del %RAMD%:\COK.TXT
%COMSPEC% /F /C %1:\WMEFRC.BAT %RAMD%
if exist %RAMD%:\COK.TXT goto INSTALLER

:FORMATER
cls
echo.
echo  Le disque C: a une partition, mais elle n'est pas encore formatee.
echo.
echo  F = formater C: maintenant (EFFACE tout ce qui serait sur C:)
echo  Q = quitter vers l'invite MS-DOS
echo.
%1:\CHOICE.COM /C:FQ /N "Votre choix : "
if errorlevel 2 goto FIN
FORMAT.COM C:
goto INSTALLER

:PARTITION
cls
echo.
echo  Aucune partition utilisable n'a ete trouvee sur le disque C:.
echo  Il faut d'abord la creer avec FDISK (repondez O pour utiliser tout le
echo  disque), puis redemarrer sur le CD et choisir de nouveau
echo  "Installer Windows Millennium Edition depuis le CD-ROM".
echo.
echo  P = lancer FDISK maintenant
echo  Q = quitter vers l'invite MS-DOS
echo.
%1:\CHOICE.COM /C:PQ /N "Votre choix : "
if errorlevel 2 goto FIN
A:\FDISK.EXE
echo.
echo  Redemarrez maintenant l'ordinateur sur le CD (Ctrl+Alt+Suppr).
goto FIN

:INSTALLER
%1:
cd \WIN9X
INSTALL.EXE %1:\WIN9X\MSBATCH.INF

:FIN
