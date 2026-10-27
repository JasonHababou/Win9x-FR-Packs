' Pack Win98FR : raccourci "Commandes MS-DOS" du menu Demarrer remplace par
' CMDMSDOS.PIF (meme PIF, avec les parametres /K C:\WINDOWS\CLAVDOS.BAT) : la
' fenetre MS-DOS charge le clavier francais ou belge en s'ouvrant.
Option Explicit
Dim SH, FSO, src, dst
Set SH = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
If LCase(SH.ExpandEnvironmentStrings("%windir%")) = "c:\windows" Then
    src = FSO.GetParentFolderName(WScript.ScriptFullName) & "\CMDMSDOS.PIF"
    dst = SH.SpecialFolders("Programs") & "\Commandes MS-DOS.pif"
    If FSO.FileExists(dst) Then FSO.GetFile(dst).Attributes = 0
    FSO.CopyFile src, dst, True
    FSO.GetFile(dst).Attributes = 32
End If
