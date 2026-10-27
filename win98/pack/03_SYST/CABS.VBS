' Pack Win98FR : fichiers du CD de Windows 98 (dossier WIN98 de l'ISO Win98FR, ou
' WIN9X) dans C:\WINDOWS\OPTIONS\CABS, puis les deux SourcePath du registre y
' pointent : Windows et les installeurs de pilotes y trouvent tout, sans le CD
' (plus de "fichier introuvable" ni de demande du CD, retours GX240 2026-10-21).
' Source cherchee : dossier a cote du pack, puis X:\WIN98 et X:\WIN9X sur chaque
' lecteur, puis C:\WIN9X (ancienne methode, deplace ensuite dans C:\W98FR\BAK).
' Journal : C:\W98FR\JOURNAL.TXT. Repris du pack WinMeFR (CABS.VBS, 2026-10-26).
Option Explicit
Dim FSO, SH, dest, src, d, j, pack, nb, n, f
Set FSO = CreateObject("Scripting.FileSystemObject")
Set SH = CreateObject("WScript.Shell")
Set j = FSO.OpenTextFile("C:\W98FR\JOURNAL.TXT", 8, True)
dest = SH.ExpandEnvironmentStrings("%windir%") & "\OPTIONS\CABS"
src = ""
pack = FSO.GetParentFolderName(FSO.GetParentFolderName(WScript.ScriptFullName))
For Each n In Array("WIN98", "WIN9X")
    If src = "" And FSO.FileExists(FSO.GetParentFolderName(pack) & "\" & n & "\PRECOPY1.CAB") Then
        src = FSO.GetParentFolderName(pack) & "\" & n
    End If
    If src = "" And FSO.FileExists(pack & "\" & n & "\PRECOPY1.CAB") Then src = pack & "\" & n
Next
If src = "" Then
    For Each d In FSO.Drives
        If d.IsReady And UCase(d.DriveLetter) <> "C" Then
            For Each n In Array("WIN98", "WIN9X")
                If src = "" And FSO.FileExists(d.DriveLetter & ":\" & n & "\PRECOPY1.CAB") Then
                    src = d.DriveLetter & ":\" & n
                End If
            Next
        End If
        If src <> "" Then Exit For
    Next
End If
If src = "" And FSO.FileExists("C:\WIN9X\PRECOPY1.CAB") Then src = "C:\WIN9X"
If src = "" Then
    j.WriteLine "CABS : dossier WIN98 / WIN9X du CD introuvable, rien copie"
    WScript.Quit 1
End If
If Not FSO.FolderExists(SH.ExpandEnvironmentStrings("%windir%") & "\OPTIONS") Then
    FSO.CreateFolder SH.ExpandEnvironmentStrings("%windir%") & "\OPTIONS"
End If
If Not FSO.FolderExists(dest) Then FSO.CreateFolder dest
nb = 0
For Each f In FSO.GetFolder(src).Files
    If Not FSO.FileExists(dest & "\" & f.Name) Then
        f.Copy dest & "\" & f.Name, False
        nb = nb + 1
    End If
Next
j.WriteLine "CABS : " & nb & " fichiers copies de " & src & " vers " & dest
SH.RegWrite "HKLM\Software\Microsoft\Windows\CurrentVersion\Setup\SourcePath", dest & "\", "REG_SZ"
SH.RegWrite "HKLM\Software\Microsoft\Windows\CurrentVersion\SourcePath", dest & "\", "REG_SZ"
j.WriteLine "CABS : SourcePath = " & dest & "\"
If LCase(src) = "c:\win9x" Then
    If Not FSO.FolderExists("C:\W98FR\BAK\WIN9X") Then
        If Not FSO.FolderExists("C:\W98FR\BAK") Then FSO.CreateFolder "C:\W98FR\BAK"
        FSO.MoveFolder "C:\WIN9X", "C:\W98FR\BAK\WIN9X"
        j.WriteLine "CABS : ancien C:\WIN9X deplace dans C:\W98FR\BAK\WIN9X"
    End If
End If
j.Close
