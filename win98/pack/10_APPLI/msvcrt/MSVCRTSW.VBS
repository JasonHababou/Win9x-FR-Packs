' ============================================================
' MSVCRTSW.VBS - Pack Win98FR : bascule de la bibliotheque C de Windows
' (SYSTEM\MSVCRT.DLL) entre deux versions, d'un double-clic :
'   6.1 (SP3.0 FR) : celle de Windows 98 a jour. A garder pour INSTALLER
'                    des programmes : avec la 7.0, les installations de
'                    K-Lite 3.4.5 et de 3DMark 2001 SE se bloquaient.
'   7.0 (U98SESP3.66, issue de Windows XP) : VLC ne plante plus a la
'                    fermeture (test Dell GX240, 2026-10-17).
' Le fichier est en service : remplacement au prochain demarrage par
' WININIT.INI [rename], comme le correctif NVIDIA.
' Versions gardees dans WINDOWS\MSVCRT (MSVCRT61.DLL et MSVCRT70.DLL).
' Modes : double-clic = bascule ; /installe (INSTALL.BAT) = copie les
' fichiers et cree le raccourci "MSVCRT 6.1 - 7.0" sur le Bureau.
' ============================================================
Set FSO = CreateObject("Scripting.FileSystemObject")
Set SH = CreateObject("WScript.Shell")
ici = FSO.GetParentFolderName(WScript.ScriptFullName)
win = FSO.GetSpecialFolder(0).Path
sys = FSO.GetSpecialFolder(1).Path
dest = win & "\MSVCRT"
actuel = sys & "\MSVCRT.DLL"
titre = "Bibliotheque C de Windows (MSVCRT)"

If WScript.Arguments.Count > 0 Then
    If LCase(WScript.Arguments(0)) = "/installe" Then Installer
End If

v = FSO.GetFileVersion(actuel)
If Left(v, 2) = "7." Then
    cible = "MSVCRT61.DLL": nouv = "6.1"
    txt = "Version actuelle : " & v & " (Windows XP, via la 3.66)." & vbCrLf & vbCrLf & _
          "Passer a la version 6.1 du SP3.0 ?" & vbCrLf & _
          "A faire AVANT d'installer des programmes (K-Lite, 3DMark 2001...)."
Else
    cible = "MSVCRT70.DLL": nouv = "7.0"
    txt = "Version actuelle : " & v & " (SP3.0)." & vbCrLf & vbCrLf & _
          "Passer a la version 7.0 (Windows XP, via la 3.66) ?" & vbCrLf & _
          "VLC ne plante plus a la fermeture. Revenez a la 6.1 avant" & vbCrLf & _
          "d'installer des programmes."
End If
If Not FSO.FileExists(dest & "\" & cible) Then
    MsgBox "Fichier introuvable : " & dest & "\" & cible, 16, titre
    WScript.Quit
End If

ini = win & "\WININIT.INI"
If InStr(1, Lire(ini), "\NOUVEAU.DLL", 1) > 0 Then
    MsgBox "Un changement de version attend deja le prochain demarrage." & vbCrLf & _
           "Redemarrez Windows pour le terminer.", 64, titre
    WScript.Quit
End If
If MsgBox(txt, 4 + 32, titre) <> 6 Then WScript.Quit

FSO.CopyFile dest & "\" & cible, dest & "\NOUVEAU.DLL", True
' WININIT.INI n'accepte que des noms courts (8.3)
ligne = FSO.GetFile(actuel).ShortPath & "=" & FSO.GetFile(dest & "\NOUVEAU.DLL").ShortPath
texte = Lire(ini)
p = InStr(1, texte, "[rename]", 1)
If p > 0 Then
    p = p + Len("[rename]")
    texte = Left(texte, p - 1) & vbCrLf & ligne & Mid(texte, p)
Else
    If Len(texte) > 0 And Right(texte, 2) <> vbCrLf Then texte = texte & vbCrLf
    texte = texte & "[rename]" & vbCrLf & ligne & vbCrLf
End If
Set t = FSO.CreateTextFile(ini, True)
t.Write texte
t.Close
Journal "MSVCRT : passage de " & v & " a " & nouv & " au prochain demarrage"

If MsgBox("La version " & nouv & " sera en place apres le redemarrage." & vbCrLf & _
          "Redemarrer maintenant ?", 4 + 32, titre) = 6 Then
    SH.Run "RUNDLL32.EXE SHELL32.DLL,SHExitWindowsEx 2", 0, False
End If
WScript.Quit

' --- /installe : versions dans WINDOWS\MSVCRT + raccourci sur le Bureau
Sub Installer()
    If Not FSO.FolderExists(dest) Then FSO.CreateFolder dest
    FSO.CopyFile ici & "\MSVCRTSW.VBS", dest & "\MSVCRTSW.VBS", True
    FSO.CopyFile ici & "\MSVCRT70.DLL", dest & "\MSVCRT70.DLL", True
    ' la 6.1 = celle du systeme a ce moment (SP3.0) ; jamais ecrasee ensuite
    If Not FSO.FileExists(dest & "\MSVCRT61.DLL") Then
        If Left(FSO.GetFileVersion(actuel), 2) = "6." Then FSO.CopyFile actuel, dest & "\MSVCRT61.DLL"
    End If
    Set l = SH.CreateShortcut(SH.SpecialFolders("Desktop") & "\MSVCRT 6.1 - 7.0.lnk")
    l.TargetPath = win & "\WSCRIPT.EXE"
    l.Arguments = FSO.GetFolder(dest).ShortPath & "\MSVCRTSW.VBS"
    l.WorkingDirectory = dest
    l.IconLocation = sys & "\SHELL32.DLL,21"
    l.Description = "Bascule la bibliotheque C de Windows entre 6.1 et 7.0"
    l.Save
    Journal "MSVCRT : outil de bascule installe (" & dest & ", raccourci sur le Bureau)"
    WScript.Quit
End Sub

Function Lire(chemin)
    Lire = ""
    If Not FSO.FileExists(chemin) Then Exit Function
    Set f = FSO.OpenTextFile(chemin, 1)
    If Not f.AtEndOfStream Then Lire = f.ReadAll
    f.Close
End Function

Sub Journal(texte)
    If Not FSO.FolderExists("C:\W98FR") Then Exit Sub
    Set j = FSO.OpenTextFile("C:\W98FR\JOURNAL.TXT", 8, True)
    j.WriteLine texte
    j.Close
End Sub
