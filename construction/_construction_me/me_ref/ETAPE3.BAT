@echo off
REM Kit VM de reference QuickInstall ME (genere par make_me_ref.py)
REM Lancer depuis le CD (lettre D:) : Executer > D:\ETAPEn.BAT
D:
echo [3/3] Certificats 2020, KernelEx, applications, mode MS-DOS FR
cd \CERTS
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\ROOTSUPD.INF,DefaultInstall
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\RVKROOTS.INF,DefaultInstall
cd \KEX
start /w KernelEx-4.5.2019.24-FR.exe /S
start /w REGEDIT /s KEXOFF.REG
cd \APPS\VC2005
if not exist C:\MEREF\NUL md C:\MEREF
start /w VCREDIST.EXE /Q /T:C:\MEREF /C
if exist C:\MEREF\VCREDI~3.EXE start /w C:\MEREF\VCREDI~3.EXE /q:a /c:"msiexec /i vcredist.msi /qb"
deltree /y C:\MEREF > NUL
cd \APPS\VC2008
start /w VC_R_9X.EXE /q:a /r:n
cd \APPS\QRES
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\QRES.INF,DefaultInstall
cd \APPS\7ZIP
start /w 7Z920.EXE /S
cd \APPS\RETROZIL
start /w RZ23.EXE -ms
start /w REGEDIT /s RETROZIL.REG
cd \APPS\SIV
start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SIV.INF,DefaultInstall
cd \
start /w REGEDIT /s SOURCE.REG
echo Etape 3 terminee (mode MS-DOS FR ensuite)>> C:\MEREF.TXT
REM dosmode_fr : son INSTALL.BAT corrige COMMAND.COM et REGENV32 dans son propre
REM dossier (donc pas depuis le CD), et finit par DOSMODE.INF, qui redemarre
if not exist C:\MEDOS\NUL md C:\MEDOS
xcopy D:\DOSMODE\*.* C:\MEDOS > NUL
C:
cd \MEDOS
call INSTALL.BAT
