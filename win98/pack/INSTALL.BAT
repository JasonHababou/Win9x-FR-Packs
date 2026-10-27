@echo off
REM ============================================================
REM  Pack Windows 98 SE FR "ultime" - installation maitre
REM  Version 2026-10-13 (reecriture complete, COMMAND.COM pur)
REM  v3 (2026-10-17) : couche U98SESP3.66 filtree FR en [11/11]
REM
REM  Architecture v2 (2026-10-14) : un dossier par etape a la racine
REM  (01_BASE ... 10_APPLI), ce script a la racine du CD ou du dossier.
REM  Lancement : AUTORUN.EXE (CD) ou double-clic sur INSTALL.BAT (le
REM  dossier courant doit etre la racine du pack). Ensuite tout est automatique :
REM  4 redemarrages, reprise toute seule (cle Run puis C:\W98FR\GO.BAT).
REM
REM  REGLES COMMAND.COM (Windows 98) respectees dans ce fichier :
REM   - pas de tilde-dp0, else, parentheses, redirection 2, FOR /F,
REM     SET /P, CALL :etiquette, double esperluette
REM   - CHOICE sans /M : CHOICE /C:ON /N texte  (pas de "/" dans le
REM     texte, sinon il faut des guillemets)
REM   - un .bat N'ATTEND PAS un programme Windows : toujours
REM     "start /w" devant RUNDLL32, REGEDIT, setup.exe, etc.
REM   - etiquettes uniques sur leurs 8 premiers caracteres
REM   - lignes de moins de 127 caracteres : on fait "cd" dans le dossier du
REM     composant, puis "cd" retour vers la racine du pack
REM   - INF lances par ".\NOM.INF" (dossier courant), jamais par un
REM     nom nu (ADVPACK pourrait prendre celui de WINDOWS\INF)
REM
REM  Dossier de travail : C:\W98FR (marqueurs d'etape, GO.BAT de
REM  reprise, sauvegardes BAK, fichiers temporaires).
REM ============================================================

REM --- Environnement agrandi (chemins longs + variables) ---
if "%W98ENV%"=="1" goto DEBUT
set W98ENV=1
%COMSPEC% /e:4096 /c INSTALL.BAT
set W98ENV=
exit

:DEBUT
REM ISO Win98FR : composants coches pendant l'installation de Windows
if exist C:\W98FR\CHOIX.BAT call C:\W98FR\CHOIX.BAT
echo install.bat : lancement>> C:\W98FR\JOURNAL.TXT
if not exist C:\W98FR\NUL md C:\W98FR
if not exist C:\W98FR\BAK\NUL md C:\W98FR\BAK

REM --- Verrou : une seule fenetre d'installation a la fois. Il reste
REM     present apres un redemarrage force : on peut alors continuer ---
if not exist C:\W98FR\ENCOURS.TXT goto VERROU
echo install.bat : verrou deja present>> C:\W98FR\JOURNAL.TXT
cls
echo.
echo  Une autre fenetre d'installation semble deja ouverte,
echo  ou la precedente a ete interrompue (redemarrage force).
echo  Si une autre fenetre MS-DOS d'installation est ouverte,
echo  repondez N et laissez-la continuer.
echo.
REM ISO : verrou laisse par un redemarrage force = on continue
if "%W98AUTO%"=="1" goto VERROU
choice /C:ON /N "Continuer dans cette fenetre ? [O,N] "
if errorlevel 2 goto FINDEJA
:VERROU
echo.> C:\W98FR\ENCOURS.TXT
set EXTRAS=non
if exist C:\W98FR\EXTRAS.TXT set EXTRAS=oui

REM --- Reprise : C:\W98FR\ETxx.TXT designe l'etape a (re)lancer.
REM     Chaque etape pose son marqueur DES SON DEBUT : apres un
REM     redemarrage prevu OU imprevu, on reprend a l'etape en cours
REM     (relancer une etape deja faite a moitie est sans danger).
set RSTEP=
if exist C:\W98FR\ET1A.TXT set RSTEP=ST1A
if exist C:\W98FR\ET1B.TXT set RSTEP=ST1B
if exist C:\W98FR\ET2.TXT set RSTEP=ST2
if exist C:\W98FR\ET3.TXT set RSTEP=ST3
if exist C:\W98FR\ET4.TXT set RSTEP=ST4
if exist C:\W98FR\ET5.TXT set RSTEP=ST5
if exist C:\W98FR\ET6.TXT set RSTEP=ST6
if exist C:\W98FR\ET7.TXT set RSTEP=ST7
if exist C:\W98FR\ET8.TXT set RSTEP=ST8
if exist C:\W98FR\ET9.TXT set RSTEP=ST9
if exist C:\W98FR\ET10.TXT set RSTEP=STA
if exist C:\W98FR\ET11.TXT set RSTEP=STX
if "%RSTEP%"=="" goto MENU
REM --- (la cle Run est permanente jusqu'a la fin : rien a re-armer,
REM     sauf si GO.BAT manque : coupure avant le 1er redemarrage)
if not exist C:\W98FR\GO.BAT goto INITGO
cls
echo.
echo  Reprise de l'installation du pack Windows 98 SE FR.
echo  Reprise automatique dans 10 secondes.
echo.
if "%W98AUTO%"=="1" goto %RSTEP%
choice /C:CA /N /T:C,10 "C = continuer, A = abandonner l'installation : "
if errorlevel 2 goto ABANDON
goto %RSTEP%

:MENU
if "%W98AUTO%"=="1" goto MODET
cls
echo.
echo            PACK WINDOWS 98 SE FR - INSTALLATION (v3)
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
echo   1 = [1/11] IE6 SP1 + WMP9      B = [1/11] correctifs, DX9b, MDAC
echo   2 = [2/11] SP3.0 B4 FR         3 = [3/11] correctifs systeme
echo   4 = [4/11] IE et OE            5 = [5/11] extras
echo   6 = [6/11] optionnels          7 = [7/11] (DirectX : pack 2)
echo   8 = [8/11] .NET                9 = [9/11] chipset
echo   A = [10/11] applications       0 = [11/11] couche 3.66, PATCHMEM
echo.
choice /C:1B23456789A0 /N "Reprendre a l'etape : "
if errorlevel 1 set RSTEP=ST1A
if errorlevel 2 set RSTEP=ST1B
if errorlevel 3 set RSTEP=ST2
if errorlevel 4 set RSTEP=ST3
if errorlevel 5 set RSTEP=ST4
if errorlevel 6 set RSTEP=ST5
if errorlevel 7 set RSTEP=ST6
if errorlevel 8 set RSTEP=ST7
if errorlevel 9 set RSTEP=ST8
if errorlevel 10 set RSTEP=ST9
if errorlevel 11 set RSTEP=STA
if errorlevel 12 set RSTEP=STX
echo.
choice /C:TE /N "Mode : T = Tout, E = Essentiel : "
if errorlevel 2 goto MODEE

:MODET
echo.> C:\W98FR\EXTRAS.TXT
set EXTRAS=oui
goto INITGO
:MODEE
if exist C:\W98FR\EXTRAS.TXT del C:\W98FR\EXTRAS.TXT
set EXTRAS=non

REM --- Memorise le dossier du pack et prepare la reprise auto ---
REM     (astuce DOS : PROMPT ecrit lettre de lecteur et dossier
REM     courant dans un .bat qu'on execute ensuite)
:INITGO
cd 02_SP30
echo @prompt set W98DRV=$n:$_set W98SUB=$p$_> C:\W98FR\P1.BAT
REM /e:2048 : sinon pas de place pour PROMPT quand CHOIX.BAT a rempli
REM l'environnement (mode auto, test QEMU 2026-10-19)
%COMSPEC% /e:2048 /c C:\W98FR\P1.BAT > C:\W98FR\P2.BAT
call C:\W98FR\P2.BAT
del C:\W98FR\P1.BAT
del C:\W98FR\P2.BAT
cd ..
if "%W98SUB%"=="" goto NOGO
REM --- GO.BAT (lance par la cle Run a chaque demarrage tant que
REM     l'installation n'est pas finie) : ne fait rien sans etape en
REM     cours, attend jusqu'a 60 s que le dossier du pack soit pret ---
set G=C:\W98FR\GO.BAT
echo @echo off> %G%
echo if not exist C:\W98FR\ET*.TXT goto FIN>> %G%
echo set N=>> %G%
echo :ATTENDRE>> %G%
echo if exist "%W98SUB%\SPUPDATE.INF" goto LANCER>> %G%
echo set N=%%N%%x>> %G%
echo if "%%N%%"=="xxxxxxxxxxxx" goto ECHEC>> %G%
echo echo Attente du dossier du pack...>> %G%
echo choice /C:O /N /T:O,5>> %G%
echo goto ATTENDRE>> %G%
echo :LANCER>> %G%
echo %W98DRV%>> %G%
echo cd "%W98SUB%">> %G%
echo cd ..>> %G%
echo call INSTALL.BAT>> %G%
echo goto FIN>> %G%
echo :ECHEC>> %G%
echo echo Dossier du pack introuvable : %W98SUB%\..>> %G%
echo echo Inserez le CD ou relancez INSTALL.BAT, il reprendra au bon endroit.>> %G%
echo pause>> %G%
echo :FIN>> %G%
echo set N=>> %G%
set G=
echo Pack : %W98SUB%\..>> C:\W98FR\JOURNAL.TXT
set R=C:\W98FR\REPRISE.REG
echo REGEDIT4> %R%
echo.>> %R%
echo [HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run]>> %R%
echo "W98FR"="command.com /c C:\\W98FR\\GO.BAT">> %R%
set R=
start /w REGEDIT /s C:\W98FR\REPRISE.REG
:NOGO
if not "%RSTEP%"=="" goto %RSTEP%

REM ============================================================
REM  [1/11] Base officielle Microsoft, phase 1 : IE6 SP1 + WMP9
REM ============================================================
:ST1A
echo Etape ST1A : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET1A.TXT
cls
echo.
echo [1/11] Base Microsoft officielle (1/2) : IE6 SP1 + Windows Media Player 9
echo.
REM  Fichiers du CD dans WINDOWS\OPTIONS\CABS + SourcePath (comme le pack ME,
REM  2026-10-26) : plus de demande du CD ni de "fichier introuvable" ensuite
echo   - Fichiers du CD dans C:\WINDOWS\OPTIONS\CABS (plus besoin du CD ensuite)
start /w CSCRIPT.EXE //NoLogo 03_SYST\CABS.VBS
cd 01_BASE\ie6sp1
echo   - Internet Explorer 6 SP1 FR
start /w IE6SETUP.EXE /Q:A /R:N /C:"ie6wzd /S:""#e"" /Q:A /R:N"
cd ..\wmp9
echo   - Windows Media Player 9 FR
start /w MPSETUP.EXE /Q:U /R:N
cd ..\..
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET1B.TXT
goto RBOOT

REM ============================================================
REM  [1/11] phase 2 : les 5 correctifs fev. 2004 absents de SP3.0
REM  (les 18 autres sont contenus dans SP3.0, versions egales ou plus recentes),
REM  MDAC 2.8 SP1 FR. Commutateurs = WSEresume.inf
REM  DirectX n'est plus installe par le pack 1 : il est dans le pack 2
REM  (Win98FR_Plus, 8.1, 8.2 ou 9.0c), commun au pack et a l'ISO.
REM ============================================================
:ST1B
echo Etape ST1B : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET1B.TXT
cls
echo.
echo [1/11] Base Microsoft officielle (2/2) : correctifs et MDAC 2.8 SP1
echo.
cd 01_BASE\updates
echo   - Correctifs q240308, q313829, q330994 (OE6), q828750 (IE6), KB819639 (WMP9)
start /w Q240308.EXE /q:u /r:n
start /w Q313829.EXE /q:u /r:n
start /w Q330994.EXE /q:u /r:n
start /w Q828750.EXE /q:u /r:n
start /w KB819639.EXE /q:a /r:n
cd ..\mdac28
echo   - MDAC 2.8 SP1 FR
start /w MDAC_TYP.EXE /Q /C:"DASETUP /Q /N"
cd ..\..
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET2.TXT
goto RBOOT

REM ============================================================
REM  [2/11] SP3.0 Beta 4 FR - mise a jour principale (spupdate.inf
REM  adapte : fuseaux EN et dates d'ete US retires). Ne retrograde
REM  rien (drapeaux 32/1056 = garde le fichier le plus recent).
REM ============================================================
:ST2
echo Etape ST2 : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET2.TXT
cls
echo.
echo [2/11] Service Pack non officiel SP3.0 B4 FR (mise a jour principale)
echo.
echo   Patientez, cela peut prendre plusieurs minutes.
cd 02_SP30
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SPUPDATE.INF,DefaultInstall
cd ..
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET3.TXT
goto RBOOT

REM ============================================================
REM  [3/11] Corrections systeme plus recentes que SP3.0
REM ============================================================
:ST3
echo Etape ST3 : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET3.TXT
cls
echo.
echo [3/11] Correctifs systeme (Shell98 FR 2007, GDI Q918547, 3.63, certificats)
echo.
echo   Si une fenetre propose de redemarrer, repondez NON.
echo.
cd 01_BASE
start /w REGEDIT /s WINSUB_B.REG
cd ..\03_SYST
echo   - Shell32.dll FR revise (2007)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SHELL98.INF,DefaultInstall
echo   - GDI.EXE / GDI32.DLL (Q918547 FR)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\Q918547.INF,DefaultInstall
echo   - Inserer un objet et Aide HTML en francais (OLEDLG, HHCTRL traduits)
cd frtrad
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\FRTRAD.INF,DefaultInstall
cd ..\copie363
call copie.bat
cd ..\rootsupd
echo   - Certificats racine de septembre 2020 (3.66) + certificats revoques
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\ROOTSUPD.INF,DefaultInstall
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\RVKROOTS.INF,DefaultInstall
cd ..\..

REM ============================================================
REM  [4/11] Internet Explorer / Outlook Express (FR 2004-2007)
REM ============================================================
:ST4
echo Etape ST4 : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET4.TXT
echo.
echo [4/11] Internet Explorer / Outlook Express (correctifs FR plus recents)
echo.
echo   Si une fenetre propose de redemarrer, repondez NON.
echo.
cd 04_IEOE
echo   - Outlook Express KB823353 FR puis KB887797 FR
start /w KB823353-OE6sp1.exe /q:a /r:n
start /w KB887797-OE6sp1.exe /q:a /r:n
echo   - Coeur IE6 Q931768 FR (2007), INF Windows 98 du pack (IE6Q9317.INF)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\IE6Q9317.INF,DefaultInstall
cd ..
if "%EXTRAS%"=="non" goto ST7

REM ============================================================
REM  [5/11] Extras
REM  Composants SP3.0 : lances en natif depuis sp30\ (INF, CAB et
REM  MLAYOUT d'origine). Le reste vient de extras\.
REM ============================================================
:ST5
echo Etape ST5 : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET5.TXT
cls
echo.
echo [5/11] Extras
echo.
cd 02_SP30
echo   - USB 2.0 et cles USB (NUSB 3.3 FR, SP3.0)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\NUSB.INF,DefaultInstall
echo   - Apparence Web des dossiers (Windows Me, SP3.0)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\MEVIEW.INF,DefaultInstall
echo   - Utilitaires Windows Me FR : Defrag, Regedit, Mes images (SP3.0)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\ME-PROGS.INF,DefaultInstall
echo   - Outil de conversion de l'euro (SP3.0)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\EURO.INF,DefaultInstall
echo   - TweakUI 1.33 FR (SP3.0)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TWEAKUI.INF,DefaultInstall
cd ..\05_EXTRA\kernelex
echo   - KernelEx 4.5.2019.24 FR (4.5.2 FR + mise a jour de Jumper)
start /w KernelEx-4.5.2019.24-FR.exe /S
echo   - KernelEx desactive par defaut (a activer par programme)
start /w REGEDIT /s KEXOFF.REG
cd ..\ntfs
REM  Configurateur NTFS : NTFSCFG.VBS (sans WMI, qui ne marche pas sous 98).
echo   - Lecteur NTFS (Paragon, configurateur FR)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\PNTFS.INF,DefaultInstall
cd ..\plus98
echo   - Plus! 98 FR : themes + Spider Solitaire (cle : plus98\MSBATCH.INF)
start /w INSTALL.EXE
cd ..\jeux
echo   - Pinball 3D FR + dossier Jeux a la racine de Programmes
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\PINBALL.INF,DefaultInstall
start /w CSCRIPT.EXE //NoLogo DEPLJEUX.VBS
cd ..\taskbarshuffle
echo   - Taskbar Shuffle 2.5
start /w ts2.5_setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
cd ..\w2kcolor
echo   - Theme Windows 2000 (icones + couleurs, sur le Shell32 FR 2007)
call w2kcolor.bat
cd ..\tweaks
echo   - Reglages de performance (SP3.0 FR + menus Copier/Deplacer vers 3.66)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TWEAKS.INF,DefaultInstall
cd ..\mspaintfilter
echo   - Filtres graphiques Paint + apercu d'image
start /w REGEDIT /s "install filter.reg"
copy *.FLT %WINDIR%\SYSTEM > NUL
cd ..\aspi
echo   - ASPI 4.71.2 (Adaptec)
REM SILENT : sans les fenetres Install et Reboot (option de ASPIINST.EXE)
start /w ASPIINST.EXE SILENT
cd ..\..

REM --- Point d'extension personnel : extras\perso\perso.bat est
REM     appele DEPUIS SON PROPRE DOSSIER s'il existe ---
if not exist 05_EXTRA\perso\perso.bat goto NOPERSO
cd 05_EXTRA\perso
call perso.bat
%W98DRV%
if "%W98SUB%"=="" goto PERSOREL
cd "%W98SUB%"
cd ..
goto NOPERSO
:PERSOREL
cd ..\..
:NOPERSO

REM  MS Agent, DirectX, MMC, RegClean et SharedDLLs : dans le pack 2
REM  (Win98FR_Plus), commun au pack 1 et a l'ISO.

REM ============================================================
REM  [6/11] Composants optionnels (un par un)
REM ============================================================
:ST6
echo Etape ST6 : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET6.TXT
cls
echo.
echo [6/11] Composants optionnels
echo.
cd 02_SP30
if "%W98AUTO%"=="1" if not "%C_WINTOP%"=="O" goto NOWINTOP
if "%W98AUTO%"=="1" goto OKWINTOP
choice /C:ON /N "WinTop, moniteur de taches et memoire (SP3.0) ? [O,N] "
if errorlevel 2 goto NOWINTOP
:OKWINTOP
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\WINTOP.INF,DefaultInstall
:NOWINTOP
if "%W98AUTO%"=="1" if not "%C_DOSH%"=="O" goto NODOSHER
if "%W98AUTO%"=="1" goto OKDOSH
choice /C:ON /N "Invite de commande ici, menu des dossiers (SP3.0) ? [O,N] "
if errorlevel 2 goto NODOSHER
:OKDOSH
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\DOSHERE.INF,DefaultInstall
:NODOSHER
REM  Plus! 98 (etape 5) pose deja ses logos (C:\LOGO.SYS + LOGOW.SYS) : pas de
REM  question dans ce cas (test GX240 2026-10-16, doublon)
if exist C:\LOGO.SYS goto NOLOGO
if "%W98AUTO%"=="1" if not "%C_LOGO%"=="O" goto NOLOGO
if "%W98AUTO%"=="1" goto OKLOGO
choice /C:ON /N "Logos de demarrage et d'arret animes (SP3.0) ? [O,N] "
if errorlevel 2 goto NOLOGO
:OKLOGO
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\LOGO.INF,DefaultInstall
:NOLOGO
REM WSH : d'abord 5.6 FR du SP3.0 (menus et reglages FR), puis les moteurs
REM 5.7 de la 3.66 par-dessus (05_EXTRA\wsh57). Dans l'autre ordre, la 5.6
REM provoque des "conflits de versions" et ecrase la 5.7.
if "%W98AUTO%"=="1" if not "%C_WSH%"=="O" goto NOWSH
if "%W98AUTO%"=="1" goto OKWSH
choice /C:ON /N "Windows Script Host FR (5.6 SP3.0 puis moteurs 5.7) ? [O,N] "
if errorlevel 2 goto NOWSH
:OKWSH
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SCR56.INF,DefaultInstall
cd ..\05_EXTRA\wsh57
echo   - Windows Script 5.7 : JScript, VBScript (3.66, menus FR gardes)
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\WSH57.INF,DefaultInstall
cd ..\..\02_SP30
:NOWSH
cd ..\06_OPTS
if "%W98AUTO%"=="1" if not "%C_TZ%"=="O" goto NOTZ
if "%W98AUTO%"=="1" goto OKTZ
choice /C:ON /N "Fuseaux horaires a jour (noms FR, regles 2020) ? [O,N] "
if errorlevel 2 goto NOTZ
:OKTZ
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TIMEZONE.INF,DefaultInstall
REM ISO (reponses automatiques) : fuseau deja choisi par l'installation de
REM Windows, regles d'ete europeennes identiques : pas de fenetre
if "%W98AUTO%"=="1" goto NOTZ
echo   Re-selectionnez votre fuseau horaire puis cliquez OK.
start /w RUNDLL32.EXE SHELL32.DLL,Control_RunDLL TIMEDATE.CPL
:NOTZ
REM  Seule source des Dossiers compresses : sous Windows 98, Plus! 98 ne les
REM  propose pas (absents de [Components.Reg], Sauvegarde 6). Deja la : rien.
if exist %WINDIR%\SYSTEM\ZIPFLDR.DLL goto NOZIP
if "%W98AUTO%"=="1" if not "%C_ZIP%"=="O" goto NOZIP
if "%W98AUTO%"=="1" goto OKZIP
choice /C:ON /N "Dossiers compresses .zip (FR) ? [O,N] "
if errorlevel 2 goto NOZIP
:OKZIP
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\ZIPFLDR.INF,DefaultInstall
:NOZIP
if "%W98AUTO%"=="1" if not "%C_TTF%"=="O" goto NOTTF
if "%W98AUTO%"=="1" goto OKTTF
choice /C:ON /N "Extension TrueType pour les polices (EN) ? [O,N] "
if errorlevel 2 goto NOTTF
:OKTTF
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TTFEXT.INF,DefaultInstall
:NOTTF
cd ..

REM ============================================================
REM  [7/11] DirectX : dans le pack 2 (Win98FR_Plus), une seule version
REM  au choix (8.1, 8.2 ou 9.0c). Etape gardee pour la numerotation.
REM ============================================================
:ST7
echo Etape ST7 : DirectX dans Win98FR_Plus>> C:\W98FR\JOURNAL.TXT

REM ============================================================
REM  [8/11] .NET Framework (optionnel, jamais automatique)
REM  Windows Installer 2.0 est deja installe par SP3.0.
REM ============================================================
:ST8
echo Etape ST8 : debut>> C:\W98FR\JOURNAL.TXT
if "%EXTRAS%"=="non" goto FINC2
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET8.TXT
cls
echo.
echo [8/11] .NET Framework (optionnel)
echo.
if "%W98AUTO%"=="1" if not "%C_NET11%"=="O" goto NONET11
if "%W98AUTO%"=="1" goto OKNET11
choice /C:ON /N ".NET Framework 1.1 FR avec SP1 et KB886903 ? [O,N] "
if errorlevel 2 goto NONET11
:OKNET11
cd 08_NET\net11
echo   Patientez : 10 a 20 minutes au total sous Windows 98.
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
REM  .NET 2.0 (dotnet9x) retire le 2026-10-16 : il faisait planter DXSETUP et
REM  dxdiag (MSVCR80, test GX240) et aucune appli du pack n'en a besoin.

REM ============================================================
REM  [9/11] Pilotes chipset (optionnel) : detection du pont hote
REM  PCI (registre Enum\PCI), puis choix du paquet exact.
REM ============================================================
:ST9
echo Etape ST9 : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET9.TXT
cls
echo.
echo [9/11] Pilotes chipset de la carte mere (optionnel)
echo.
echo   A la fin, si l'installeur du chipset propose de redemarrer,
echo   repondez NON : ce script redemarre juste apres, proprement.
echo.
if "%W98AUTO%"=="1" if not "%C_CHIP%"=="O" goto FINC2
if "%W98AUTO%"=="1" goto OKCHIP
choice /C:ON /N "Detecter et installer les pilotes chipset ? [O,N] "
if errorlevel 2 echo Etape ST9 : chipset refuse (N)>> C:\W98FR\JOURNAL.TXT
if errorlevel 2 goto FINC2
:OKCHIP
cd 09_CHIP
if exist C:\W98FR\CHIPSET.BAT del C:\W98FR\CHIPSET.BAT
start /w CSCRIPT.EXE //NoLogo DETECT_CHIPSET.VBS
set CHIPSET=INCONNU
if exist C:\W98FR\CHIPSET.BAT call C:\W98FR\CHIPSET.BAT
echo   Chipset detecte : %CHIPSET%
echo Etape ST9 : chipset detecte = %CHIPSET%>> C:\W98FR\JOURNAL.TXT
echo.
if "%CHIPSET%"=="INTEL" goto CHINTEL
if "%CHIPSET%"=="VIA" goto CHVIA
if "%CHIPSET%"=="SIS" goto CHSIS
echo   Fabricant non reconnu : rien n'est installe.
echo Etape ST9 : fabricant non reconnu>> C:\W98FR\JOURNAL.TXT
if "%W98AUTO%"=="1" goto CHFIN
pause
goto CHFIN

:CHINTEL
echo   A = Intel 3.20.1008 (440BX/LX/GX, 810, 815)
echo   B = Intel 6.3.0.1007 (serie 800 dont 845, puis 915/925)
echo   C = Intel Pentium a Pentium II uniquement
echo   N = ne rien installer
choice /C:ABCN /N "Votre choix : "
if errorlevel 4 echo Etape ST9 : Intel, aucun pilote choisi (N)>> C:\W98FR\JOURNAL.TXT
if errorlevel 4 goto CHFIN
if errorlevel 3 goto CHI3
if errorlevel 2 goto CHI2
echo Etape ST9 : Intel 3.20.1008 lance>> C:\W98FR\JOURNAL.TXT
cd intel\3201008
goto CHIINF
:CHI2
echo Etape ST9 : Intel 6.3.0.1007 lance>> C:\W98FR\JOURNAL.TXT
cd intel\6301007
:CHIINF
start /w INFINST_ENU.EXE
echo Etape ST9 : installeur Intel termine>> C:\W98FR\JOURNAL.TXT
cd ..\..
goto CHFIN
:CHI3
echo Etape ST9 : Intel Pentium a Pentium II lance>> C:\W98FR\JOURNAL.TXT
cd intel\pentiumTo2
start /w SETUP.EXE
cd ..\..
goto CHFIN

:CHVIA
echo   A = VIA 4in1 4.35v (anciens : KT133, KT266)
echo   B = VIA Hyperion 4.56v (recents : KT400 et plus, P4X400 et plus)
echo   C = VIA vlatency (seulement si soucis son, USB ou IDE)
echo   N = ne rien installer
choice /C:ABCN /N "Votre choix : "
if errorlevel 4 echo Etape ST9 : VIA, aucun pilote choisi (N)>> C:\W98FR\JOURNAL.TXT
if errorlevel 4 goto CHFIN
if errorlevel 3 goto CHV3
if errorlevel 2 goto CHV2
echo Etape ST9 : VIA 4in1 4.35v lance>> C:\W98FR\JOURNAL.TXT
cd via\4in1_435v
start /w SETUP.EXE
cd ..\..
goto CHFIN
:CHV2
echo Etape ST9 : VIA Hyperion 4.56v lance>> C:\W98FR\JOURNAL.TXT
cd via\hyperion
start /w VIAHyperion4in1456v.exe
cd ..\..
goto CHFIN
:CHV3
echo Etape ST9 : VIA vlatency lance>> C:\W98FR\JOURNAL.TXT
cd via\vlatency
start /w vlatency_v020_beta21.exe
cd ..\..
goto CHFIN

:CHSIS
echo   A = SiS 530 (graphique integre SiS530)
echo   B = SiS 5597 et 5598 (graphique integre)
echo   C = SiS agp121 (AGP SiS 6xx et 7xx)
echo   D = SiS ide204a (IDE SiS 96x, 630, 730)
echo   N = ne rien installer
choice /C:ABCDN /N "Votre choix : "
if errorlevel 5 echo Etape ST9 : SiS, aucun pilote choisi (N)>> C:\W98FR\JOURNAL.TXT
if errorlevel 5 goto CHFIN
if errorlevel 4 goto CHS4
if errorlevel 3 goto CHS3
if errorlevel 2 goto CHS2
echo Etape ST9 : SiS 530 lance>> C:\W98FR\JOURNAL.TXT
cd sis\530_5598\530_108\Win98
start /w REGMOD.EXE
cd ..\..\..\..
goto CHFIN
:CHS2
echo Etape ST9 : SiS 5597/5598 lance>> C:\W98FR\JOURNAL.TXT
cd sis\530_5598\5598_113\win98
start /w SETUP.EXE
cd ..\..\..\..
goto CHFIN
:CHS3
echo Etape ST9 : SiS agp121 lance>> C:\W98FR\JOURNAL.TXT
cd sis\agp121
start /w SETUP.EXE
cd ..\..
goto CHFIN
:CHS4
echo Etape ST9 : SiS ide204a lance>> C:\W98FR\JOURNAL.TXT
cd sis\ide204a
start /w SETUP.EXE
cd ..\..

:CHFIN
cd ..
if exist C:\W98FR\CHIPSET.BAT del C:\W98FR\CHIPSET.BAT

REM --- Fin de la Couche 2 : redemarrage, puis [11/11] ---
:FINC2
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET10.TXT
goto RBOOT

REM ============================================================
REM  [10/11] Applications (optionnel, mode Tout seulement). Apres le
REM  redemarrage qui suit le chipset : KernelEx est alors actif,
REM  indispensable a VC++ 2008. Le reste (Firefox, VLC, jeux, outils
REM  de test...) est dans le pack 2 : Win98FR_Plus\PLUS.BAT.
REM ============================================================
:STA
echo Etape STA : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET10.TXT
if "%EXTRAS%"=="non" goto STX
cls
echo.
echo [10/11] Applications (optionnel)
echo.
cd 10_APPLI\vc2005
if "%W98AUTO%"=="1" if not "%C_VC5%"=="O" goto NOVC5
if "%W98AUTO%"=="1" goto OKVC5
choice /C:ON /N "Visual C++ 2005 (bibliotheques des programmes) ? [O,N] "
if errorlevel 2 goto NOVC5
:OKVC5
REM VCREDIST.EXE (emballage FR) contient VCREDI~3.EXE (installeur standard
REM 8.0.50727.42) qui contient vcredist.msi : on extrait, puis on lance.
if not exist C:\W98FR\VC5\NUL md C:\W98FR\VC5
start /w VCREDIST.EXE /Q /T:C:\W98FR\VC5 /C
if exist C:\W98FR\VC5\VCREDI~3.EXE start /w C:\W98FR\VC5\VCREDI~3.EXE /q:a /c:"msiexec /i vcredist.msi /qb"
if not exist C:\W98FR\VC5\VCREDI~3.EXE echo   ATTENTION : extraction de Visual C++ 2005 impossible.
if not exist C:\W98FR\VC5\VCREDI~3.EXE echo Etape STA : VC++ 2005 extraction impossible>> C:\W98FR\JOURNAL.TXT
deltree /y C:\W98FR\VC5 > NUL
:NOVC5
cd ..\vc2008
if "%W98AUTO%"=="1" if not "%C_VC8%"=="O" goto NOVC
if "%W98AUTO%"=="1" goto OKVC8
choice /C:ON /N "Visual C++ 2008 pour 98 (exige KernelEx) ? [O,N] "
if errorlevel 2 goto NOVC
:OKVC8
start /w VC_R_9X.EXE /q:a /r:n
:NOVC
cd ..\qres
if "%W98AUTO%"=="1" if not "%C_QRES%"=="O" goto NOQRES
if "%W98AUTO%"=="1" goto OKQRES
choice /C:ON /N "QRes (jeux Windows en 256 couleurs) ? [O,N] "
if errorlevel 2 goto NOQRES
:OKQRES
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\QRES.INF,DefaultInstall
start /w CSCRIPT.EXE //NoLogo LIENBUR.VBS
echo   Mode d'emploi : C:\WINDOWS\QRES.TXT
:NOQRES
cd ..\7zip
if "%W98AUTO%"=="1" if not "%C_7Z%"=="O" goto NO7Z
if "%W98AUTO%"=="1" goto OK7Z
choice /C:ON /N "7-Zip 9.20 (archives, interface francaise) ? [O,N] "
if errorlevel 2 goto NO7Z
:OK7Z
start /w 7Z920.EXE /S
:NO7Z
cd ..\daemon
if "%W98AUTO%"=="1" if not "%C_DT%"=="O" goto NODT
if "%W98AUTO%"=="1" goto OKDT
choice /C:ON /N "DAEMON Tools 3.47 (lecteur CD virtuel) ? [O,N] "
if errorlevel 2 goto NODT
:OKDT
start /w %WINDIR%\SYSTEM\MSIEXEC.EXE /i DAEMON.MSI /qb REBOOT=ReallySuppress
if exist 1036.DLL copy 1036.DLL "C:\Program Files\D-Tools\Lang" > NUL
start /w REGEDIT /s DAEMON.REG
:NODT
cd ..\retrozil
if "%W98AUTO%"=="1" if not "%C_RZ%"=="O" goto NORZ
if "%W98AUTO%"=="1" goto OKRZ
choice /C:ON /N "RetroZilla 2.3 (navigateur web) ? [O,N] "
if errorlevel 2 goto NORZ
:OKRZ
start /w RZ23.EXE -ms
REM  Navigateur par defaut, sans la question au 1er lancement : memes cles que
REM  RetroZilla quand on repond Yes (releve test12, 2026-10-20)
echo   - RetroZilla : navigateur par defaut
start /w REGEDIT /s RETROZIL.REG
:NORZ
cd ..\tarot
if "%W98AUTO%"=="1" if not "%C_TAROT%"=="O" goto NOTAROT
if "%W98AUTO%"=="1" goto OKTAROT
choice /C:ON /N "Jeu de Tarot (Sybex, francais) ? [O,N] "
if errorlevel 2 goto NOTAROT
:OKTAROT
if not exist C:\JEUX\NUL md C:\JEUX
if not exist C:\JEUX\TAROT\NUL md C:\JEUX\TAROT
REM  /S : les .dat et l'animation vont dans C:\JEUX\TAROT\DATA (Groupe 2 de
REM  l'installeur d'origine ; a plat, le jeu reclamait DATA\SCRIPT10.DAT)
xcopy JEU\*.* C:\JEUX\TAROT /S /Y > NUL
if not exist %WINDIR%\SYSTEM\VB6DOCKOCX.OCX copy VB6DOCKOCX.OCX %WINDIR%\SYSTEM > NUL
start /w REGSVR32 /s %WINDIR%\SYSTEM\VB6DOCKOCX.OCX
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\TAROT.INF,DefaultInstall
:NOTAROT
cd ..\fraps
if not exist FRAPS19D.EXE goto NOFRAPS
if "%W98AUTO%"=="1" if not "%C_FRAPS%"=="O" goto NOFRAPS
if "%W98AUTO%"=="1" goto OKFRAPS
choice /C:ON /N "Fraps 1.9D (images par seconde dans les jeux, guide) ? [O,N] "
if errorlevel 2 goto NOFRAPS
:OKFRAPS
REM  ISO : installation sans question (NSIS /S, dossier C:\Fraps par defaut)
if "%W98AUTO%"=="1" goto FRAPSAUTO
start /w FRAPS19D.EXE
goto NOFRAPS
:FRAPSAUTO
start /w FRAPS19D.EXE /S
:NOFRAPS
REM  SIV 5.88 (gratuit) : materiel, memoire et timings, PCI, USB, capteurs
cd ..\siv
if not exist SIV.INF goto NOSIV
if "%W98AUTO%"=="1" if not "%C_SIV%"=="O" goto NOSIV
if "%W98AUTO%"=="1" goto OKSIV
choice /C:ON /N "SIV, informations systeme (memoire, PCI, USB, capteurs) ? [O,N] "
if errorlevel 2 goto NOSIV
:OKSIV
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SIV.INF,DefaultInstall
:NOSIV
REM  Bascule MSVCRT 6.1 (SP3.0) / 7.0 (3.66) par un raccourci sur le Bureau :
REM  7.0 = VLC ne plante plus a la fermeture, mais bloque les installeurs de
REM  K-Lite et de 3DMark 2001 (test GX240) ; le systeme reste en 6.1.
cd ..\msvcrt
if "%W98AUTO%"=="1" if not "%C_MSVC%"=="O" goto NOMSVC
if "%W98AUTO%"=="1" goto OKMSVC
choice /C:ON /N "Raccourci de bascule MSVCRT 6.1 - 7.0 sur le Bureau ? [O,N] "
if errorlevel 2 goto NOMSVC
:OKMSVC
start /w CSCRIPT.EXE //NoLogo MSVCRTSW.VBS /installe
:NOMSVC
cd ..\..

REM ============================================================
REM  [11/11] Couche 3.66 filtree FR (03_SYST\sp366fr) puis correctif memoire
REM  PATCHMEM (RLoew, 03_SYST\rloew), EN DERNIER
REM  (apres le redemarrage qui suit tout le reste).
REM  FIX95CPU retire du pack : il ne concerne que Windows 95.
REM ============================================================
:STX
echo Etape STX : debut>> C:\W98FR\JOURNAL.TXT
del C:\W98FR\ET*.TXT > NUL
echo.> C:\W98FR\ET11.TXT
cls
echo.
echo [11/11] Couche 3.66 filtree FR
echo.
echo   Fichiers du Service Pack non officiel 3.66 plus recents que ceux du
echo   SP3.0 FR : pilotes de disque et CD, MSXML, Visual C++ et VB, Jet,
echo   noyau FR corrige... Les fichiers anglais qui remplaceraient un
echo   fichier francais sont ecartes (detail : 03_SYST\sp366fr\RAPPORT_366FR.TXT).
echo   Rien n'est retrograde : installe en dernier, apres tout le reste.
echo.
if "%W98AUTO%"=="1" if not "%C_366%"=="O" goto NO366
if "%W98AUTO%"=="1" goto OK366
choice /C:ON /N "Installer la couche 3.66 FR (conseille) ? [O,N] "
if errorlevel 2 goto NO366
:OK366
echo Etape STX : couche 3.66 lancee>> C:\W98FR\JOURNAL.TXT
cd 03_SYST\sp366fr
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SP366FR.INF,DefaultInstall
cd ..\..
echo Etape STX : couche 3.66 terminee>> C:\W98FR\JOURNAL.TXT
:NO366
cls
echo.
echo [11/11] Correctif memoire PATCHMEM (RLoew)
echo.
echo   PATCHMEM est indispensable au-dela de 512 Mo de RAM. Il patche
echo   VMM.VXD et VCACHE.VXD, puis retire MaxPhysPage et MaxFileCache
echo   de SYSTEM.INI (consigne RLoew apres un Service Pack).
echo.
if "%W98AUTO%"=="1" if not "%C_PMEM%"=="O" goto FINOK
if "%W98AUTO%"=="1" goto OKPMEM
choice /C:ON /N "Installer PATCHMEM maintenant ? [O,N] "
if errorlevel 2 goto FINOK
:OKPMEM
cd 03_SYST\rloew
echo Etape STX : PATCHMEM lance>> C:\W98FR\JOURNAL.TXT
REM ISO : VMM32.VXD deja corrige (patcher9x), donc PATCHMEM demande "Erase Backup
REM and Continue (Y/N)" : reponse Y lue dans OUI.TXT (test QEMU 2026-10-18)
if "%W98AUTO%"=="1" goto PMAUTO
PATCHMEM.EXE /I
goto PMFIN
:PMAUTO
PATCHMEM.EXE /I < OUI.TXT
:PMFIN
echo Etape STX : PATCHMEM termine>> C:\W98FR\JOURNAL.TXT
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SYSINI.INF,DefaultInstall
cd ..\..

:FINOK
REM --- Clavier DOS : KEYB n'est plus charge au demarrage de Windows (avec un clavier
REM     USB, il faisait figer Dungeon Keeper, fleche haut = Maj+8, GX240 2026-10-28) ;
REM     sa ligne passe d'AUTOEXEC.BAT a DOSSTART.BAT (mode MS-DOS) et a CLAVDOS.BAT
REM     (fenetre "Commandes MS-DOS"). Pas de redirection derriere un IF : COMMAND.COM
REM     l'appliquerait meme si la condition est fausse.
if exist C:\W98FR\CLAVDOS.TXT goto CLAVFAIT
echo   - Clavier DOS : en mode MS-DOS et dans Commandes MS-DOS seulement
echo Etape STX : clavier DOS>> C:\W98FR\JOURNAL.TXT
copy C:\AUTOEXEC.BAT C:\W98FR\AUTOEXEC.KBK > NUL
echo @echo off> %WINDIR%\CLAVDOS.BAT
find /i "keyb " < C:\W98FR\AUTOEXEC.KBK >> %WINDIR%\CLAVDOS.BAT
find /v /i "keyb " < C:\W98FR\AUTOEXEC.KBK > C:\AUTOEXEC.BAT
if exist %WINDIR%\DOSSTART.BAT goto CLAVDS
echo @echo off> %WINDIR%\DOSSTART.BAT
:CLAVDS
echo.>> %WINDIR%\DOSSTART.BAT
find /i "keyb " < C:\W98FR\AUTOEXEC.KBK >> %WINDIR%\DOSSTART.BAT
start /w CSCRIPT.EXE //NoLogo 05_EXTRA\clavier\CLAVDOS.VBS
echo.> C:\W98FR\CLAVDOS.TXT
:CLAVFAIT
REM --- DMA des peripheriques IDE (au choix) : ici, apres le redemarrage qui
REM     suit le pilote chipset, les canaux IDE du bon controleur existent
cls
echo.
echo  DMA des disques et lecteurs IDE (transferts 2 a 3 fois plus rapides)
echo.
echo  Conseille pour un vrai disque dur IDE et les lecteurs CD/DVD.
echo  Carte Compact Flash sur adaptateur IDE : seulement si elle le gere.
echo  Si Windows bloque ensuite au demarrage : touche Ctrl au demarrage,
echo  Mode sans echec, puis decocher DMA dans le Gestionnaire de
echo  peripheriques (disque, onglet Parametres).
echo.
if "%W98AUTO%"=="1" if not "%C_DMA%"=="O" goto NODMA
if "%W98AUTO%"=="1" goto OKDMA
choice /C:ON /N "Activer le DMA des disques et lecteurs IDE ? [O,N] "
if errorlevel 2 goto NODMA
:OKDMA
start /w CSCRIPT.EXE //NoLogo 09_CHIP\DMAON.VBS
:NODMA
REM --- KernelEx desactive par defaut, actif seulement pour les programmes regles
if exist %WINDIR%\KERNELEX\KERNELEX.DLL start /w REGEDIT /s 05_EXTRA\kernelex\KEXOFF.REG
REM --- Correctif d'arret NVIDIA 81.85/81.98/82.16/82.69 + desinstalleur : outil
REM     copie dans WINDOWS\NVFIX et verifie maintenant. Surveillance au
REM     demarrage (cle Run, pilote installe apres le pack) : au choix.
cls
echo.
echo  Correctif d'arret NVIDIA (pilotes 81.x et 82.x, GeForce 6 et plus)
echo.
echo  Ces pilotes font planter l'arret du PC. Le pack peut verifier a chaque
echo  demarrage si un tel pilote vient d'etre installe et le corriger.
echo  Ajoute NVFIX aux programmes du demarrage (visible dans msconfig) ;
echo  il ne fait rien tant que le pilote NVIDIA ne change pas.
echo  Sinon : double-cliquer sur WINDOWS\NVFIX\NVFIX.VBS apres le pilote.
echo.
set NVMODE=/installe
if "%W98AUTO%"=="1" if not "%C_NVSURV%"=="O" goto NVSANS
if "%W98AUTO%"=="1" goto OKNVSURV
choice /C:ON /N "Surveiller l'installation d'un pilote NVIDIA ? [O,N] "
if errorlevel 2 goto NVSANS
:OKNVSURV
set NVMODE=/surveille
:NVSANS
echo Fin : NVFIX %NVMODE%>> C:\W98FR\JOURNAL.TXT
start /w CSCRIPT.EXE //NoLogo 09_CHIP\nvidia\NVFIX.VBS %NVMODE%
set NVMODE=
REM ISO Win98FR : correctif processeurs recents, apres PATCHMEM
if "%C_P9X%"=="O" call 03_SYST\patcher9x\P9X.BAT
set APRES=FINMSG
goto NETTOY
:FINMSG
echo Fin : message final affiche>> C:\W98FR\JOURNAL.TXT
cls
echo.
echo  Installation terminee !
echo  (originaux remplaces sauvegardes dans C:\W98FR\BAK)
echo.
echo  Un redemarrage est necessaire pour finaliser.
echo.
echo  Ensuite, installez les pilotes (carte graphique, son...), puis
echo  lancez le pack 2 (CD 2 ou dossier Win98FR_Plus) : logiciels, jeux.
echo.
echo  Pilote NVIDIA 81.x ou 82.x : correctif d'arret au demarrage suivant si
echo  la surveillance est active, sinon WINDOWS\NVFIX\NVFIX.VBS.
echo.
if "%W98AUTO%"=="1" goto OKRB1
choice /C:ON /N "Redemarrer maintenant ? [O,N] "
if errorlevel 2 goto FINMAN
:OKRB1
echo Fin : redemarrage demande>> C:\W98FR\JOURNAL.TXT
REM ISO : redemarrage FORCE (6 = redemarrer et fermer sans question), sinon
REM Windows demandait de quitter cette fenetre MS-DOS (test QEMU 2026-10-18)
if "%W98AUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 6
if not "%W98AUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 2
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
REM ISO Win98FR : correctif processeurs recents re-applique avant chaque redemarrage
if "%C_P9X%"=="O" call 03_SYST\patcher9x\P9X.BAT
echo Redemarrage demande par le script>> C:\W98FR\JOURNAL.TXT
if exist C:\W98FR\REPRISE.REG start /w REGEDIT /s C:\W98FR\REPRISE.REG
if exist C:\W98FR\GO.BAT echo   Redemarrage necessaire : l'installation reprendra toute seule.
if not exist C:\W98FR\GO.BAT echo   Redemarrage necessaire : relancez ensuite INSTALL.BAT.
if "%W98AUTO%"=="1" goto OKRB2
choice /C:ON /N "Redemarrer maintenant ? [O,N] "
if errorlevel 2 goto RBMAN
:OKRB2
REM ISO : redemarrage FORCE (6 = redemarrer et fermer sans question), sinon
REM Windows demandait de quitter cette fenetre MS-DOS (test QEMU 2026-10-18)
if "%W98AUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 6
if not "%W98AUTO%"=="1" start RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 2
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
del C:\W98FR\ET*.TXT > NUL
if exist C:\W98FR\GO.BAT del C:\W98FR\GO.BAT
if exist C:\W98FR\REPRISE.REG del C:\W98FR\REPRISE.REG
if exist C:\W98FR\EXTRAS.TXT del C:\W98FR\EXTRAS.TXT
if exist C:\W98FR\CHOIX.BAT del C:\W98FR\CHOIX.BAT
if exist %WINDIR%\W98FRGO.BAT del %WINDIR%\W98FRGO.BAT
REM  Valeur Run\W98FR retiree par ADVPACK (DelReg) : l'ancien RegDelete par WSH
REM  la laissait en place (fenetre MS-DOS "fichier introuvable" a chaque demarrage)
echo Nettoyage : suppression de la cle Run>> C:\W98FR\JOURNAL.TXT
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\01_BASE\FINRUN.INF,DefaultInstall
set V=C:\W98FR\RUNCHK.VBS
echo On Error Resume Next> %V%
echo Set S = CreateObject("WScript.Shell")>> %V%
echo K = "HKLM\Software\Microsoft\Windows\CurrentVersion\Run\W98FR">> %V%
echo X = S.RegRead(K)>> %V%
echo If Err.Number = 0 Then S.RegDelete K>> %V%
echo Set F = CreateObject("Scripting.FileSystemObject")>> %V%
echo Set J = F.OpenTextFile("C:\W98FR\JOURNAL.TXT", 8, True)>> %V%
echo Err.Clear>> %V%
echo X = S.RegRead(K)>> %V%
echo M = "Nettoyage : Run\W98FR retire (verifie)">> %V%
echo If Err.Number = 0 Then M = "Nettoyage : ATTENTION, Run\W98FR toujours la">> %V%
echo J.WriteLine M>> %V%
echo J.Close>> %V%
start /w CSCRIPT.EXE //NoLogo %V%
del %V%
set V=
goto %APRES%

:FIN
if exist C:\W98FR\ENCOURS.TXT del C:\W98FR\ENCOURS.TXT
exit
:FINDEJA
echo install.bat : arret, autre fenetre en cours>> C:\W98FR\JOURNAL.TXT
exit
