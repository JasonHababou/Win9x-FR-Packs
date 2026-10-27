; ============================================================
; MODEAFF.nsi - Pack Win98FR : change le mode d'affichage le temps d'un jeu
; (remplace QRes dans les raccourcis de jeu : apres QRes, le curseur
; disparaissait du Bureau jusqu'au redemarrage, test GX240 2026-10-16 ;
; le meme changement fait a la main ne posait pas ce probleme).
; Appelle directement ChangeDisplaySettingsA de Windows, sans mise a jour
; du registre : le mode du Bureau (registre) n'est jamais modifie.
;   MODEAFF x=640 y=480 c=8   passe en 640 x 480, 256 couleurs
;   MODEAFF c=16              change seulement les couleurs
;   MODEAFF /R                revient au mode du Bureau (registre)
;   MODEAFF /I                ecrit le mode actuel dans %TEMP%\MODEAFF.TXT
; Code de sortie : 0 = fait, 1 = redemarrage exige, 2 = mode refuse.
; Compilation : makensis MODEAFF.nsi (NSIS 2.46, fichier en cp1252)
; ============================================================

  !include "FileFunc.nsh"
  !insertmacro GetParameters
  !insertmacro GetOptions

  Name "ModeAff"
  OutFile "MODEAFF.EXE"
  SilentInstall silent
  RequestExecutionLevel user
  Icon "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"

  !define DM_BITSPERPEL 0x00040000
  !define DM_PELSWIDTH  0x00080000
  !define DM_PELSHEIGHT 0x00100000

Section
  ${GetParameters} $0

  ; --- Retour au mode du Bureau
  ${GetOptions} $0 "/R" $9
  IfErrors 0 restaure

  ; --- DEVMODEA (156 octets) rempli avec le mode actuel
  System::Alloc 156
  Pop $1
  IntOp $2 $1 + 36
  System::Call "*$2(&i2 156)"
  System::Call "user32::EnumDisplaySettingsA(i 0, i -1, i r1) i .r3"
  IntCmp $3 0 0 lu lu
    System::Call "user32::EnumDisplaySettingsA(i 0, i -2, i r1) i .r3"
  lu:

  ${GetOptions} $0 "/I" $9
  IfErrors change
    IntOp $2 $1 + 104
    System::Call "*$2(i .r4, i .r5, i .r6)"
    FileOpen $7 "$TEMP\MODEAFF.TXT" w
    FileWrite $7 "x=$5 y=$6 c=$4$\r$\n"
    FileClose $7
    System::Free $1
    Goto fin

  change:
  StrCpy $8 0
  ${GetOptions} $0 "x=" $4
  IfErrors +4
    IntOp $2 $1 + 108
    System::Call "*$2(i r4)"
    IntOp $8 $8 | ${DM_PELSWIDTH}
  ${GetOptions} $0 "y=" $4
  IfErrors +4
    IntOp $2 $1 + 112
    System::Call "*$2(i r4)"
    IntOp $8 $8 | ${DM_PELSHEIGHT}
  ${GetOptions} $0 "c=" $4
  IfErrors +4
    IntOp $2 $1 + 104
    System::Call "*$2(i r4)"
    IntOp $8 $8 | ${DM_BITSPERPEL}
  IntOp $2 $1 + 40
  System::Call "*$2(i r8)"
  System::Call "user32::ChangeDisplaySettingsA(i r1, i 0) i .r3"
  System::Free $1
  Goto resultat

  restaure:
  System::Call "user32::ChangeDisplaySettingsA(i 0, i 0) i .r3"

  resultat:
  IntCmp $3 0 fin
  IntCmp $3 1 0 refuse refuse
    SetErrorLevel 1
    Goto fin
  refuse:
    SetErrorLevel 2
  fin:
SectionEnd
