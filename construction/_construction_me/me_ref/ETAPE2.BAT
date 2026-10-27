@echo off
REM Kit VM de reference QuickInstall ME (genere par make_me_ref.py)
REM Lancer depuis le CD (lettre D:) : Executer > D:\ETAPEn.BAT
D:
echo [2/3] Correctifs IE6 / WMP9, MDAC 2.8 SP1, Me SP 2.02 Beta 9 FR
cd \MAJ
start /w Q828750.EXE /q:u /r:n
start /w KB819639.EXE /q:a /r:n
cd \MDAC28
start /w MDAC_TYP.EXE /Q /C:"DASETUP /Q /N"
cd \MESP
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SPUPDATE.INF,DefaultInstall
echo Etape 2 terminee>> C:\MEREF.TXT
echo.
echo   Redemarrage...
start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 6
