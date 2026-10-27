# Pack 2, installeur a cases : Winamp = sous-groupe a cocher (oui / non), qui
# contient 3 versions dont une seule peut etre cochee. Les macros RadioButton de
# Sections.nsh ne suffisaient pas : cocher "Multimedia" cochait plusieurs Winamp
# (test GX240 2026-10-16). Logique maison dans .onSelChange.
import sys
from pathlib import Path

p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8")


def rep(old, new):
    global t
    assert t.count(old) == 1, old
    t = t.replace(old, new)


rep("  Var WARADIO    ; section Winamp cochee (boutons radio)\n",
    "  Var WARADIO    ; version de Winamp retenue (une seule cochee)\n"
    "  Var WANB       ; nombre de versions de Winamp cochees avant le clic\n")

rep('Section /o "Winamp : aucun" SEC_WAN\n'
    'SectionEnd\n'
    'Section /o "Winamp 5.2 Standard (anglais)" SEC_WAS\n'
    'SectionEnd\n'
    'Section "Winamp 5.2 Full (anglais)" SEC_WAF\n'
    'SectionEnd\n'
    'Section /o "Winamp 2.91 (francais)" SEC_WA2\n'
    'SectionEnd\n',
    'SectionGroup /e "Winamp (une seule version)" GRP_WA\n'
    'Section /o "Winamp 5.2 Standard (anglais)" SEC_WAS\n'
    'SectionEnd\n'
    'Section "Winamp 5.2 Full (anglais)" SEC_WAF\n'
    'SectionEnd\n'
    'Section /o "Winamp 2.91 (francais)" SEC_WA2\n'
    'SectionEnd\n'
    'SectionGroupEnd\n')

rep('  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_WAN} "Ne pas installer Winamp."\n',
    '  !insertmacro MUI_DESCRIPTION_TEXT ${GRP_WA} "Decochez pour ne pas installer Winamp. Ouvrez le groupe pour choisir la version : une seule peut etre cochee."\n')

rep("  StrCpy $WARADIO ${SEC_WAF}\n",
    "  StrCpy $WARADIO ${SEC_WAF}\n"
    "  StrCpy $WANB 1\n")

rep("; Winamp : une seule version (cocher l'une decoche les autres)\n"
    "Function .onSelChange\n"
    "  !insertmacro StartRadioButtons $WARADIO\n"
    "    !insertmacro RadioButton ${SEC_WAN}\n"
    "    !insertmacro RadioButton ${SEC_WAS}\n"
    "    !insertmacro RadioButton ${SEC_WAF}\n"
    "    !insertmacro RadioButton ${SEC_WA2}\n"
    "  !insertmacro EndRadioButtons\n"
    "FunctionEnd\n",
    "; Winamp : une seule version. Une version de plus cochee d'un clic = elle\n"
    "; remplace l'ancienne ; groupe entier coche (groupe Winamp ou Multimedia) =\n"
    "; on garde la derniere version retenue (par defaut 5.2 Full).\n"
    "!macro WA_COMPTE SEC\n"
    "  ${If} ${SectionIsSelected} ${SEC}\n"
    "    IntOp $R0 $R0 + 1\n"
    "    ${If} ${SEC} != $WARADIO\n"
    "      StrCpy $R1 ${SEC}\n"
    "    ${EndIf}\n"
    "  ${EndIf}\n"
    "!macroend\n"
    "\n"
    "Function .onSelChange\n"
    "  Push $R0\n"
    "  Push $R1\n"
    "  StrCpy $R0 0\n"
    "  StrCpy $R1 -1\n"
    "  !insertmacro WA_COMPTE ${SEC_WAS}\n"
    "  !insertmacro WA_COMPTE ${SEC_WAF}\n"
    "  !insertmacro WA_COMPTE ${SEC_WA2}\n"
    "  ${If} $R0 > 1\n"
    "    ${If} $WANB == 1\n"
    "    ${AndIf} $R0 == 2\n"
    "      StrCpy $WARADIO $R1\n"
    "    ${EndIf}\n"
    "    !insertmacro UnselectSection ${SEC_WAS}\n"
    "    !insertmacro UnselectSection ${SEC_WAF}\n"
    "    !insertmacro UnselectSection ${SEC_WA2}\n"
    "    !insertmacro SelectSection $WARADIO\n"
    "    StrCpy $R0 1\n"
    "  ${ElseIf} $R0 == 1\n"
    "  ${AndIf} $R1 != -1\n"
    "    StrCpy $WARADIO $R1\n"
    "  ${EndIf}\n"
    "  StrCpy $WANB $R0\n"
    "  Pop $R1\n"
    "  Pop $R0\n"
    "FunctionEnd\n")

assert "SEC_WAN" not in t
p.write_text(t, encoding="utf-8")
print("ok")
