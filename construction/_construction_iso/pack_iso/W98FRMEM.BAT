@echo off
REM ISO Win98FR : lance par W98FRDOS.BAT avec COMMAND /F (erreur disque = Echec
REM sans question). Si C: est formate et sans Windows, prepare
REM C:\WINDOWS\SYSTEM.INI avec la limite de memoire de l'UBCD (512 Mo).
if not exist C:\NUL goto FIN
if exist C:\WINDOWS\WIN.COM goto FIN
if exist C:\WINDOWS\SYSTEM.INI goto FIN
if not exist C:\WINDOWS\NUL md C:\WINDOWS
if not exist C:\WINDOWS\NUL goto FIN
echo [boot]> C:\WINDOWS\SYSTEM.INI
echo.>> C:\WINDOWS\SYSTEM.INI
echo [keyboard]>> C:\WINDOWS\SYSTEM.INI
echo.>> C:\WINDOWS\SYSTEM.INI
echo [boot.description]>> C:\WINDOWS\SYSTEM.INI
echo.>> C:\WINDOWS\SYSTEM.INI
echo [386Enh]>> C:\WINDOWS\SYSTEM.INI
echo MaxPhysPage=20000>> C:\WINDOWS\SYSTEM.INI
echo.>> C:\WINDOWS\SYSTEM.INI
echo [vcache]>> C:\WINDOWS\SYSTEM.INI
echo MaxFileCache=65535>> C:\WINDOWS\SYSTEM.INI
echo  Memoire limitee a 512 Mo pendant l'installation (retiree par PATCHMEM).
:FIN
