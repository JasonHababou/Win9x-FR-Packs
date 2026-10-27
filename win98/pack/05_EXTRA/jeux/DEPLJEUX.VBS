' DEPLJEUX.VBS - Pack Win98FR
' Regroupe les jeux dans Menu Demarrer\Programmes\Jeux : y deplace les
' raccourcis de Programmes\Accessoires\Jeux (Demineur, Solitaire,
' FreeCell, Dame de Pique) et de Microsoft Plus! 98\Jeux (Spider),
' puis supprime ces dossiers vides. Sans accent ici : les noms sont
' obtenus par SpecialFolders.
Set sh = CreateObject("WScript.Shell")
Set fs = CreateObject("Scripting.FileSystemObject")
p = sh.SpecialFolders("Programs")
dst = p & "\Jeux"
If Not fs.FolderExists(dst) Then fs.CreateFolder dst
For Each src In Array(p & "\Accessoires\Jeux", p & "\Microsoft Plus! 98\Jeux")
  If fs.FolderExists(src) Then
    For Each f In fs.GetFolder(src).Files
      t = dst & "\" & f.Name
      If fs.FileExists(t) Then fs.DeleteFile t, True
      f.Move t
    Next
    If fs.GetFolder(src).Files.Count = 0 And fs.GetFolder(src).SubFolders.Count = 0 Then fs.DeleteFolder src, True
  End If
Next
