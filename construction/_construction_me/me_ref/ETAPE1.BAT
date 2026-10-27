@echo off
REM Kit VM de reference QuickInstall ME (genere par make_me_ref.py)
REM Lancer depuis le CD (lettre D:) : Executer > D:\ETAPEn.BAT
D:
echo [1/3] Internet Explorer 6 SP1 FR + Windows Media Player 9 FR
cd \IE6SP1
start /w IE6SETUP.EXE /Q:A /R:N /C:"ie6wzd /S:""#e"" /Q:A /R:N"
cd \WMP9
start /w MPSETUP.EXE /Q:U /R:N
echo Etape 1 terminee>> C:\MEREF.TXT
echo.
echo   Redemarrage...
start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 6
