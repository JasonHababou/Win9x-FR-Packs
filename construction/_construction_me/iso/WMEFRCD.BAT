@echo off
REM ISO WinMeFR : premier demarrage de Windows Me. Lance par la valeur Run
REM "WMEFR" que pose MSBATCH.INF ([Install]), avec la lettre du CD en parametre
REM (retentee a chaque ouverture de session tant que le CD n'est pas trouve).
REM Le pack est a la racine du CD (a cote de WIN9X) : INSTALL.BAT affiche son
REM menu (T = tout installer) puis reprend tout seul apres chaque redemarrage.
%1:
cd \
REM Valeur effacee avant le pack : quitter son menu ne le relance plus ensuite
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection %1:\01_BASE\FINRUN.INF,DefaultInstall
call INSTALL.BAT
