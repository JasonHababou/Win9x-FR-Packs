import sys
from pathlib import Path
R = Path(sys.argv[1])
txt = r"""Couche 3.66 filtree FR - PREPARATION (pas encore dans Win98FR_v2)

Contenu
  sp366fr\SP366FR.INF + 159 fichiers (45 Mo) : a copier tel quel dans le pack
  RAPPORT_366FR.TXT : decision fichier par fichier + effet sur la Sauvegarde 4
  Reconstruire : python -I _construction_outils\build_366fr.py <win98se> _construction_366

Principe : on part du SPUPDATE.INF de la 3.66 et on ne garde que ce qui est plus
recent que le pack SANS perte de francais. Les 20 fichiers en conflit sont pris
dans WIN9X\Mise a jour\FR pour la 3.66 (5 reconstruits = copie forcee, drapeau 36).
Exclus : DOS/aide/INF anglais, IO.SYS RLoew, VMM32.VXD generique, outils EN, theme,
date US, effacement de Setup\Updates, MSIEXEC EN, NOVOLTRK, convmem/file64,
SMARTVSD deplace, VCOMP.DLL (fonctions absentes de 98).

Integration prevue (apres validation de la v2) : fin de l'etape 03_SYST, avant le
redemarrage, une ligne dans INSTALL.BAT :
  start /w RUNDLL32.EXE ADVPACK.DLL,LaunchINFSection .\SP366FR.INF,DefaultInstall
Les OCX VB6 sont inscrits au redemarrage suivant (RunOnceEx de la 3.66).

A surveiller au premier test : KERNEL32 FR 2226 (RLoew), MSVCRT.DLL 7.0, IFSMGR.VXD
2227, VxD CD/disque de Windows Me (CDFS, DISKVSD...), GDIPLUS, Jet 4.0 SP8.
"""
(R / "_construction_366/LISEZMOI.TXT").write_bytes(txt.replace("\n", "\r\n").encode("cp1252"))
f = R / "Win98FR_v2/ETUDE_BASE_366.md"
t = f.read_text(encoding="utf-8")
a = "## 5. Les 42 options 3.66, langue et équivalent FR"
assert t.count(a) == 1
t = t.replace(a, """**Préparée (2026-10-14)** : `win98se\_construction_366\sp366fr\SP366FR.INF`, généré par
`_construction_outils\build_366fr.py` (159 fichiers, 45 Mo, dont 20 FR). Contrôle sur la
Sauvegarde 4 : aucune rétrogradation, `KERNEL32` 2225 → 2226 FR. En plus du §4 : `SMARTVSD`
laissé où 98 SE le met, `VCOMP.DLL` exclu (imports absents de 98), noms de pays et colonne
« Attributs » traduits. Pas encore dans le pack : à intégrer en fin de `03_SYST` après
validation de la v2. Détail : `_construction_366\RAPPORT_366FR.TXT`.

""" + a, 1)
f.write_text(t, encoding="utf-8")
print("ok")
