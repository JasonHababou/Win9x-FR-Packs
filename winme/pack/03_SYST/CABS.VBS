' Pack WinMeFR : fichiers du CD de Windows Me (dossier WIN9X) dans
' C:\WINDOWS\OPTIONS\CABS, puis les deux SourcePath du registre y pointent.
' Windows et les installeurs de pilotes y trouvent ainsi tout, y compris les
' fichiers deja deposes la par le Me SP (CD inutile, plus de "fichier introuvable").
' Source cherchee : dossier WIN9X a cote du pack, puis X:\WIN9X sur chaque lecteur,
' puis C:\WIN9X (ancienne methode, deplace ensuite). Journal : C:\WMEFR\JOURNAL.TXT
Option Explicit
Dim FSO, SH, dest, src, d, j, pack, nb
Set FSO = CreateObject("Scripting.FileSystemObject")
Set SH = CreateObject("WScript.Shell")
Set j = FSO.OpenTextFile("C:\WMEFR\JOURNAL.TXT", 8, True)
dest = SH.ExpandEnvironmentStrings("%windir%") & "\OPTIONS\CABS"
src = ""
pack = FSO.GetParentFolderName(FSO.GetParentFolderName(WScript.ScriptFullName))
If FSO.FileExists(FSO.GetParentFolderName(pack) & "\WIN9X\PRECOPY1.CAB") Then
    src = FSO.GetParentFolderName(pack) & "\WIN9X"
End If
If src = "" Then
    For Each d In FSO.Drives
        If d.IsReady Then
            If FSO.FileExists(d.DriveLetter & ":\WIN9X\PRECOPY1.CAB") Then
                If UCase(d.DriveLetter) <> "C" Then src = d.DriveLetter & ":\WIN9X"
            End If
        End If
        If src <> "" Then Exit For
    Next
End If
If src = "" And FSO.FileExists("C:\WIN9X\PRECOPY1.CAB") Then src = "C:\WIN9X"
If src = "" Then
    j.WriteLine "CABS : dossier WIN9X du CD introuvable, rien copie"
    WScript.Quit 1
End If
If Not FSO.FolderExists(SH.ExpandEnvironmentStrings("%windir%") & "\OPTIONS") Then
    FSO.CreateFolder SH.ExpandEnvironmentStrings("%windir%") & "\OPTIONS"
End If
If Not FSO.FolderExists(dest) Then FSO.CreateFolder dest
nb = 0
Dim f
For Each f In FSO.GetFolder(src).Files
    If Not FSO.FileExists(dest & "\" & f.Name) Then
        f.Copy dest & "\" & f.Name, False
        nb = nb + 1
    End If
Next
j.WriteLine "CABS : " & nb & " fichiers copies de " & src & " vers " & dest
' Les deux SourcePath (Setup et CurrentVersion) : chemin avec \ final
SH.RegWrite "HKLM\Software\Microsoft\Windows\CurrentVersion\Setup\SourcePath", dest & "\", "REG_SZ"
SH.RegWrite "HKLM\Software\Microsoft\Windows\CurrentVersion\SourcePath", dest & "\", "REG_SZ"
j.WriteLine "CABS : SourcePath = " & dest & "\"
' Ancienne methode (C:\WIN9X) : deplacee dans C:\WMEFR\BAK, pas supprimee
If LCase(src) = "c:\win9x" Then
    If Not FSO.FolderExists("C:\WMEFR\BAK\WIN9X") Then
        FSO.MoveFolder "C:\WIN9X", "C:\WMEFR\BAK\WIN9X"
        j.WriteLine "CABS : ancien C:\WIN9X deplace dans C:\WMEFR\BAK\WIN9X"
    End If
End If
j.Close
