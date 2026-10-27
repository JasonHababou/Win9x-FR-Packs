@echo off
REM ISO Win98FR : appele par la disquette de demarrage (AUTOEXEC.BAT, menu
REM "Demarrer l'installation de Windows 98 depuis le CD-ROM") a la place
REM d'OEMSETUP.EXE. Comme l'UBCD : prepare C:\WINDOWS\SYSTEM.INI avec une
REM limite de memoire (512 Mo) pour que l'installation passe sur un PC de
REM plus de 1 Go. Le SP3.0 la porte a 1 Go, PATCHMEM (pack) la retire.
REM Le test de C: est fait dans W98FRMEM.BAT, lance par COMMAND /F : quand C:
REM est partitionne mais pas encore formate, chaque acces a C: demandait
REM Abandon, Reprise, Echec (vu sous QEMU le 2026-10-18). /F repond Echec seul.
REM Disque pas encore prepare : le programme d'installation partitionne et
REM formate, la limite est alors posee par W98FRPK.INF pendant la copie.
%COMSPEC% /F /C %CDROM%\W98FRMEM.BAT
%CDROM%
cd \WIN98
OEMSETUP.EXE
