@echo off
REM ============================================================
REM  PLUS.BAT - Pack 2 Win98FR_Plus : logiciels, jeux et outils de
REM  test. A lancer APRES l'installation de base (pack 1) ET des
REM  pilotes (Puzzle Collection et 3DMark exigent 256 couleurs ou
REM  plus). Sans redemarrage automatique : une question par element.
REM  Firefox et VLC exigent KernelEx : installe ici s'il manque.
REM  DirectX, MS Agent et les outils systeme (MMC, RegClean, SharedDLLs)
REM  sont ici, pour le pack 1 comme pour l'ISO Win98FR.
REM  DirectX passe en premier : les 3DMark et les jeux en dependent.
REM ============================================================
if not exist PLUS.BAT goto PASDOS
set REBOOT=non
set KEX=non
if exist %WINDIR%\KERNELEX\KERNELEX.DLL set KEX=oui
cls
echo.
echo  Win98FR - Pack 2 : logiciels, jeux et outils de test
echo  Repondez O ou N a chaque question.
echo.
cd applis\directx
echo   DirectX : Windows 98 SE a DirectX 6.1 d'origine, la plupart des jeux
echo   exigent DirectX 8 ou 9. Une seule version : DirectX ne revient jamais
echo   en arriere. 9.0c conseille ; 8.1 ou 8.2 pour les jeux qui buguent
echo   avec DirectX 9 (certains jeux Cryo : Egypte, Ubik...).
echo   1 = ne rien installer (deja installe)
echo   2 = DirectX 8.1     3 = DirectX 8.2     4 = DirectX 9.0c (decembre 2006)
choice /C:1234 /N "Votre choix [1-4] : "
if errorlevel 4 goto DX9O
if errorlevel 3 goto DX82
if errorlevel 2 goto DX81
goto NODX
:DX81
cd dx81
goto DXSET
:DX82
cd dx82
:DXSET
echo   Installation de DirectX, patientez...
start /w DXSETUP.EXE /silent
cd ..
goto DXOK
:DX9O
cd dx90c
echo   Installation de DirectX 9.0c, patientez...
start /w DXSETUP.EXE /silent
cd ..
:DXOK
set REBOOT=oui
:NODX
cd ..\msagent
choice /C:ON /N "MS Agent 2.0 + langue francaise (personnages animes) ? [O,N] "
if errorlevel 2 goto NOAGENT
call msagent_install.bat
set REBOOT=oui
:NOAGENT
cd ..\firefox
choice /C:ON /N "Firefox 31.8 ESR portable en francais (KernelEx) ? [O,N] "
if errorlevel 2 goto NOFF
call ..\..\KEXCHK.BAT
echo   Decompression de Firefox dans C:\FIREFOX, patientez...
..\outils\7Z.EXE x -y -oC:\FIREFOX FIREFOX.7Z > NUL
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\FIREFOX.INF,DefaultInstall
:NOFF
cd ..\vlc
choice /C:ON /N "VLC 3.0.24 FR (video, via KernelEx, experimental) ? [O,N] "
if errorlevel 2 goto NOVLC
call ..\..\KEXCHK.BAT
echo   Decompression de VLC (130 Mo), patientez...
if not exist C:\PROGRA~1\VIDEOLAN\NUL md C:\PROGRA~1\VIDEOLAN
..\outils\7Z.EXE x -y -oC:\PROGRA~1\VIDEOLAN\VLC VLC.7Z > NUL
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\VLC.INF,DefaultInstall
start /w REGEDIT /s VLCKEX.REG
:NOVLC
cd ..\winrar
choice /C:ON /N "WinRAR 3.93 FR (shareware, essai 40 jours) ? [O,N] "
if errorlevel 2 goto NORAR
start /w WRAR393F.EXE /s
if exist C:\PROGRA~1\WINRAR\VODELI~1.HTM del C:\PROGRA~1\WINRAR\VODELI~1.HTM
:NORAR
cd ..\imgburn
choice /C:ON /N "ImgBurn 2.5.8.0 (gravure, francais) ? [O,N] "
if errorlevel 2 goto NOIMG
start /w IMGBURN.EXE /S
if not exist C:\PROGRA~1\IMGBURN\LANGUA~1\NUL md "C:\Program Files\ImgBurn\Languages"
copy FRENCH.LNG "C:\Program Files\ImgBurn\Languages" > NUL
:NOIMG
cd ..\aida32
choice /C:ON /N "AIDA32 3.93 (informations systeme) ? [O,N] "
if errorlevel 2 goto NOAIDA
start /w AIDA393.EXE /VERYSILENT /SP-
:NOAIDA
cd ..\cpuz
choice /C:ON /N "CPU-Z 1.78 (processeur, carte mere, memoire) ? [O,N] "
if errorlevel 2 goto NOCPUZ
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\CPUZ.INF,DefaultInstall
:NOCPUZ
cd ..\winamp
echo.
echo   Winamp : S = 5.2 Standard (anglais, mediatheque, video)
echo            F = 5.2 Full (anglais, + extraction et gravure de CD)
echo            A = 2.91 en francais (leger)      N = aucun
choice /C:SFAN /N "Votre choix [S,F,A,N] : "
if errorlevel 4 goto NOWAMP
if errorlevel 3 goto WAMP291
if errorlevel 2 goto WAMPFUL
start /w WA52STD.EXE /S
goto NOWAMP
:WAMPFUL
start /w WA52FULL.EXE /S
goto NOWAMP
:WAMP291
start /w WINAMP29.EXE /S
echo.
echo   Winamp s'ouvre a la fin de son installation : repondez a sa
echo   question puis FERMEZ Winamp avant de continuer (le patch
echo   francais doit remplacer ses fichiers).
pause
start /w WAMPFR.EXE /S
:NOWAMP
cd ..\xnview
choice /C:ON /N "XnView 1.80 (images, francais) ? [O,N] "
if errorlevel 2 goto NOXNV
start /w XNVIEW18.EXE /VERYSILENT /SP-
:NOXNV
cd ..\foxit
choice /C:ON /N "Foxit Reader 1.3 (PDF, en anglais) ? [O,N] "
if errorlevel 2 goto NOFOXIT
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\FOXIT.INF,DefaultInstall
:NOFOXIT
cd ..\klcodec
choice /C:ON /N "K-Lite Codec Pack 3.4.5 (codecs + Media Player Classic) ? [O,N] "
if errorlevel 2 goto NOKLCP
start /w KLCP345F.EXE /VERYSILENT /SP- /NORESTART
:NOKLCP
cd ..\jeux
choice /C:ON /N "Jeux : Hover! (FR), SkiFree et Echecs (EN) ? [O,N] "
if errorlevel 2 goto NOJEUX
..\outils\7Z.EXE x -y -oC:\JEUX JEUX.7Z > NUL
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\JEUX.INF,DefaultInstall
:NOJEUX
cd ..\puzzle
choice /C:ON /N "Microsoft Puzzle Collection (10 jeux, francais) ? [O,N] "
if errorlevel 2 goto NOPUZZ
..\outils\7Z.EXE x -y -oC:\JEUX PUZZLE.7Z > NUL
start /w REGEDIT /s PUZZLE.REG
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\PUZZLE.INF,DefaultInstall
:NOPUZZ
cd ..\systeme
echo.
echo   Outils systeme (en anglais) :
choice /C:ON /N "Console MMC 1.2 (EN) ? [O,N] "
if errorlevel 2 goto NOMMC
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\MMC.INF,DefaultInstall
:NOMMC
choice /C:ON /N "RegClean (EN, relisez toujours son rapport) ? [O,N] "
if errorlevel 2 goto NOREGCL
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\REGCLEAN.INF,DefaultInstall
:NOREGCL
choice /C:ON /N "Outil SharedDLLs (EN) ? [O,N] "
if errorlevel 2 goto NOSHDLL
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SHAREDLL.INF,DefaultInstall
:NOSHDLL
cd ..\bench
echo.
echo   Outils de test (installations guidees, a valider a l'ecran).
echo   Les cles (publiees par UL) s'ouvrent dans le Bloc-notes : copiez-les.
copy CLES.TXT %WINDIR%\BENCH_CLES.TXT > NUL
set CLES=non
choice /C:ON /N "3DMark99 Max (DirectX 6) ? [O,N] "
if errorlevel 2 goto NO3DM99
if "%CLES%"=="non" start notepad %WINDIR%\BENCH_CLES.TXT
set CLES=oui
echo   Nom : Futuremark   Cle : 78TR2-8DBDU-BMXXS
start /w 3DM99.EXE
:NO3DM99
choice /C:ON /N "3DMark2000 (DirectX 7) ? [O,N] "
if errorlevel 2 goto NO3DM00
if "%CLES%"=="non" start notepad %WINDIR%\BENCH_CLES.TXT
set CLES=oui
echo   Nom : Futuremark   Cle : 6VZTY-SDZ75-KA9V7
start /w 3DM2000.EXE
:NO3DM00
choice /C:ON /N "3DMark2001 SE (DirectX 8) ? [O,N] "
if errorlevel 2 goto NO3DM01
if "%CLES%"=="non" start notepad %WINDIR%\BENCH_CLES.TXT
set CLES=oui
echo   Cle : 7QMF2-TSLJR-ESRDD-L3FJF
start /w 3DM2001.EXE
:NO3DM01
choice /C:ON /N "3DMark03 3.4.0 (exige DirectX 9.0b ou 9.0c) ? [O,N] "
if errorlevel 2 goto NO3DM03
if "%CLES%"=="non" start notepad %WINDIR%\BENCH_CLES.TXT
set CLES=oui
echo   Cle : N4LWE-T6HUX-8U4JB-28YLV
start /w 3DM03.EXE
:NO3DM03
cd ..\..
cls
echo.
echo  Pack 2 termine.
if "%REBOOT%"=="non" goto FIN
echo  Redemarrage necessaire (DirectX, MS Agent ou KernelEx).
choice /C:ON /N "Redemarrer maintenant ? [O,N] "
if errorlevel 2 goto FIN
start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 2
goto FIN
:PASDOS
echo Lancez PLUS.BAT depuis son dossier (double-clic dans l'Explorateur).
pause
:FIN
