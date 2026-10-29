@echo off
REM ============================================================
REM  Pack Windows Me FR (WinMeFR) - installation maitre
REM  Version 2026-10-25 : meme mecanique que le pack Win98FR v3
REM  (etapes, reprise automatique, mode ISO), contenu propre a ME.
REM
REM  Lancement : AUTORUN.EXE (CD) ou double-clic sur INSTALL.BAT (le
REM  dossier courant doit etre la racine du pack). Ensuite tout est
REM  automatique : redemarrages et reprise (cle Run puis C:\WMEFR\GO.BAT).
REM
REM  REGLES COMMAND.COM respectees : pas de tilde-dp0, else, parentheses,
REM  redirection 2, FOR /F, SET /P, CALL :etiquette ; "start /w" devant
REM  les programmes Windows ; etiquettes uniques sur 8 caracteres ;
REM  lignes de moins de 127 caracteres ; INF lances par ".\NOM.INF".
REM  Pas de signe "plus grand que" dans un REM (COMMAND.COM le prend
REM  pour une redirection).
REM
REM  Dossier de travail : C:\WMEFR (marqueurs, GO.BAT, journal, BAK).
REM ============================================================

if "%WMEENV%"=="1" goto DEBUT
set WMEENV=1
%COMSPEC% /e:4096 /c INSTALL.BAT
set WMEENV=
exit

:DEBUT
if not exist C:\WMEFR\NUL md C:\WMEFR
if not exist C:\WMEFR\BAK\NUL md C:\WMEFR\BAK
REM ISO WinMeFR : composants coches pendant l'installation de Windows
if exist C:\WMEFR\CHOIX.BAT call C:\WMEFR\CHOIX.BAT
echo install.bat : lancement>> C:\WMEFR\JOURNAL.TXT

REM --- Verrou : une seule fenetre d'installation a la fois ---
if not exist C:\WMEFR\ENCOURS.TXT goto VERROU
echo install.bat : verrou deja present>> C:\WMEFR\JOURNAL.TXT
cls
echo.
echo  Une autre fenetre d'installation semble deja ouverte,
echo  ou la precedente a ete interrompue (redemarrage force).
echo.
if "%WMEAUTO%"=="1" goto VERROU
choice /C:ON /N "Continuer dans cette fenetre ? [O,N] "
if errorlevel 2 goto FINDEJA
:VERROU
echo.> C:\WMEFR\ENCOURS.TXT
set EXTRAS=non
if exist C:\WMEFR\EXTRAS.TXT set EXTRAS=oui

REM --- Reprise : C:\WMEFR\ETx.TXT designe l'etape a (re)lancer ---
set RSTEP=
if exist C:\WMEFR\ET1.TXT set RSTEP=ST1
if exist C:\WMEFR\ET2.TXT set RSTEP=ST2
if exist C:\WMEFR\ET3.TXT set RSTEP=ST3
if exist C:\WMEFR\ET4.TXT set RSTEP=ST4
if exist C:\WMEFR\ET5.TXT set RSTEP=ST5
if exist C:\WMEFR\ET6.TXT set RSTEP=ST6
if exist C:\WMEFR\ET7.TXT set RSTEP=ST7
if exist C:\WMEFR\ET8.TXT set RSTEP=ST8
if "%RSTEP%"=="" goto MENU
if not exist C:\WMEFR\GO.BAT goto INITGO
cls
echo.
echo  Reprise de l'installation du pack Windows Me FR.
echo  Reprise automatique dans 10 secondes.
echo.
if "%WMEAUTO%"=="1" goto %RSTEP%
choice /C:CA /N /T:C,10 "C = continuer, A = abandonner l'installation : "
if errorlevel 2 goto ABANDON
goto %RSTEP%

:MENU
if "%WMEAUTO%"=="1" goto MODET
cls
echo.
echo            PACK WINDOWS ME FR - INSTALLATION
echo.
echo  Fermez tous les programmes avant de continuer.
echo  Windows redemarrera 4 fois ; l'installation reprend toute seule.
echo  Si un installeur propose de redemarrer, repondez NON :
echo  c'est ce script qui redemarre au bon moment.
echo.
echo  T = Tout installer (recommande)
echo  E = Essentiel seulement (systeme + securite, sans extras)
echo  R = Reprendre a une etape precise (apres un incident)
echo  Q = Quitter
echo.
choice /C:TERQ /N "Votre choix : "
if errorlevel 4 goto FIN
if errorlevel 3 goto MENUR
if errorlevel 2 goto MODEE
goto MODET

:MENUR
echo.
echo   1 = [1/8] CAB du CD, IE6 SP1, WMP9    2 = [2/8] correctifs, MDAC, Me SP
echo   3 = [3/8] systeme                     4 = [4/8] extras
echo   5 = [5/8] .NET 1.1                    6 = [6/8] chipset
echo   7 = [7/8] applications                8 = [8/8] fin, mode MS-DOS
echo.
choice /C:12345678 /N "Reprendre a l'etape : "
if errorlevel 1 set RSTEP=ST1
if errorlevel 2 set RSTEP=ST2
if errorlevel 3 set RSTEP=ST3
if errorlevel 4 set RSTEP=ST4
if errorlevel 5 set RSTEP=ST5
if errorlevel 6 set RSTEP=ST6
if errorlevel 7 set RSTEP=ST7
if errorlevel 8 set RSTEP=ST8
echo.
choice /C:TE /N "Mode : T = Tout, E = Essentiel : "
if errorlevel 2 goto MODEE

:MODET
echo.> C:\WMEFR\EXTRAS.TXT
set EXTRAS=oui
goto INITGO
:MODEE
if exist C:\WMEFR\EXTRAS.TXT del C:\WMEFR\EXTRAS.TXT
set EXTRAS=non

REM --- Memorise le dossier du pack et prepare la reprise auto
REM     (PROMPT ecrit lettre de lecteur et dossier courant dans un .bat) ---
:INITGO
cd 03_SYST
echo @prompt set WMEDRV=$n:$_set WMESUB=$p$_> C:\WMEFR\P1.BAT
%COMSPEC% /e:2048 /c C:\WMEFR\P1.BAT > C:\WMEFR\P2.BAT
call C:\WMEFR\P2.BAT
del C:\WMEFR\P1.BAT
del C:\WMEFR\P2.BAT
cd ..
if "%WMESUB%"=="" goto NOGO
REM --- GO.BAT (cle Run a chaque demarrage tant que ce n'est pas fini) :
REM     ne fait rien sans etape en cours, attend jusqu'a 60 s le pack ---
set G=C:\WMEFR\GO.BAT
echo @echo off> %G%
echo if not exist C:\WMEFR\ET*.TXT goto FIN>> %G%
echo set N=>> %G%
echo :ATTENDRE>> %G%
echo if exist "%WMESUB%\CABS.VBS" goto LANCER>> %G%
echo set N=%%N%%x>> %G%
echo if "%%N%%"=="xxxxxxxxxxxx" goto ECHEC>> %G%
echo choice /C:X /N /T:X,5 "Attente du dossier du pack... ">> %G%
echo goto ATTENDRE>> %G%
echo :LANCER>> %G%
REM  WMEDRV/WMESUB aussi pour la reprise (etape 8 : retour au pack apres le mode
REM  MS-DOS ; vides, FINRUN.INF etait cherche dans C:\WMEFR\DOS, test 2026-10-26)
echo set WMEDRV=%WMEDRV%>> %G%
echo set WMESUB=%WMESUB%>> %G%
echo %WMEDRV%>> %G%
echo cd "%WMESUB%">> %G%
echo cd ..>> %G%
echo call INSTALL.BAT>> %G%
echo goto FIN>> %G%
echo :ECHEC>> %G%
echo echo Dossier du pack introuvable : %WMESUB%\..>> %G%
echo echo Inserez le CD ou relancez INSTALL.BAT, il reprendra au bon endroit.>> %G%
echo pause>> %G%
echo :FIN>> %G%
echo set N=>> %G%
set G=
echo Pack : %WMESUB%\..>> C:\WMEFR\JOURNAL.TXT
set R=C:\WMEFR\REPRISE.REG
echo REGEDIT4> %R%
echo.>> %R%
echo [HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run]>> %R%
echo "WMEFR"="command.com /c C:\\WMEFR\\GO.BAT">> %R%
set R=
start /w REGEDIT /s C:\WMEFR\REPRISE.REG
:NOGO
if not "%RSTEP%"=="" goto %RSTEP%

REM ============================================================
REM  [1/8] Fichiers du CD dans WINDOWS\OPTIONS\CABS (SourcePath),
REM  puis base Microsoft : IE6 SP1 FR + WMP9 FR
REM ============================================================
:ST1
echo Etape ST1 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET1.TXT
cls
echo.
echo [1/8] Fichiers du CD de Windows + Internet Explorer 6 SP1 + Media Player 9
echo.
echo   - Fichiers du CD dans C:\WINDOWS\OPTIONS\CABS (plus besoin du CD ensuite)
start /w CSCRIPT.EXE //NoLogo 03_SYST\CABS.VBS
cd 01_BASE\ie6sp1
echo   - Internet Explorer 6 SP1 FR
start /w IE6SETUP.EXE /Q:A /R:N /C:"ie6wzd /S:""#e"" /Q:A /R:N"
cd ..\wmp9
echo   - Windows Media Player 9 FR
start /w MPSETUP.EXE /Q:U /R:N
cd ..\..
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET2.TXT
goto RBOOT

REM ============================================================
REM  [2/8] Correctifs IE6 / WMP9, MDAC 2.8 SP1, puis Me SP 2.02 Beta 9 FR
REM  (RUNPOST sans ROOTSUPD/CRLUPD de 2007 ; fichiers WMP de WMP9 gardes)
REM ============================================================
:ST2
echo Etape ST2 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET2.TXT
cls
echo.
echo [2/8] Correctifs, MDAC 2.8 SP1 et Service Pack non officiel Me SP 2.02 FR
echo.
echo   Patientez, cela peut prendre plusieurs minutes.
cd 01_BASE\updates
echo   - Correctifs q828750 (IE6) et KB819639 (WMP9)
start /w Q828750.EXE /q:u /r:n
start /w KB819639.EXE /q:a /r:n
cd ..\mdac28
echo   - MDAC 2.8 SP1 FR
start /w MDAC_TYP.EXE /Q /C:"DASETUP /Q /N"
cd ..\..\02_MESP
echo   - Me SP 2.02 Beta 9 FR (mise a jour principale)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SPUPDATE.INF,DefaultInstall
cd ..
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET3.TXT
goto RBOOT

REM ============================================================
REM  [3/8] Systeme : certificats, KernelEx, WSH 5.7, fuseaux, USB 2.0
REM ============================================================
:ST3
echo Etape ST3 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET3.TXT
cls
echo.
echo [3/8] Systeme (certificats, KernelEx, scripts, fuseaux, USB 2.0)
echo.
echo   Si une fenetre propose de redemarrer, repondez NON.
echo.
cd 03_SYST\rootsupd
echo   - Certificats racine de septembre 2020 + certificats revoques
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\ROOTSUPD.INF,DefaultInstall
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\RVKROOTS.INF,DefaultInstall
cd ..\..\05_EXTRA\kernelex
echo   - KernelEx 4.5.2019.24 FR, desactive par defaut (a activer par programme)
start /w KernelEx-4.5.2019.24-FR.exe /S
start /w REGEDIT /s KEXOFF.REG
cd ..\wsh57
echo   - Windows Script 5.7 : JScript, VBScript
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\WSH57.INF,DefaultInstall
cd ..\..\06_OPTS
echo   - Fuseaux horaires a jour (noms FR, regles 2020)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TIMEZONE.INF,DefaultInstall
echo   - Extension TrueType pour les polices
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TTFEXT.INF,DefaultInstall
cd ..\05_EXTRA\usb2
echo   - USB 2.0 et cles USB (pilotes SweetLow, installes a la detection)
start /w CSCRIPT.EXE //NoLogo USB2.VBS
cd ..\..
if "%EXTRAS%"=="non" goto ST6

REM ============================================================
REM  [4/8] Extras
REM ============================================================
:ST4
echo Etape ST4 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET4.TXT
cls
echo.
echo [4/8] Extras
echo.
cd 05_EXTRA\ntfs
echo   - Lecteur NTFS (Paragon UFSD corrige par SweetLow, configurateur FR)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\PNTFS.INF,DefaultInstall
cd ..\taskbarshuffle
echo   - Taskbar Shuffle 2.5
start /w ts2.5_setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
cd ..\mspaintfilter
echo   - Filtres graphiques Paint + apercu d'image
start /w REGEDIT /s "install filter.reg"
copy *.FLT %WINDIR%\SYSTEM > NUL
cd ..\aspi
echo   - ASPI 4.71.2 (Adaptec)
start /w ASPIINST.EXE SILENT
cd ..\..

REM ============================================================
REM  [5/8] .NET Framework 1.1 (optionnel)
REM ============================================================
:ST5
echo Etape ST5 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET5.TXT
cls
echo.
echo [5/8] .NET Framework (optionnel)
echo.
if "%WMEAUTO%"=="1" if not "%C_NET11%"=="O" goto NONET11
if "%WMEAUTO%"=="1" goto OKNET11
choice /C:ON /N ".NET Framework 1.1 FR avec SP1 et KB886903 ? [O,N] "
if errorlevel 2 goto NONET11
:OKNET11
cd 08_NET\net11
echo   Patientez : 10 a 20 minutes au total.
echo   - Framework 1.1 (barre de progression, sans question)
start /w DOTNETFX.EXE /q:a /c:"install /qb"
echo   - Module de langue francais
start /w LANGPACK.EXE /q:a /c:"inst /qb"
echo   - Service Pack 1 (KB867460), sans fenetre, plusieurs minutes
start /w KB867460-X86.EXE /q
echo   - Correctif KB886903, sans fenetre
start /w KB886903-X86.EXE /q
REM  Precompilation NetFxUpdate (Postngen) retiree : sous 9x elle bloquait
REM  l'arret de Windows a chaque demarrage (tests QEMU et GX240, 2026-10-21)
echo   - Precompilation .NET (Postngen) retiree : elle bloquait l'arret
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\NOPOSTNG.INF,DefaultInstall
cd ..\..
:NONET11

REM ============================================================
REM  [6/8] Pilotes chipset : detection du pont hote PCI, paquet exact
REM  (Intel : aussi l'AGP sur GX240, sinon "acceleration AGP indisponible")
REM ============================================================
:ST6
echo Etape ST6 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET6.TXT
cls
echo.
echo [6/8] Pilotes chipset de la carte mere
echo.
echo   A la fin, si l'installeur du chipset propose de redemarrer,
echo   repondez NON : ce script redemarre juste apres, proprement.
echo.
if "%WMEAUTO%"=="1" if not "%C_CHIP%"=="O" goto FINCHIP
if "%WMEAUTO%"=="1" goto OKCHIP
choice /C:ON /N "Installer le pilote chipset de la carte mere ? [O,N] "
if errorlevel 2 goto FINCHIP
:OKCHIP
cd 09_CHIP
if exist C:\W98FR\CHIPSET.BAT del C:\W98FR\CHIPSET.BAT
if not exist C:\W98FR\NUL md C:\W98FR
start /w CSCRIPT.EXE //NoLogo DETECT_CHIPSET.VBS
set CHIPSET=INCONNU
if exist C:\W98FR\CHIPSET.BAT call C:\W98FR\CHIPSET.BAT
echo   Chipset detecte : %CHIPSET%
echo Etape ST6 : chipset detecte = %CHIPSET%>> C:\WMEFR\JOURNAL.TXT
echo.
if "%CHIPSET%"=="INTEL" goto CHINTEL
if "%CHIPSET%"=="VIA" goto CHVIA
if "%CHIPSET%"=="SIS" goto CHSIS
echo   Fabricant non reconnu : rien n'est installe.
echo Etape ST6 : fabricant non reconnu>> C:\WMEFR\JOURNAL.TXT
if "%WMEAUTO%"=="1" goto CHFIN
pause
goto CHFIN
:CHINTEL
if "%WMEAUTO%"=="1" goto CHI2
echo   A = Intel 3.20.1008 (440BX/LX/GX, 810, 815)
echo   B = Intel 6.3.0.1007 (serie 800 dont 845, puis 915/925)
echo   C = Intel Pentium a Pentium II uniquement
echo   N = ne rien installer
choice /C:ABCN /N "Votre choix : "
if errorlevel 4 echo Etape ST6 : Intel, aucun pilote choisi (N)>> C:\WMEFR\JOURNAL.TXT
if errorlevel 4 goto CHFIN
if errorlevel 3 goto CHI3
if errorlevel 2 goto CHI2
echo Etape ST6 : Intel 3.20.1008 lance>> C:\WMEFR\JOURNAL.TXT
cd intel\3201008
goto CHIINF
:CHI2
echo Etape ST6 : Intel 6.3.0.1007 lance>> C:\WMEFR\JOURNAL.TXT
cd intel\6301007
:CHIINF
start /w INFINST_ENU.EXE
echo Etape ST6 : installeur Intel termine>> C:\WMEFR\JOURNAL.TXT
cd ..\..
goto CHFIN
:CHI3
echo Etape ST6 : Intel Pentium a Pentium II lance>> C:\WMEFR\JOURNAL.TXT
cd intel\pentiumTo2
start /w SETUP.EXE
cd ..\..
goto CHFIN

:CHVIA
if "%WMEAUTO%"=="1" goto CHFIN
echo   A = VIA 4in1 4.35v (anciens : KT133, KT266)
echo   B = VIA Hyperion 4.56v (recents : KT400 et plus, P4X400 et plus)
echo   C = VIA vlatency (seulement si soucis son, USB ou IDE)
echo   N = ne rien installer
choice /C:ABCN /N "Votre choix : "
if errorlevel 4 echo Etape ST6 : VIA, aucun pilote choisi (N)>> C:\WMEFR\JOURNAL.TXT
if errorlevel 4 goto CHFIN
if errorlevel 3 goto CHV3
if errorlevel 2 goto CHV2
echo Etape ST6 : VIA 4in1 4.35v lance>> C:\WMEFR\JOURNAL.TXT
cd via\4in1_435v
start /w SETUP.EXE
cd ..\..
goto CHFIN
:CHV2
echo Etape ST6 : VIA Hyperion 4.56v lance>> C:\WMEFR\JOURNAL.TXT
cd via\hyperion
start /w VIAHyperion4in1456v.exe
cd ..\..
goto CHFIN
:CHV3
echo Etape ST6 : VIA vlatency lance>> C:\WMEFR\JOURNAL.TXT
cd via\vlatency
start /w vlatency_v020_beta21.exe
cd ..\..
goto CHFIN

:CHSIS
if "%WMEAUTO%"=="1" goto CHFIN
echo   A = SiS 530 (graphique integre SiS530)
echo   B = SiS 5597 et 5598 (graphique integre)
echo   C = SiS agp121 (AGP SiS 6xx et 7xx)
echo   D = SiS ide204a (IDE SiS 96x, 630, 730)
echo   N = ne rien installer
choice /C:ABCDN /N "Votre choix : "
if errorlevel 5 echo Etape ST6 : SiS, aucun pilote choisi (N)>> C:\WMEFR\JOURNAL.TXT
if errorlevel 5 goto CHFIN
if errorlevel 4 goto CHS4
if errorlevel 3 goto CHS3
if errorlevel 2 goto CHS2
echo Etape ST6 : SiS 530 lance>> C:\WMEFR\JOURNAL.TXT
cd sis\530_5598\530_108\Win98
start /w REGMOD.EXE
cd ..\..\..\..
goto CHFIN
:CHS2
echo Etape ST6 : SiS 5597/5598 lance>> C:\WMEFR\JOURNAL.TXT
cd sis\530_5598\5598_113\win98
start /w SETUP.EXE
cd ..\..\..\..
goto CHFIN
:CHS3
echo Etape ST6 : SiS agp121 lance>> C:\WMEFR\JOURNAL.TXT
cd sis\agp121
start /w SETUP.EXE
cd ..\..
goto CHFIN
:CHS4
echo Etape ST6 : SiS ide204a lance>> C:\WMEFR\JOURNAL.TXT
cd sis\ide204a
start /w SETUP.EXE
cd ..\..

:CHFIN
cd ..
if exist C:\W98FR\CHIPSET.BAT del C:\W98FR\CHIPSET.BAT
:FINCHIP
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET7.TXT
goto RBOOT

REM ============================================================
REM  [7/8] Applications (optionnel)
REM ============================================================
:ST7
echo Etape ST7 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET7.TXT
if "%EXTRAS%"=="non" goto ST8
cls
echo.
echo [7/8] Applications (optionnel)
echo.
cd 10_APPLI\vc2005
if "%WMEAUTO%"=="1" if not "%C_VC5%"=="O" goto NOVC5
if "%WMEAUTO%"=="1" goto OKVC5
choice /C:ON /N "Visual C++ 2005 (bibliotheques des programmes) ? [O,N] "
if errorlevel 2 goto NOVC5
:OKVC5
if not exist C:\WMEFR\VC5\NUL md C:\WMEFR\VC5
start /w VCREDIST.EXE /Q /T:C:\WMEFR\VC5 /C
if exist C:\WMEFR\VC5\VCREDI~3.EXE start /w C:\WMEFR\VC5\VCREDI~3.EXE /q:a /c:"msiexec /i vcredist.msi /qb"
deltree /y C:\WMEFR\VC5 > NUL
:NOVC5
cd ..\vc2008
if "%WMEAUTO%"=="1" if not "%C_VC8%"=="O" goto NOVC
if "%WMEAUTO%"=="1" goto OKVC8
choice /C:ON /N "Visual C++ 2008 pour 9x (exige KernelEx) ? [O,N] "
if errorlevel 2 goto NOVC
:OKVC8
start /w VC_R_9X.EXE /q:a /r:n
:NOVC
cd ..\qres
if "%WMEAUTO%"=="1" if not "%C_QRES%"=="O" goto NOQRES
if "%WMEAUTO%"=="1" goto OKQRES
choice /C:ON /N "Raccourci de jeu (affichage et carte son, QRes) ? [O,N] "
if errorlevel 2 goto NOQRES
:OKQRES
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\QRES.INF,DefaultInstall
start /w CSCRIPT.EXE //NoLogo LIENBUR.VBS
:NOQRES
cd ..\7zip
if "%WMEAUTO%"=="1" if not "%C_7Z%"=="O" goto NO7Z
if "%WMEAUTO%"=="1" goto OK7Z
choice /C:ON /N "7-Zip 9.20 (archives, interface francaise) ? [O,N] "
if errorlevel 2 goto NO7Z
:OK7Z
start /w 7Z920.EXE /S
:NO7Z
cd ..\daemon
if "%WMEAUTO%"=="1" if not "%C_DT%"=="O" goto NODT
if "%WMEAUTO%"=="1" goto OKDT
choice /C:ON /N "DAEMON Tools 3.47 (lecteur CD virtuel) ? [O,N] "
if errorlevel 2 goto NODT
:OKDT
start /w %WINDIR%\SYSTEM\MSIEXEC.EXE /i DAEMON.MSI /qb REBOOT=ReallySuppress
REM  Installation parfois annulee ("Device setup error 25057", 2 tests QEMU sur 4,
REM  27-28/10/2026) : un second essai la reussit souvent ; sinon ("driver conflicts",
REM  test du 29/10/2026), nouvel essai au demarrage suivant (DTRETRY.BAT, RunOnce)
if exist C:\PROGRA~1\D-TOOLS\DAEMON.EXE goto DAEMONOK
echo DAEMON Tools : second essai>> C:\WMEFR\JOURNAL.TXT
start /w %WINDIR%\SYSTEM\MSIEXEC.EXE /i DAEMON.MSI /qb REBOOT=ReallySuppress
if exist C:\PROGRA~1\D-TOOLS\DAEMON.EXE goto DAEMONOK
echo DAEMON Tools : nouvel essai au prochain demarrage>> C:\WMEFR\JOURNAL.TXT
echo   - DAEMON Tools : nouvel essai au prochain demarrage de Windows
if not exist C:\WMEFR\DAEMON\NUL md C:\WMEFR\DAEMON
copy DAEMON.MSI C:\WMEFR\DAEMON > NUL
copy DTRETRY.BAT C:\WMEFR\DAEMON > NUL
start /w REGEDIT /s DTRETRY.REG
:DAEMONOK
start /w REGEDIT /s DAEMON.REG
:NODT
cd ..\retrozil
if "%WMEAUTO%"=="1" if not "%C_RZ%"=="O" goto NORZ
if "%WMEAUTO%"=="1" goto OKRZ
choice /C:ON /N "RetroZilla 2.3 (navigateur web par defaut) ? [O,N] "
if errorlevel 2 goto NORZ
:OKRZ
start /w RZ23.EXE -ms
start /w REGEDIT /s RETROZIL.REG
:NORZ
cd ..\tarot
if "%WMEAUTO%"=="1" if not "%C_TAROT%"=="O" goto NOTAROT
if "%WMEAUTO%"=="1" goto OKTAROT
choice /C:ON /N "Jeu de Tarot (Sybex, francais) ? [O,N] "
if errorlevel 2 goto NOTAROT
:OKTAROT
if not exist C:\JEUX\NUL md C:\JEUX
if not exist C:\JEUX\TAROT\NUL md C:\JEUX\TAROT
xcopy JEU\*.* C:\JEUX\TAROT /S /Y > NUL
if not exist %WINDIR%\SYSTEM\VB6DOCKOCX.OCX copy VB6DOCKOCX.OCX %WINDIR%\SYSTEM > NUL
start /w REGSVR32 /s %WINDIR%\SYSTEM\VB6DOCKOCX.OCX
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TAROT.INF,DefaultInstall
:NOTAROT
cd ..\fraps
if "%WMEAUTO%"=="1" if not "%C_FRAPS%"=="O" goto NOFRAPS
if "%WMEAUTO%"=="1" goto OKFRAPS
choice /C:ON /N "Fraps 1.9D (images par seconde dans les jeux) ? [O,N] "
if errorlevel 2 goto NOFRAPS
:OKFRAPS
start /w FRAPS19D.EXE /S
:NOFRAPS
cd ..\siv
if "%WMEAUTO%"=="1" if not "%C_SIV%"=="O" goto NOSIV
if "%WMEAUTO%"=="1" goto OKSIV
choice /C:ON /N "SIV, informations systeme (memoire, PCI, USB, capteurs) ? [O,N] "
if errorlevel 2 goto NOSIV
:OKSIV
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SIV.INF,DefaultInstall
:NOSIV
cd ..\..

REM ============================================================
REM  [8/8] Fin : PATCHMEM, DMA, correctif NVIDIA, puis mode MS-DOS FR
REM ============================================================
:ST8
echo Etape ST8 : debut>> C:\WMEFR\JOURNAL.TXT
del C:\WMEFR\ET*.TXT > NUL
echo.> C:\WMEFR\ET8.TXT
cls
echo.
echo [8/8] Correctif memoire PATCHMEM (RLoew)
echo.
echo   PATCHMEM est indispensable au-dela de 512 Mo de RAM.
echo.
if "%WMEAUTO%"=="1" if not "%C_PMEM%"=="O" goto NOPMEM
if "%WMEAUTO%"=="1" goto OKPMEM
choice /C:ON /N "Installer PATCHMEM maintenant ? [O,N] "
if errorlevel 2 goto NOPMEM
:OKPMEM
cd 03_SYST\rloew
echo Etape ST8 : PATCHMEM lance>> C:\WMEFR\JOURNAL.TXT
if "%WMEAUTO%"=="1" goto PMAUTO
PATCHMEM.EXE /I
goto PMFIN
:PMAUTO
PATCHMEM.EXE /I < OUI.TXT
:PMFIN
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SYSINI.INF,DefaultInstall
cd ..\..
:NOPMEM
cls
echo.
echo  DMA des disques et lecteurs IDE (transferts 2 a 3 fois plus rapides)
echo.
echo  Si Windows bloque ensuite au demarrage : touche Ctrl au demarrage,
echo  Mode sans echec, puis decocher DMA dans le Gestionnaire de
echo  peripheriques (disque, onglet Parametres).
echo.
if "%WMEAUTO%"=="1" if not "%C_DMA%"=="O" goto NODMA
if "%WMEAUTO%"=="1" goto OKDMA
choice /C:ON /N "Activer le DMA des disques et lecteurs IDE ? [O,N] "
if errorlevel 2 goto NODMA
:OKDMA
start /w CSCRIPT.EXE //NoLogo 09_CHIP\DMAON.VBS
:NODMA
if exist %WINDIR%\KERNELEX\KERNELEX.DLL start /w REGEDIT /s 05_EXTRA\kernelex\KEXOFF.REG
set NVMODE=/installe
if "%WMEAUTO%"=="1" if not "%C_NVSURV%"=="O" goto NVSANS
if "%WMEAUTO%"=="1" goto OKNVSURV
echo.
echo  Correctif d'arret NVIDIA (pilotes 81.x et 82.x) : le pack peut verifier
echo  a chaque demarrage si un tel pilote vient d'etre installe.
choice /C:ON /N "Surveiller l'installation d'un pilote NVIDIA ? [O,N] "
if errorlevel 2 goto NVSANS
:OKNVSURV
set NVMODE=/surveille
:NVSANS
echo Fin : NVFIX %NVMODE%>> C:\WMEFR\JOURNAL.TXT
start /w CSCRIPT.EXE //NoLogo 09_CHIP\nvidia\NVFIX.VBS %NVMODE%
set NVMODE=
if "%C_P9X%"=="O" call 03_SYST\patcher9x\P9X.BAT
cls
echo.
echo [8/8] Mode MS-DOS (vrai DOS, comme Windows 98)
echo.
echo   Redemarrer en mode MS-DOS, "Sortie de Dos" et les PIF des jeux DOS.
echo.
if "%WMEAUTO%"=="1" if not "%C_DOS%"=="O" goto NODOS
if "%WMEAUTO%"=="1" goto OKDOS
choice /C:ON /N "Installer le mode MS-DOS ? [O,N] "
if errorlevel 2 goto NODOS
:OKDOS
REM  dosmode corrige COMMAND.COM et REGENV32 dans SON dossier : copie sur C:
if not exist C:\WMEFR\DOS\NUL md C:\WMEFR\DOS
xcopy 11_DOS\*.* C:\WMEFR\DOS /Y > NUL
echo Etape ST8 : mode MS-DOS>> C:\WMEFR\JOURNAL.TXT
%WMEDRV%
C:
cd \WMEFR\DOS
call INSTALL.BAT
%WMEDRV%
cd "%WMESUB%"
cd ..
:NODOS
set APRES=FINMSG
goto NETTOY
:FINMSG
echo Fin : message final affiche>> C:\WMEFR\JOURNAL.TXT
cls
echo.
echo  Installation terminee !
echo  (originaux remplaces sauvegardes dans C:\WMEFR\BAK)
echo.
echo  Un redemarrage est necessaire pour finaliser.
echo.
echo  Ensuite, installez les pilotes (carte graphique, son...), puis
echo  lancez le pack 2 (CD Win9x_FR_Plus) : DirectX, logiciels, jeux.
echo.
if "%WMEAUTO%"=="1" goto OKRB1
choice /C:ON /N "Redemarrer maintenant ? [O,N] "
if errorlevel 2 goto FINMAN
:OKRB1
echo Fin : redemarrage demande>> C:\WMEFR\JOURNAL.TXT
if "%WMEAUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 6
if not "%WMEAUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 2
goto FIN
:FINMAN
echo.
echo  Pensez a redemarrer Windows vous-meme.
pause
goto FIN

REM ============================================================
REM  Redemarrage avec reprise automatique (cle Run puis GO.BAT)
REM ============================================================
:RBOOT
echo.
if "%C_P9X%"=="O" call 03_SYST\patcher9x\P9X.BAT
echo Redemarrage demande par le script>> C:\WMEFR\JOURNAL.TXT
if exist C:\WMEFR\REPRISE.REG start /w REGEDIT /s C:\WMEFR\REPRISE.REG
if exist C:\WMEFR\GO.BAT echo   Redemarrage necessaire : l'installation reprendra toute seule.
if not exist C:\WMEFR\GO.BAT echo   Redemarrage necessaire : relancez ensuite INSTALL.BAT.
if "%WMEAUTO%"=="1" goto OKRB2
choice /C:ON /N "Redemarrer maintenant ? [O,N] "
if errorlevel 2 goto RBMAN
:OKRB2
if "%WMEAUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 6
if not "%WMEAUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 2
goto FIN
:RBMAN
echo   Redemarrez quand vous voulez : la suite est deja programmee.
pause
goto FIN

REM ============================================================
REM  Abandon (choisi a la reprise) et nettoyage commun
REM ============================================================
:ABANDON
set APRES=FIN
echo   Installation abandonnee : la reprise automatique est annulee.
:NETTOY
del C:\WMEFR\ET*.TXT > NUL
if exist C:\WMEFR\GO.BAT del C:\WMEFR\GO.BAT
if exist C:\WMEFR\REPRISE.REG del C:\WMEFR\REPRISE.REG
if exist C:\WMEFR\EXTRAS.TXT del C:\WMEFR\EXTRAS.TXT
if exist C:\WMEFR\CHOIX.BAT del C:\WMEFR\CHOIX.BAT
if exist %WINDIR%\WMEFRGO.BAT del %WINDIR%\WMEFRGO.BAT
echo Nettoyage : suppression de la cle Run>> C:\WMEFR\JOURNAL.TXT
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\01_BASE\FINRUN.INF,DefaultInstall
goto %APRES%

:FIN
if exist C:\WMEFR\ENCOURS.TXT del C:\WMEFR\ENCOURS.TXT
exit
:FINDEJA
echo install.bat : arret, autre fenetre en cours>> C:\WMEFR\JOURNAL.TXT
exit
