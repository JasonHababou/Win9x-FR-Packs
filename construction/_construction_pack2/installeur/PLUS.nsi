; ============================================================
; PLUS.nsi - Pack 2 Win98FR : installeur a cases a cocher (NSIS 2.46)
; Remplace PLUS.BAT (essai). N'embarque aucun logiciel : il utilise le
; dossier applis\ du pack 2, cherche a cote de l'installeur, sinon dans
; ..\Win98FR_Plus\applis (dossier d'essai Win98FR_Plus_Installeur).
; Fichier en cp1252 (NSIS 2 ANSI). Compilation : makensis PLUS.nsi
; ============================================================

  !include "MUI2.nsh"
  !include "Sections.nsh"
  !include "LogicLib.nsh"

  Name "Win98FR - Pack 2"
  Caption "Win98FR - Pack 2 : logiciels, jeux et outils de test"
  OutFile "INSTALLER_PLUS.EXE"
  SetCompressor /SOLID lzma
  RequestExecutionLevel user
  ShowInstDetails show
  InstallDir "$PROGRAMFILES"

  Var APP        ; dossier applis du pack 2
  Var KEXNEW     ; 1 si KernelEx vient d'etre installe
  Var WARADIO    ; version de Winamp retenue (une seule cochee)
  Var WANB       ; nombre de versions de Winamp cochees avant le clic
  Var CLESOUV    ; 1 si BENCH_CLES.TXT est deja ouvert
  Var DXRADIO    ; version de DirectX retenue (une seule cochee)
  Var DXNB       ; nombre de versions de DirectX cochees avant le clic

;--------------------------------
; Interface

  !define MUI_ABORTWARNING
  !define MUI_COMPONENTSPAGE_SMALLDESC
  !define MUI_WELCOMEPAGE_TITLE "Win98FR - Pack 2"
  !define MUI_WELCOMEPAGE_TEXT "Logiciels, jeux et outils de test pour Windows 98 SE et Windows Me.$\r$\n$\r$\nA lancer APRES l'installation de base (pack 1) et APRES les pilotes (carte graphique, son) : la Puzzle Collection et les 3DMark exigent 256 couleurs ou plus.$\r$\n$\r$\nCochez ce que vous voulez installer a la page suivante. KernelEx est installe automatiquement s'il manque et qu'un logiciel coche en a besoin."
  !define MUI_COMPONENTSPAGE_TEXT_TOP "Cochez les elements a installer. Passez la souris sur un element pour sa description."
  !define MUI_FINISHPAGE_TITLE "Pack 2 termine"

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_LANGUAGE "French"

;--------------------------------
; Outils

!macro INF DIR FILE
  SetOutPath "$APP\${DIR}"
  ExecWait '"$WINDIR\RUNDLL32.EXE" advpack.dll,LaunchINFSection .\${FILE},DefaultInstall'
!macroend

!macro UNZ ARCHIVE DEST
  DetailPrint "Decompression de ${ARCHIVE}..."
  ExecWait '"$APP\outils\7Z.EXE" x -y "-o${DEST}" "$APP\${ARCHIVE}"'
!macroend

!macro REG DIR FILE
  SetOutPath "$APP\${DIR}"
  ExecWait '"$WINDIR\REGEDIT.EXE" /s ${FILE}'
!macroend


;--------------------------------
; DirectX, MS Agent et outils systeme : communs au pack 1 et a l'ISO Win98FR.
; DirectX en premier (les sections s'executent dans l'ordre) : les
; 3DMark et les jeux en dependent.
SectionGroup /e "DirectX (une seule version)" GRP_DX
Section /o "DirectX 8.1" SEC_DX81
SectionEnd
Section /o "DirectX 8.2" SEC_DX82
SectionEnd
Section "DirectX 9.0c (decembre 2006)" SEC_DX9O
SectionEnd
SectionGroupEnd

Section "-DirectX" SEC_DX
  ${If} ${SectionIsSelected} ${SEC_DX81}
    SetOutPath "$APP\directx\dx81"
    ExecWait '"$APP\directx\dx81\DXSETUP.EXE" /silent'
  ${ElseIf} ${SectionIsSelected} ${SEC_DX82}
    SetOutPath "$APP\directx\dx82"
    ExecWait '"$APP\directx\dx82\DXSETUP.EXE" /silent'
  ${ElseIf} ${SectionIsSelected} ${SEC_DX9O}
    SetOutPath "$APP\directx\dx90c"
    ExecWait '"$APP\directx\dx90c\DXSETUP.EXE" /silent'
  ${Else}
    Return
  ${EndIf}
  SetRebootFlag true
SectionEnd

Section /o "MS Agent 2.0 (francais)" SEC_AGENT
  SetOutPath "$APP\msagent"
  ExecWait '"$APP\msagent\MSAGENT.EXE" /q:a /r:n'
  ExecWait '"$APP\msagent\AGTX040C.EXE" /q:a /r:n'
  SetRebootFlag true
SectionEnd

;--------------------------------
SectionGroup /e "Navigateurs" GRP_NAV

Section "Firefox 31.8 ESR (francais)" SEC_FF
  !insertmacro UNZ firefox\FIREFOX.7Z "C:\FIREFOX"
  !insertmacro INF firefox FIREFOX.INF
SectionEnd

SectionGroupEnd

;--------------------------------
SectionGroup /e "Multimedia" GRP_MM

Section "VLC 3.0.24 (francais, experimental)" SEC_VLC
  !insertmacro UNZ vlc\VLC.7Z "$PROGRAMFILES\VideoLAN\VLC"
  !insertmacro INF vlc VLC.INF
  !insertmacro REG vlc VLCKEX.REG
SectionEnd

SectionGroup /e "Winamp (une seule version)" GRP_WA
Section /o "Winamp 5.2 Standard (anglais)" SEC_WAS
SectionEnd
Section "Winamp 5.2 Full (anglais)" SEC_WAF
SectionEnd
Section /o "Winamp 2.91 (francais)" SEC_WA2
SectionEnd
SectionGroupEnd

Section "-Winamp" SEC_WA
  SetOutPath "$APP\winamp"
  ${If} ${SectionIsSelected} ${SEC_WAF}
    ExecWait '"$APP\winamp\WA52FULL.EXE" /S'
  ${ElseIf} ${SectionIsSelected} ${SEC_WAS}
    ExecWait '"$APP\winamp\WA52STD.EXE" /S'
  ${ElseIf} ${SectionIsSelected} ${SEC_WA2}
    ExecWait '"$APP\winamp\WINAMP29.EXE" /S'
    MessageBox MB_OK|MB_ICONINFORMATION "Winamp s'ouvre a la fin de son installation : repondez a sa question puis FERMEZ Winamp, et seulement ensuite cliquez sur OK (le patch francais doit remplacer ses fichiers)."
    ExecWait '"$APP\winamp\WAMPFR.EXE" /S'
  ${EndIf}
SectionEnd

Section /o "K-Lite Codec Pack 3.4.5" SEC_KL
  ExecWait '"$APP\klcodec\KLCP345F.EXE" /VERYSILENT /SP- /NORESTART'
SectionEnd

SectionGroupEnd

;--------------------------------
SectionGroup /e "Utilitaires" GRP_UT

Section "WinRAR 3.93 (francais)" SEC_RAR
  ExecWait '"$APP\winrar\WRAR393F.EXE" /s'
  Delete "$PROGRAMFILES\WinRAR\Vodelic_mode_d_emploi_video.html"
SectionEnd

Section "ImgBurn 2.5.8.0 (francais)" SEC_IMG
  ExecWait '"$APP\imgburn\IMGBURN.EXE" /S'
  CreateDirectory "$PROGRAMFILES\ImgBurn\Languages"
  CopyFiles /SILENT "$APP\imgburn\FRENCH.LNG" "$PROGRAMFILES\ImgBurn\Languages"
SectionEnd


Section "AIDA32 3.93" SEC_AIDA
  ExecWait '"$APP\aida32\AIDA393.EXE" /VERYSILENT /SP-'
SectionEnd

Section "CPU-Z 1.78" SEC_CPUZ
  !insertmacro INF cpuz CPUZ.INF
SectionEnd

Section "XnView 1.80" SEC_XNV
  ExecWait '"$APP\xnview\XNVIEW18.EXE" /VERYSILENT /SP-'
SectionEnd

Section "Foxit Reader 1.3 (anglais)" SEC_FOX
  !insertmacro INF foxit FOXIT.INF
SectionEnd

SectionGroupEnd


;--------------------------------
; Bureautique et Internet (logiciels du CD WIN98SE2024-Archives, ajoutes le
; 26/10/2026). OpenOffice : MSI extrait de l'installeur FR, sans le JRE 6
; (Java 6 ne s'installe pas sous 98) ni le module de langue (deja en francais).
SectionGroup /e "Bureautique et Internet" GRP_BUR

Section "OpenOffice.org 2.4.2 (francais)" SEC_OOO
  IfFileExists "$SYSDIR\MSIEXEC.EXE" ooo_msi
    DetailPrint "Windows Installer 2.0 absent : installation, puis redemarrage"
    ExecWait '"$APP\bureau\ooo\instmsia.exe" /q /c:"msiinst /delayrebootq"'
    SetRebootFlag true
    MessageBox MB_OK|MB_ICONINFORMATION "Windows Installer vient d'etre installe.$\r$\nApres le redemarrage, relancez le pack 2 et cochez seulement OpenOffice.org."
    Goto ooo_fin
  ooo_msi:
  DetailPrint "OpenOffice.org 2.4.2 : plusieurs minutes..."
  ExecWait '"$SYSDIR\MSIEXEC.EXE" /i "$APP\bureau\ooo\openofficeorg24.msi" /qb REMOVE=gm_o_Java REBOOT=ReallySuppress'
  ooo_fin:
SectionEnd

Section /o "AbiWord 2.2.7 + dictionnaire francais" SEC_ABI
  ExecWait '"$APP\bureau\abiword\ABIWORD.EXE" /S'
  ExecWait '"$APP\bureau\abiword\ABIDICFR.EXE" /S'
SectionEnd

Section /o "Spread32 (tableur leger)" SEC_SPR
  CreateDirectory "$PROGRAMFILES\Spread32"
  CopyFiles /SILENT "$APP\bureau\spread32\SPREAD32.EXE" "$PROGRAMFILES\Spread32"
  CreateDirectory "$SMPROGRAMS\Spread32"
  CreateShortCut "$SMPROGRAMS\Spread32\Spread32 (tableur).lnk" "$PROGRAMFILES\Spread32\SPREAD32.EXE"
SectionEnd

Section "Nvu 1.0 (pages web, francais)" SEC_NVU
  ExecWait '"$APP\bureau\nvu\NVUFR.EXE" /VERYSILENT /SP-'
  CreateDirectory "$PROGRAMFILES\Nvu\components\myspell"
  CopyFiles /SILENT "$APP\bureau\nvu\fr_FR\fr_FR.*" "$PROGRAMFILES\Nvu\components\myspell"
SectionEnd

Section "Flash Player 9 (IE et Firefox)" SEC_FLASH
  ExecWait '"$APP\bureau\flash\FP9IE.EXE" /S'
  ExecWait '"$APP\bureau\flash\FP9NS.EXE" /S'
SectionEnd

Section /o "UltimateZip 2.7 (anglais)" SEC_UZIP
  ExecWait '"$APP\bureau\uzip\UZIP.EXE" /VERYSILENT /SP-'
SectionEnd

Section /o "FTP Commander (anglais, installation guidee)" SEC_FTP
  ExecWait '"$APP\bureau\ftpcmd\FTPCMD.EXE"'
SectionEnd

SectionGroupEnd

;--------------------------------
SectionGroup "Outils systeme" GRP_SYS

Section /o "Console MMC 1.2 (anglais)" SEC_MMC
  !insertmacro INF systeme MMC.INF
SectionEnd

Section /o "RegClean (anglais)" SEC_REGCL
  !insertmacro INF systeme REGCLEAN.INF
SectionEnd

Section /o "SharedDLLs (anglais)" SEC_SHDLL
  !insertmacro INF systeme SHAREDLL.INF
SectionEnd

SectionGroupEnd

;--------------------------------
SectionGroup /e "Jeux (C:\Jeux)" GRP_JX

Section "Hover! (francais), SkiFree, Echecs" SEC_JX
  !insertmacro UNZ jeux\JEUX.7Z "C:\JEUX"
  !insertmacro INF jeux JEUX.INF
SectionEnd

Section "Microsoft Puzzle Collection (10 jeux)" SEC_PUZ
  !insertmacro UNZ puzzle\PUZZLE.7Z "C:\JEUX"
  !insertmacro REG puzzle PUZZLE.REG
  !insertmacro INF puzzle PUZZLE.INF
SectionEnd

SectionGroupEnd

;--------------------------------
SectionGroup "Outils de test (guides)" GRP_BN

Section "-Cles" SEC_CLES
  CopyFiles /SILENT "$APP\bench\CLES.TXT" "$WINDIR\BENCH_CLES.TXT"
SectionEnd

Section /o "3DMark99 Max" SEC_99
  Call OuvreCles
  DetailPrint "Cle : 78TR2-8DBDU-BMXXS (voir le Bloc-notes)"
  SetOutPath "$APP\bench"
  ExecWait '"$APP\bench\3DM99.EXE"'
SectionEnd

Section /o "3DMark2000" SEC_00
  Call OuvreCles
  DetailPrint "Cle : 6VZTY-SDZ75-KA9V7 (voir le Bloc-notes)"
  SetOutPath "$APP\bench"
  ExecWait '"$APP\bench\3DM2000.EXE"'
SectionEnd

Section /o "3DMark2001 SE" SEC_01
  Call OuvreCles
  DetailPrint "Cle : 7QMF2-TSLJR-ESRDD-L3FJF (voir le Bloc-notes)"
  SetOutPath "$APP\bench"
  ExecWait '"$APP\bench\3DM2001.EXE"'
SectionEnd

Section /o "3DMark03 3.4.0 (DirectX 9)" SEC_03
  Call OuvreCles
  DetailPrint "Cle : N4LWE-T6HUX-8U4JB-28YLV (voir le Bloc-notes)"
  SetOutPath "$APP\bench"
  ExecWait '"$APP\bench\3DM03.EXE"'
SectionEnd

SectionGroupEnd

;--------------------------------
; KernelEx (cache, execute en dernier : les sections doivent etre declarees
; avant d'etre testees ; les reglages KernelEx deja ecrits sont conserves)

Section "-KernelEx" SEC_KEX
  StrCpy $KEXNEW 0
  ${If} ${SectionIsSelected} ${SEC_FF}
  ${OrIf} ${SectionIsSelected} ${SEC_VLC}
    IfFileExists "$WINDIR\KERNELEX\KERNELEX.DLL" kex_ok
      DetailPrint "KernelEx 4.5.2019.24 FR absent : installation..."
      SetOutPath "$APP\kernelex"
      ExecWait '"$APP\kernelex\KEX2019.EXE" /S'
      ExecWait '"$WINDIR\REGEDIT.EXE" /s KEXOFF.REG'
      StrCpy $KEXNEW 1
      SetRebootFlag true
    kex_ok:
  ${EndIf}
SectionEnd

;--------------------------------
; Descriptions

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${GRP_DX} "Windows 98 SE a DirectX 6.1 d'origine (Windows Me : 7.1) ; la plupart des jeux exigent DirectX 8 ou 9. Decochez si DirectX est deja installe (CD 1 classique). Une seule version peut etre cochee."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_DX81} "DirectX 8.1. Une seule version de DirectX peut etre cochee : il ne revient jamais en arriere."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_DX82} "DirectX 8.2. Une seule version de DirectX peut etre cochee : il ne revient jamais en arriere."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_DX9O} "DirectX 9.0c officiel Microsoft (decembre 2006). Conseille. Pour les jeux qui buguent avec DirectX 9 (certains jeux Cryo : Egypte, Ubik...), prenez 8.1 ou 8.2."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_AGENT} "Microsoft Agent 2.0 + langue francaise : personnages animes (Merlin...) utilises par certains logiciels."
  !insertmacro MUI_DESCRIPTION_TEXT ${GRP_SYS} "Outils du SP3.0 et de Microsoft pour utilisateurs avertis."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_MMC} "Microsoft Management Console 1.2 (anglais)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_REGCL} "RegClean (anglais) : nettoyeur de registre Microsoft. Relisez toujours son rapport avant de valider."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_SHDLL} "ShareDlls Removal Tool (anglais) : nettoie les compteurs de DLL partagees."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_FF} "Firefox 31.8 ESR portable en francais, copie dans C:\FIREFOX. Page d'accueil DuckDuckGo Lite. Exige KernelEx (mode Windows XP SP3)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_VLC} "VLC 3.0.24 en francais, dans Program Files\VideoLAN\VLC. Exige KernelEx (mode XP SP3). Experimental : peut planter a la fermeture."
  !insertmacro MUI_DESCRIPTION_TEXT ${GRP_WA} "Decochez pour ne pas installer Winamp. Ouvrez le groupe pour choisir la version : une seule peut etre cochee."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_WAS} "Winamp 5.2 Standard (anglais) : lecteur, mediatheque, video. Une seule version de Winamp peut etre cochee."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_WAF} "Winamp 5.2 Full (anglais) : Standard + extraction et gravure de CD. Une seule version de Winamp peut etre cochee."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_WA2} "Winamp 2.91 + traduction francaise : leger. Une seule version de Winamp peut etre cochee."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_KL} "K-Lite Codec Pack 3.4.5 Full (selection par defaut) : codecs video, Media Player Classic, ffdshow."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_RAR} "WinRAR 3.93 en francais (shareware, essai 40 jours)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_IMG} "ImgBurn 2.5.8.0 (gravure) + traduction francaise."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_AIDA} "AIDA32 3.93 : informations systeme et tests memoire (francais)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_CPUZ} "CPU-Z 1.78 (version Windows 9x, anglais) : processeur, carte mere, barrettes de memoire, carte graphique. Menu Programmes\CPU-Z."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_XNV} "XnView 1.80 : visionneuse et convertisseur d'images (francais)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_FOX} "Foxit Reader 1.3 : lecteur PDF leger (anglais), dans Program Files\Foxit."
  !insertmacro MUI_DESCRIPTION_TEXT ${GRP_BUR} "Suite bureautique, traitement de texte, tableur, editeur de pages web, Flash, archives et FTP."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_OOO} "OpenOffice.org 2.4.2 en francais (texte, tableur, presentation, dessin, base de donnees), sans Java. Environ 350 Mo sur le disque, plusieurs minutes. Exige Windows Installer 2.0 (installe s'il manque, puis redemarrage)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_ABI} "AbiWord 2.2.7 : traitement de texte leger (ouvre les .doc), plus le dictionnaire francais."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_SPR} "Spread32 : petit tableur (ouvre les .xls), dans Program Files\Spread32, menu Programmes\Spread32."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_NVU} "Nvu 1.0 en francais : editeur de pages web visuel, avec le dictionnaire francais."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_FLASH} "Adobe Flash Player 9 (9.0.277) pour Internet Explorer et pour Firefox / RetroZilla."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_UZIP} "UltimateZip 2.7 (anglais) : gestionnaire d'archives. 7-Zip est deja installe par le pack 1. UltimateZip s'ouvre apres l'installation et propose de prendre les archives : repondez No pour les laisser a 7-Zip."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_FTP} "FTP Commander (gratuit, anglais) : client FTP. Installation guidee : son installeur n'a pas de mode silencieux (cochez I agree, puis Next)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_JX} "Hover! en francais (CD Windows 95), SkiFree et Echecs (anglais), dans C:\Jeux, menu Programmes\Jeux."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_PUZ} "Microsoft The Puzzle Collection en francais (10 jeux), dans C:\Jeux\Puzzle Collection, menu Programmes\Jeux. Exige 256 couleurs pour jouer."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_99} "3DMark99 Max (DirectX 6). Installation guidee, les cles s'ouvrent dans le Bloc-notes (copiables)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_00} "3DMark2000 (DirectX 7). Installation guidee, les cles s'ouvrent dans le Bloc-notes (copiables)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_01} "3DMark2001 SE (DirectX 8). Exige 16 bits de couleurs ou plus."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_03} "3DMark03 3.4.0 : exige DirectX 9.0b ou 9.0c (valide sous 98 sans KernelEx)."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------

Function .onInit
  StrCpy $APP "$EXEDIR\applis"
  IfFileExists "$APP\kernelex\KEX2019.EXE" ok
  StrCpy $APP "$EXEDIR\..\Win98FR_Plus\applis"
  IfFileExists "$APP\kernelex\KEX2019.EXE" ok
    MessageBox MB_OK|MB_ICONSTOP "Dossier applis du pack 2 introuvable.$\r$\nPlacez INSTALLER_PLUS.EXE a la racine du pack 2 (a cote du dossier applis)."
    Abort
  ok:
  GetFullPathName $APP $APP
  StrCpy $WARADIO ${SEC_WAF}
  StrCpy $WANB 1
  StrCpy $CLESOUV 0
  StrCpy $DXRADIO ${SEC_DX9O}
  StrCpy $DXNB 1
FunctionEnd

; Winamp et DirectX : une seule version. Une version de plus cochee d'un
; clic = elle remplace l'ancienne ; groupe entier coche = on garde la
; derniere version retenue (par defaut Winamp 5.2 Full, DirectX 9.0c officiel).
!macro RADIO_COMPTE SEC RADIO
  ${If} ${SectionIsSelected} ${SEC}
    IntOp $R0 $R0 + 1
    ${If} ${SEC} != ${RADIO}
      StrCpy $R1 ${SEC}
    ${EndIf}
  ${EndIf}
!macroend

Function .onSelChange
  Push $R0
  Push $R1
  StrCpy $R0 0
  StrCpy $R1 -1
  !insertmacro RADIO_COMPTE ${SEC_DX81} $DXRADIO
  !insertmacro RADIO_COMPTE ${SEC_DX82} $DXRADIO
  !insertmacro RADIO_COMPTE ${SEC_DX9O} $DXRADIO
  ${If} $R0 > 1
    ${If} $DXNB == 1
    ${AndIf} $R0 == 2
      StrCpy $DXRADIO $R1
    ${EndIf}
    !insertmacro UnselectSection ${SEC_DX81}
    !insertmacro UnselectSection ${SEC_DX82}
    !insertmacro UnselectSection ${SEC_DX9O}
    !insertmacro SelectSection $DXRADIO
    StrCpy $R0 1
  ${ElseIf} $R0 == 1
  ${AndIf} $R1 != -1
    StrCpy $DXRADIO $R1
  ${EndIf}
  StrCpy $DXNB $R0

  StrCpy $R0 0
  StrCpy $R1 -1
  !insertmacro RADIO_COMPTE ${SEC_WAS} $WARADIO
  !insertmacro RADIO_COMPTE ${SEC_WAF} $WARADIO
  !insertmacro RADIO_COMPTE ${SEC_WA2} $WARADIO
  ${If} $R0 > 1
    ${If} $WANB == 1
    ${AndIf} $R0 == 2
      StrCpy $WARADIO $R1
    ${EndIf}
    !insertmacro UnselectSection ${SEC_WAS}
    !insertmacro UnselectSection ${SEC_WAF}
    !insertmacro UnselectSection ${SEC_WA2}
    !insertmacro SelectSection $WARADIO
    StrCpy $R0 1
  ${ElseIf} $R0 == 1
  ${AndIf} $R1 != -1
    StrCpy $WARADIO $R1
  ${EndIf}
  StrCpy $WANB $R0
  Pop $R1
  Pop $R0
FunctionEnd

; Cles des 3DMark dans le Bloc-notes : copiables, et l'installation du
; 3DMark demarre sans attendre la fermeture de la fenetre (test GX240).
Function OuvreCles
  StrCmp $CLESOUV 1 +3
  Exec 'notepad.exe "$WINDIR\BENCH_CLES.TXT"'
  StrCpy $CLESOUV 1
FunctionEnd
