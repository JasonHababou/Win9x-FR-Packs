' ============================================================
' Detection du fabricant de chipset (carte-mere) par lecture du
' registre, sans dependance WMI : export regedit de HKLM\Enum\PCI
' puis recherche du PONT HOTE (peripherique PCI bus 0, device 0,
' fonction 0 = BUS_00&DEV_00&FUNC_00), qui est toujours le
' chipset de la carte-mere. On evite ainsi de detecter "Intel"
' sur une carte VIA/SiS equipee d'une carte reseau Intel.
'   Intel : VEN_8086   VIA : VEN_1106   SiS : VEN_1039
' Repli : ancienne methode (premier fabricant trouve).
' Ecrit le resultat dans C:\WMEFR\CHIPSET.BAT (set CHIPSET=...).
' ============================================================
Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

tmpReg = "C:\WMEFR\PCILIST.REG"

WshShell.Run "regedit /e " & tmpReg & " HKEY_LOCAL_MACHINE\Enum\PCI", 0, True

vendor = "INCONNU"
If FSO.FileExists(tmpReg) Then
    Set f = FSO.OpenTextFile(tmpReg, 1)
    content = UCase(f.ReadAll)
    f.Close
    FSO.DeleteFile tmpReg

    pos = InStr(1, content, "\BUS_00&DEV_00&FUNC_00]", 0)
    If pos > 0 Then
        start = InStrRev(content, "\PCI\VEN_", pos, 0)
        If start > 0 Then vendor = NomFabricant(Mid(content, start + 9, 4))
    End If

    If vendor = "INCONNU" Then
        If InStr(1, content, "VEN_1106", 0) > 0 Then
            vendor = "VIA"
        ElseIf InStr(1, content, "VEN_1039", 0) > 0 Then
            vendor = "SIS"
        ElseIf InStr(1, content, "VEN_8086", 0) > 0 Then
            vendor = "INTEL"
        End If
    End If
End If

Set outBat = FSO.CreateTextFile("C:\WMEFR\CHIPSET.BAT", True)
outBat.WriteLine "set CHIPSET=" & vendor
outBat.Close

Function NomFabricant(code)
    Select Case code
        Case "8086": NomFabricant = "INTEL"
        Case "1106": NomFabricant = "VIA"
        Case "1039": NomFabricant = "SIS"
        Case Else:   NomFabricant = "INCONNU"
    End Select
End Function
