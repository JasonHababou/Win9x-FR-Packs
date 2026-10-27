@echo off
REM KEXCHK.BAT - appele par PLUS.BAT depuis un dossier applis : installe
REM KernelEx 4.5.2019.24 FR s'il est absent (Firefox et VLC en ont besoin).
if "%KEX%"=="oui" goto FIN
echo   - KernelEx 4.5.2019.24 FR absent : installation...
start /w ..\kernelex\KEX2019.EXE /S
start /w REGEDIT /s ..\kernelex\KEXOFF.REG
set KEX=oui
set REBOOT=oui
:FIN
