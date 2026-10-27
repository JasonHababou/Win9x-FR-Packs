' ============================================================
' Correctif d'arret des pilotes NVIDIA 81.85 / 81.98 / 82.16 / 82.69
' (GeForce 6 a 9 : "Erreur de protection Windows" a l'arret).
'
' 1. NVCORE.VXD : remplace par la version corrigee (correctif de
'    R. Loew et Drugwash, MSFN 174096, mode "Full (c)" de
'    ShutdownPatcher ; valide sur Dell GX240 + 81.98, 2026-10-16).
'    Le fichier est en service : remplacement au prochain demarrage
'    par WININIT.INI [rename].
' 2. NVUDISP.EXE (desinstalleur, plante avec les 81.x / 82.x) :
'    remplace par celui de la 77.72.
'
' Version reconnue par la taille de SYSTEM\NVCORE.VXD ; deja corrige
' si l'appel detourne contient C2 05 00 00. Originaux dans
' C:\W98FR\BAK. Sans danger si relance, ou sans pilote NVIDIA.
'
' Modes :
'   (aucun)     double-clic : message a la fin
'   /installe   INSTALL.BAT : copie l'outil dans WINDOWS\NVFIX, retire la
'               cle Run NVFIX si elle existe, puis verifie
'   /surveille  idem, mais lance aussi l'outil a chaque demarrage (cle
'               Run NVFIX) : choix de l'utilisateur en fin de pack
'   /demarrage  cle Run : silencieux ; ne fait rien si NVCORE.VXD n'a
'               pas change depuis la derniere fois ; message seulement
'               si un correctif vient d'etre pose (pilote installe
'               apres le pack)
' ============================================================
Set FSO = CreateObject("Scripting.FileSystemObject")
mode = ""
If WScript.Arguments.Count > 0 Then mode = LCase(WScript.Arguments(0))
ici = FSO.GetParentFolderName(WScript.ScriptFullName)
win = FSO.GetSpecialFolder(0).Path
sys = FSO.GetSpecialFolder(1).Path
dest = win & "\NVFIX"
bak = "C:\W98FR\BAK"
If Not FSO.FolderExists("C:\W98FR") Then FSO.CreateFolder "C:\W98FR"
If Not FSO.FolderExists(bak) Then FSO.CreateFolder bak

msg = ""
pose = False
nv = sys & "\NVCORE.VXD"
If mode = "/installe" Or mode = "/surveille" Then Installer

' --- Demarrage : rien a faire si NVCORE.VXD est le meme que la derniere fois
empreinte = "absent"
If FSO.FileExists(nv) Then empreinte = FSO.GetFile(nv).Size & " " & FSO.GetFile(nv).DateLastModified
If mode = "/demarrage" Then
    If Lire(dest & "\DERNIER.TXT") = empreinte Then WScript.Quit
End If

If Not FSO.FileExists(nv) Then Fin "Aucun pilote NVIDIA installe : rien a faire."

taille = FSO.GetFile(nv).Size
Select Case taille
    Case 3269725: ver = "81.85": pos = &H31DBF6: orig = "9662E5FF": cor = "N8185.VXD"
    Case 3275869: ver = "81.98": pos = &H31F35E: orig = "9E55E5FF": cor = "N8198.VXD"
    Case 3276893: ver = "82.16": pos = &H31F6E6: orig = "E654E5FF": cor = "N8216.VXD"
    Case 3317853: ver = "82.69": pos = &H329802: orig = "DAA7E4FF": cor = "N8269.VXD"
    Case Else
        Fin "Pilote NVIDIA non concerne (NVCORE.VXD de " & taille & " octets)." _
            & vbCrLf & "La 77.72 et les versions plus anciennes n'ont pas le bug d'arret."
End Select
Note "Pilote NVIDIA " & ver & " detecte."

etat = Octets(nv, pos, 4)
If etat = "C2050000" Then
    Note "Correctif d'arret : deja en place."
ElseIf etat = orig Then
    If Not FSO.FileExists(bak & "\NVCORE.VXD") Then FSO.CopyFile nv, bak & "\NVCORE.VXD"
    FSO.CopyFile ici & "\" & cor, "C:\W98FR\NVCORE.NEW", True
    Renommer FSO.GetFile(nv).ShortPath, FSO.GetFile("C:\W98FR\NVCORE.NEW").ShortPath
    Note "Correctif d'arret : pose au prochain demarrage (original dans " & bak & ")."
    pose = True
Else
    Note "Correctif d'arret : NVCORE.VXD non reconnu (" & etat & "), pas modifie."
End If

nvu = sys & "\NVUDISP.EXE"
If FSO.FileExists(nvu) Then
    If FSO.GetFile(nvu).Size = FSO.GetFile(ici & "\NVUDISP.EXE").Size Then
        Note "Desinstalleur : deja celui de la 77.72."
    Else
        If Not FSO.FileExists(bak & "\NVUDISP.EXE") Then FSO.CopyFile nvu, bak & "\NVUDISP.EXE"
        FSO.CopyFile ici & "\NVUDISP.EXE", nvu, True
        Note "Desinstalleur : remplace par celui de la 77.72."
    End If
End If
Fin ""

' --- /installe : outil copie dans WINDOWS\NVFIX et lance a chaque demarrage
Sub Installer()
    If Not FSO.FolderExists(dest) Then FSO.CreateFolder dest
    For Each f In Array("NVFIX.VBS", "N8185.VXD", "N8198.VXD", "N8216.VXD", "N8269.VXD", "NVUDISP.EXE")
        FSO.CopyFile ici & "\" & f, dest & "\" & f, True
    Next
    cle = "HKLM\Software\Microsoft\Windows\CurrentVersion\Run\NVFIX"
    Set sh = CreateObject("WScript.Shell")
    If mode = "/surveille" Then
        sh.RegWrite cle, win & "\WSCRIPT.EXE " & FSO.GetFolder(dest).ShortPath & "\NVFIX.VBS /demarrage"
        Note "Outil installe dans " & dest & " (verification a chaque demarrage)."
    Else
        On Error Resume Next
        sh.RegDelete cle
        On Error GoTo 0
        Note "Outil installe dans " & dest & " (sans verification au demarrage)."
    End If
    ici = dest
End Sub

' --- Ajoute "cible=source" dans la section [rename] de WININIT.INI
Sub Renommer(cible, source)
    ini = win & "\WININIT.INI"
    ligne = cible & "=" & source
    texte = Lire(ini)
    If InStr(1, texte, ligne, 1) > 0 Then Exit Sub
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
End Sub

' --- Contenu d'un fichier texte ("" s'il n'existe pas ou s'il est vide)
Function Lire(chemin)
    Lire = ""
    If Not FSO.FileExists(chemin) Then Exit Function
    Set t = FSO.OpenTextFile(chemin, 1)
    If Not t.AtEndOfStream Then Lire = t.ReadAll
    t.Close
End Function

' --- n octets a la position pos, en hexadecimal (lecture texte ANSI)
Function Octets(chemin, pos, n)
    Set t = FSO.OpenTextFile(chemin, 1, False, 0)
    t.Skip pos
    s = t.Read(n)
    t.Close
    h = ""
    For i = 1 To Len(s)
        h = h & Right("0" & Hex(Asc(Mid(s, i, 1))), 2)
    Next
    Octets = h
End Function

Sub Note(texte)
    msg = msg & texte & vbCrLf
    Set j = FSO.OpenTextFile("C:\W98FR\JOURNAL.TXT", 8, True)
    j.WriteLine "NVFIX : " & texte
    j.Close
End Sub

Sub Fin(texte)
    If texte <> "" Then Note texte
    ' empreinte memorisee : le prochain demarrage ne refait rien si rien ne change
    If FSO.FolderExists(dest) Then
        Set t = FSO.CreateTextFile(dest & "\DERNIER.TXT", True)
        t.Write empreinte
        t.Close
    End If
    If pose Then msg = msg & vbCrLf & "Redemarrez Windows pour terminer."
    If mode = "/installe" Or mode = "/surveille" Then
        WScript.Echo msg
    ElseIf mode <> "/demarrage" Or pose Then
        MsgBox msg, 64, "Correctif NVIDIA"
    End If
    WScript.Quit
End Sub
