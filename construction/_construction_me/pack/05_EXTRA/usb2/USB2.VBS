' Pack WinMeFR : USB 2.0 (module officiel Microsoft 4.90.3000.10 pour 98 SE et ME,
' fourni avec QuickInstall). Les fichiers vont dans C:\WINDOWS\OPTIONS\USB2 et
' OtherDevicePath y pointe : Windows y trouve USB2.INF des qu'il detecte un
' controleur USB 2.0 (meme methode que QuickInstall avec C:\DRIVER).
Option Explicit
Dim FSO, SH, src, dest, f, j
Set FSO = CreateObject("Scripting.FileSystemObject")
Set SH = CreateObject("WScript.Shell")
Set j = FSO.OpenTextFile("C:\WMEFR\JOURNAL.TXT", 8, True)
src = FSO.GetParentFolderName(WScript.ScriptFullName)
dest = SH.ExpandEnvironmentStrings("%windir%") & "\OPTIONS"
If Not FSO.FolderExists(dest) Then FSO.CreateFolder dest
dest = dest & "\USB2"
If Not FSO.FolderExists(dest) Then FSO.CreateFolder dest
For Each f In FSO.GetFolder(src).Files
    If UCase(FSO.GetExtensionName(f.Name)) <> "VBS" Then f.Copy dest & "\" & f.Name, True
Next
SH.RegWrite "HKLM\Software\Microsoft\Windows\CurrentVersion\OtherDevicePath", dest, "REG_SZ"
j.WriteLine "USB2 : pilotes dans " & dest & ", OtherDevicePath regle"
j.Close
