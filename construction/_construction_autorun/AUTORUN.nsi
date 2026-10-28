; ============================================================
; AUTORUN.nsi - lanceur des CD Win98FR (NSIS 2.46, cp1252)
;   makensis /DPACK=1 AUTORUN.nsi  -> CD 1 (Win98FR_v2)   : INSTALL.BAT
;   makensis /DPACK=2 AUTORUN.nsi  -> CD 2 (Win98FR_Plus) : INSTALLER_PLUS.EXE / PLUS.BAT
;   makensis /DPACK=3 AUTORUN.nsi  -> CD correctif Windows Me (WinMeFR) : INSTALL.BAT
; Fonctionne aussi depuis un dossier du disque dur : tout est lance
; depuis le dossier de AUTORUN.EXE.
; ============================================================

  !include "nsDialogs.nsh"
  !include "LogicLib.nsh"
  !include "WinMessages.nsh"

  !ifndef PACK
    !define PACK 1
  !endif

  !if ${PACK} == 1
    Name "Windows 98 SE FR"
    Caption "Windows 98 SE FR - CD 1 : installation de base"
  !else if ${PACK} == 3
    Name "Windows Me FR"
    Caption "Windows Me FR - pack correctif"
  !else
    Name "Windows 98 SE FR"
    Caption "Windows 98 SE / Me FR - CD 2 : logiciels, jeux et outils"
  !endif
  OutFile "AUTORUN.EXE"
  SetCompressor /SOLID lzma
  RequestExecutionLevel user
  BrandingText " "
  XPStyle on

  Var DLG

  Page custom Menu

Function Menu
  GetDlgItem $0 $HWNDPARENT 1
  ShowWindow $0 ${SW_HIDE}
  GetDlgItem $0 $HWNDPARENT 3
  ShowWindow $0 ${SW_HIDE}
  GetDlgItem $0 $HWNDPARENT 2
  SendMessage $0 ${WM_SETTEXT} 0 "STR:Quitter"

  nsDialogs::Create 1018
  Pop $DLG

!if ${PACK} == 1
  ${NSD_CreateLabel} 0 0 100% 54u "Pack Windows 98 SE FR « ultime » : correctifs, Service Pack 3.0, Internet Explorer, extras, DirectX, .NET, pilotes chipset et applications essentielles.$\r$\n$\r$\nL'installation redémarre Windows plusieurs fois et reprend toute seule. Laissez ce CD dans le lecteur jusqu'à la fin."
  Pop $0
  ${NSD_CreateButton} 15% 58u 70% 18u "Installer Windows 98 SE FR"
  Pop $0
  ${NSD_OnClick} $0 Installer
  ${NSD_SetFocus} $0
  ${NSD_CreateButton} 15% 80u 70% 18u "Lisez-moi"
  Pop $0
  ${NSD_OnClick} $0 LisezMoi
  ${NSD_CreateLabel} 0 104u 100% 30u "Ensuite : installez les pilotes (carte graphique, son), puis insérez le CD 2 pour les logiciels, les jeux et les outils de test."
  Pop $0
!else if ${PACK} == 3
  ${NSD_CreateLabel} 0 0 100% 54u "Pack Windows Me FR : correctifs, Me SP 2.02 (non officiel), Internet Explorer 6 SP1, Media Player 9, MDAC 2.8, .NET 1.1, pilotes chipset, vrai mode MS-DOS et applications essentielles.$\r$\n$\r$\nL'installation redémarre Windows plusieurs fois et reprend toute seule. Laissez ce CD dans le lecteur jusqu'à la fin."
  Pop $0
  ${NSD_CreateButton} 15% 58u 70% 18u "Installer le pack Windows Me FR"
  Pop $0
  ${NSD_OnClick} $0 Installer
  ${NSD_SetFocus} $0
  ${NSD_CreateButton} 15% 80u 70% 18u "Lisez-moi"
  Pop $0
  ${NSD_OnClick} $0 LisezMoi
  ${NSD_CreateLabel} 0 104u 100% 30u "Ensuite : installez les pilotes (carte graphique, son), puis insérez le CD du pack 2 pour les logiciels, les jeux et les outils de test."
  Pop $0
!else
  ${NSD_CreateLabel} 0 0 100% 36u "Logiciels, jeux et outils de test pour Windows 98 SE et Windows Me.$\r$\nA lancer APRES l'installation de base (CD 1) et APRES les pilotes : certains jeux et tests exigent 256 couleurs ou plus."
  Pop $0
  ${NSD_CreateButton} 15% 42u 70% 18u "Installer (cases à cocher)"
  Pop $0
  ${NSD_OnClick} $0 Installer
  ${NSD_SetFocus} $0
  ${NSD_CreateButton} 15% 64u 70% 18u "Installer (questions O/N, MS-DOS)"
  Pop $0
  ${NSD_OnClick} $0 InstallerBat
  ${NSD_CreateButton} 15% 86u 70% 18u "Lisez-moi"
  Pop $0
  ${NSD_OnClick} $0 LisezMoi
!endif

  nsDialogs::Show
FunctionEnd

Function Quitter
  SendMessage $HWNDPARENT ${WM_COMMAND} 2 0
FunctionEnd

Function Installer
  Pop $0
  SetOutPath "$EXEDIR"
!if ${PACK} != 2
  ReadEnvStr $1 COMSPEC
  Exec '"$1" /c INSTALL.BAT'
!else
  Exec '"$EXEDIR\INSTALLER_PLUS.EXE"'
!endif
  Call Quitter
FunctionEnd

Function InstallerBat
  Pop $0
  SetOutPath "$EXEDIR"
  ReadEnvStr $1 COMSPEC
  Exec '"$1" /c PLUS.BAT'
  Call Quitter
FunctionEnd

Function LisezMoi
  Pop $0
  ExecShell "open" "$EXEDIR\LISEZMOI.TXT"
FunctionEnd

Section
SectionEnd
