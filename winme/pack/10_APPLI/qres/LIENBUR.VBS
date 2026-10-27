' Pack Win98FR : raccourci "Raccourci de jeu (affichage et carte son)" sur le Bureau
' (outil QRESJEUX.HTA : jeu dans son mode d'affichage et, au choix, sur une autre carte son)
Option Explicit
Dim SH, FSO, l, hta
Set SH = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
hta = SH.ExpandEnvironmentStrings("%windir%") & "\QRESJEUX.HTA"
If FSO.FileExists(hta) Then
    Set l = SH.CreateShortcut(SH.SpecialFolders("Desktop") & "\Raccourci de jeu (affichage et carte son).lnk")
    l.TargetPath = hta
    l.IconLocation = SH.ExpandEnvironmentStrings("%windir%") & "\MODEAFF.EXE,0"
    l.Description = "Cree un raccourci de jeu : mode d'affichage et carte son pendant le jeu"
    l.Save
End If
