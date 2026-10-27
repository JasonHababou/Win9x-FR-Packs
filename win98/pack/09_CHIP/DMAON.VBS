' ============================================================
' DMAON.VBS - Pack Win98FR : active le DMA des peripheriques IDE
' (disques durs et lecteurs CD/DVD), comme la case "DMA" du
' Gestionnaire de peripheriques (onglet Parametres).
' Windows 98 range ce reglage dans la cle du canal IDE :
'   HKLM\System\CurrentControlSet\Services\Class\hdc\00xx
'   "IDEDMADrive0" (maitre) et "IDEDMADrive1" (esclave) = 01
' On le pose sur tous les canaux IDE primaire / secondaire (les cles
' inutilisees sont sans effet). Pris en compte au redemarrage ; si le
' peripherique ne gere pas le DMA, Windows decoche la case tout seul.
' Test Dell GX240 (carte CF + ICH2) : copie 3x plus rapide.
' ============================================================
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
cle = "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Class\hdc"
export = "C:\W98FR\HDC.REG"
sortie = "C:\W98FR\DMAON.REG"

sh.Run "regedit /e " & export & " """ & cle & """", 0, True
If Not fso.FileExists(export) Then WScript.Quit

Set f = fso.OpenTextFile(export, 1)
texte = f.ReadAll
f.Close
fso.DeleteFile export

reg = "REGEDIT4" & vbCrLf & vbCrLf
n = 0
For Each bloc In Split(texte, vbCrLf & "[")
    p = InStr(bloc, "]")
    If p > 0 Then
        nom = Left(bloc, p - 1)
        If Left(nom, 1) = "[" Then nom = Mid(nom, 2)
        d = LCase(Valeur(bloc, """DriverDesc""="))
        If InStr(d, "ide") > 0 And (InStr(d, "prima") > 0 Or InStr(d, "seconda") > 0) Then
            reg = reg & "[" & nom & "]" & vbCrLf & _
                  """IDEDMADrive0""=hex:01" & vbCrLf & _
                  """IDEDMADrive1""=hex:01" & vbCrLf & vbCrLf
            n = n + 1
        End If
    End If
Next

Set j = fso.OpenTextFile("C:\W98FR\JOURNAL.TXT", 8, True)
If n > 0 Then
    Set f = fso.CreateTextFile(sortie, True)
    f.Write reg
    f.Close
    sh.Run "regedit /s " & sortie, 0, True
    j.WriteLine "DMA : active sur " & n & " canal(aux) IDE (voir " & sortie & ")"
Else
    j.WriteLine "DMA : aucun canal IDE primaire/secondaire trouve, rien change"
End If
j.Close

' Valeur texte d'une ligne "nom"="valeur" dans un bloc d'export REGEDIT4
Function Valeur(bloc, debut)
    Valeur = ""
    q = InStr(1, bloc, debut, 1)
    If q = 0 Then Exit Function
    q = q + Len(debut)
    If Mid(bloc, q, 1) = """" Then q = q + 1
    r = InStr(q, bloc, """")
    If r > q Then Valeur = Mid(bloc, q, r - q)
End Function
