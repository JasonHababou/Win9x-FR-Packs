' Configurateur NTFS (pack Win98FR) : desactive la Corbeille sur les lecteurs
' NTFS choisis (la Corbeille de Windows 98 ne sait pas gerer le NTFS du pilote
' Paragon). Meme effet que le PNTFS.VBS de RF MasterX (bit "supprimer
' directement" de chaque lecteur dans BitBucket\PurgeInfo), mais SANS WMI :
' lecture par WScript.Shell.RegRead, ecriture par un fichier .REG importe avec
' REGEDIT /S. Prise en compte au prochain demarrage de Windows.
Option Explicit

Const CLE = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\explorer\BitBucket"
Const TITRE = "Configurateur NTFS"

Dim oShell, oFso, octets(71), i, v, saisie, lettres, n, ok, fic, f, ligne

Set oShell = CreateObject("WScript.Shell")
Set oFso = CreateObject("Scripting.FileSystemObject")

' Valeur actuelle de PurgeInfo (72 octets) ou valeur par defaut de Windows 98
On Error Resume Next
v = oShell.RegRead(CLE & "\PurgeInfo")
If Err.Number <> 0 Then v = Empty
On Error GoTo 0
If IsArray(v) Then
   If UBound(v) <> 71 Then v = Empty
End If
If IsArray(v) Then
   For i = 0 To 71 : octets(i) = CInt(v(i)) : Next
Else
   v = Array(&H48, 0, 0, 0, 1, 0, 0, 0)
   For i = 0 To 7 : octets(i) = v(i) : Next
   For i = 8 To 63 Step 2 : octets(i) = &H0A : octets(i + 1) = 0 : Next   ' 10 % par lecteur
   For i = 64 To 67 : octets(i) = 0 : Next     ' bits "supprimer directement" (A a Z)
   octets(68) = &H68 : octets(69) = &H4E : octets(70) = &HF5 : octets(71) = &HBF
End If

saisie = InputBox("Désactiver la Corbeille pour le(s) lecteur(s) NTFS choisi(s)." & vbCrLf & vbCrLf & _
   "Entrez la ou les lettres de lecteur :" & vbCrLf & vbCrLf & _
   "un seul lecteur : E" & vbCrLf & "plusieurs lecteurs : E,F,G", TITRE)
saisie = UCase(Replace(Replace(saisie, " ", ""), ";", ","))
If Len(saisie) = 0 Then WScript.Quit

lettres = Split(saisie, ",")
For Each v In lettres
   If Len(v) <> 1 Then ok = False Else ok = (Asc(v) >= 65 And Asc(v) <= 90)
   If Not ok Then
      MsgBox "Lettre de lecteur invalide : " & v, vbCritical, TITRE
      WScript.Quit
   End If
Next

octets(4) = 0                                   ' reglage par lecteur (pas global)
For Each v In lettres
   n = Asc(v) - 65                              ' A = 0 ... Z = 25
   octets(64 + n \ 8) = octets(64 + n \ 8) Or (2 ^ (n Mod 8))
Next

' Ecriture par un fichier .REG (REGEDIT4) importe en silence
fic = oShell.ExpandEnvironmentStrings("%TEMP%") & "\NTFSCFG.REG"
Set f = oFso.CreateTextFile(fic, True)
f.WriteLine "REGEDIT4"
f.WriteLine ""
f.WriteLine "[" & CLE & "]"
ligne = """PurgeInfo""=hex:"
For i = 0 To 71
   ligne = ligne & LCase(Right("0" & Hex(octets(i)), 2))
   If i < 71 Then ligne = ligne & ","
Next
f.WriteLine ligne
f.Close
oShell.Run "REGEDIT /S """ & fic & """", 0, True
oFso.DeleteFile fic

MsgBox "Corbeille désactivée pour : " & saisie & vbCrLf & vbCrLf & _
   "Le changement sera pris en compte au prochain démarrage de Windows.", vbInformation, TITRE
