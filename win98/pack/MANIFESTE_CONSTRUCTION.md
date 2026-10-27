# Manifeste de construction — Pack Windows 98 SE FR

## ⭐ Architecture v2 (2026-10-14) — À LIRE EN PREMIER

Ce dossier `Win98FR_v2` remplace `Win98FR` (conservé pour comparaison tant que la
v2 n'est pas validée sur la vraie machine). Construit par copie avec
`scratchpad\make_v2.py` ; sources texte dans scratchpad `src_v2`.

- **`INSTALL.BAT` à la racine** (plus de dossier `w\`). Lancement : `AUTORUN.EXE`
  (CD : `AUTORUN.INF`) ou double-clic sur `INSTALL.BAT`, depuis un CD **ou** un
  dossier du disque dur.
- **Un dossier par étape** (noms 8.3) :

| Dossier | Étape | Ancien emplacement |
|---|---|---|
| `01_BASE` | [1/11] IE6 SP1, WMP9, correctifs, MDAC (+ `winsub_b.reg` étape 3) | `maj2004` |
| `02_SP30` | [2/11] SP3.0 + composants SP3.0 des étapes 5 et 6 | `sp30` |
| `03_SYST` | [3/11] Shell32, GDI, 3.63, certificats ; `rloew` = PATCHMEM [11/11] | `systeme` + `materiel\rloew` |
| `04_IEOE` | [4/11] correctifs IE / OE | `ie_oe` |
| `05_EXTRA` | [5/11] KernelEx, NTFS, Plus! 98, Pinball, réglages, ASPI, WSH 5.7, MS Agent | `extras\*` |
| `06_OPTS` | [6/11] MMC, RegClean, SharedDLLs, fuseaux, Zip, TTF | `extras\divers` |
| `07_DX` | [7/11] DirectX au choix | `materiel\directx` |
| `08_NET` | [8/11] .NET 1.1 / 2.0 | `extras\dotnet` |
| `09_CHIP` | [9/11] chipset | `materiel\pilotes_phil` |
| `10_APPLI` | [10/11] VC++, QRes, 7-Zip, DAEMON, RetroZilla, Tarot, Fraps | `extras\applis` |

- **Retirés** : `materiel\ess_allegro` (jamais installé par le pack : l'utilisateur
  installe le pilote son lui-même), `extras\aspi\Docs` et `include` (fichiers de
  développement). L'étape [11/11] n'est plus que PATCHMEM (correctif système,
  toujours lancé en dernier).
- **Reprise** : `INITGO` mémorise le chemin de `02_SP30` (`W98SUB`, jamais « D:\ »
  à la racine d'un CD) ; `GO.BAT` attend `%W98SUB%\SPUPDATE.INF` (CD inséré ou
  dossier présent) puis `cd "%W98SUB%"`, `cd ..`, `call INSTALL.BAT`.
- Chaque bloc fait `cd NN_XXX\composant` depuis la racine puis revient à la racine
  (`cd ..\..`) ; `w2kcolor.bat` lit `..\..\03_SYST\SHELL32.DLL`.
- **Autorun** : `_construction_autorun\AUTORUN.nsi` (NSIS 2.46, nsDialogs),
  `makensis /DPACK=1` → `Win98FR_v2\AUTORUN.EXE` (Installer / Lisez-moi / Quitter),
  `/DPACK=2` → `Win98FR_Plus\AUTORUN.EXE` (cases à cocher / questions O/N / Lisez-moi).
- Vérificateur `check_bat.py` : mode v2 automatique (présence de `INSTALL.BAT` à la
  racine) ; il reste 3 signalements attendus (dossier facultatif `05_EXTRA\perso`,
  `REGSVR32` dans `C:\WINDOWS\SYSTEM`).
- **2026-10-14, WinUpdates_95-XP32.iso analysée puis supprimée** : correctifs 98 surtout
  anglais (US8/ENU) et déjà couverts en FR par SP3.0. Repris : **Visual C++ 2005**
  8.0.50727.42 (`10_APPLI\vc2005\VCREDIST.EXE`, msvcr80/msvcp80/mfc80u : imports
  98 vérifiés, sans KernelEx ; `/q:a /c:"msiexec /i vcredist.msi /qb"`), Java 1.5.0_18,
  Flash 9.0.47 (greffon Mozilla) et Shockwave 10.2 rangés dans `WIN9X\Logiciel\Plugins web 98`
  (non intégrés), guide d'installation 9x + liste des versions dans `Sources\Documentation`
  (options SETUP utiles pour une future image : /IS /IE /IW /NF /NH, CAB copiés dans
  `C:\WINDOWS\OPTIONS\CABS`). VC++ 2008 de l'image = identique à celui du pack.
- **2026-10-14, `bkpWin98` ne contient plus que les sauvegardes** : `cd\dell` →
  `WIN9X\Driver\Dell GX240`, Plus! 98 décompressé (thèmes FF7/FF8, Pinball/Spider FR) →
  `WIN9X\Logiciel\Plus98 (decompresse, themes FF7-FF8)`, jeux et émulateurs de `down` et
  `Jeux` → `WIN9X\Jeux`, doublons (Logiciel, Win98, addons, dx, Security, installeurs) →
  `_a_supprimer\bkpWin98_cd`. VC++ 2005 du pack = emballage **français** (`vcredist.msi`
  identique à la version anglaise).
- **Modifier la v2 directement dans scratchpad `src_v2`** (ne plus relancer `make_v2.py`,
  qui régénère `src_v2` depuis l'ancien `src`).
- Dans le reste de ce document, les anciens chemins (`w\install.bat`, `extras\…`,
  `materiel\…`, `sp30\…`) se lisent avec le tableau ci-dessus.


Ce document indique exactement quel fichier source (de vos archives déjà collectées)
placer dans quel dossier de cette structure, pour que `w\install.bat` fonctionne.
Pour chaque élément, la **provenance exacte** (nom de l'archive/ISO d'origine chez
vous) est précisée, pour que vous puissiez retrouver le bon fichier sans ambiguïté.

Structure actuelle (révision 2026-10-13) :
```
Win98FR\
├── w\install.bat          ← script maître, COMMAND.COM pur, 10 étapes, 4 redémarrages
├── MANIFESTE_CONSTRUCTION.md  ← ce fichier
├── CONTEXTE_IA.md         ← à lire en premier dans toute nouvelle session
├── maj2004\               ← [1/10] ie6sp1\, wmp9\, directx9b\, mdac28\,
│                             updates\ (5 correctifs seulement), winsub_b.reg
├── sp30\                  ← SP3.0 B4 FR COMPLET (racine de SP30B4FR.EXE) :
│                             [2/10] spupdate.inf, [5/10] NUSB, meview, Me-Progs,
│                             euro, TweakUI, tweaks, [6/10] WinTop, DosHere, logos, WSH
├── systeme\               ← [3/10] Shell98 FR, Q918547 FR
│   └── copie363\          ← 8 fichiers 3.63 + copie.bat
├── ie_oe\                 ← [4/10] KB823353, KB887797, Q931768 (via IEUPDATE.EXE)
├── extras\                ← [5/10] et [6/10] : uniquement ce qui ne vient PAS de SP3.0
│   ├── kernelex\  ntfs\  plus98\  taskbarshuffle\
│   ├── w2kcolor\ (+ base\, w2kcolor.bat, W2KSHELL.INF, W2K_*.TXT) ← exception
│   ├── tweaks\ (TWEAKS366.INF)  mspaintfilter\  aspi\  msagent\
│   ├── divers\            ← MMC, RegClean, SharedDLLs, fuseaux FR, Zip FR, TTF
│   ├── dotnet\net11\, dotnet\net20\   ← [8/10]
│   └── perso\perso.bat    ← facultatif, à créer vous-même
└── materiel\
    ├── directx\           ← [7/10] dx81, dx82, dx90b, dx90c, dx90Cunofficial
    ├── pilotes_phil\      ← [9/10] detect_chipset.vbs + intel\ via\ sis\
    ├── ess_allegro\       ← manuel
    └── rloew\             ← [10/10] PATCHMEM, FIX95CPU (après le dernier redémarrage)
```
Fichiers retirés du pack : déplacés (pas supprimés) dans
`win98se\_retires_Win98FR\`.

---

## ⭐ Révision 2026-10-13 : audit complet (prime sur les sections plus bas)

Audit fichier par fichier de `Win98FR\` et comparaison avec SP30B4FR,
U98SESP3.63/3.66 et WUPG98 (versions et **langue** lues dans les binaires).
Quand une section plus bas contredit celle-ci, **c'est celle-ci qui fait foi**.

### Nouvelle séquence d'`install.bat` (10 étapes, 4 redémarrages)

| Étape | Contenu | Redémarrage après |
|---|---|---|
| 1/10 phase 1 | IE6 SP1 FR, WMP9 FR | oui |
| 1/10 phase 2 | q240308, q313829, q330994, q828750, KB819639, MDAC 2.8 SP1 FR | oui |
| 2/10 | **SP3.0 B4 FR `spupdate.inf`** (mise à jour principale, 246 fichiers) | oui |

> **27/10/2026** : la ligne `Keyb.com` (correctif 319571) est retirée de `spupdate.inf`. Elle remplaçait le `KEYB.COM` **français** de 98 SE (1999, 20 135 octets) par un `KEYB.COM` **anglais** (2005, 19 943 octets). Effet sur le GX240 : dans Dungeon Keeper (DOS), la flèche haut était lue comme Maj + 8 du pavé numérique (ou 8 seul, Verr Num éteint), et le menu de choix des touches se figeait. Windows Me, qui garde le `KEYB.COM` français, n'a pas ce problème.
>
> **27/10/2026 (suite)** : test sur le GX240, le `KEYB.COM` français de 98 SE fait **aussi** figer Dungeon Keeper, et le problème disparaît avec celui de Windows ME. Clavier du GX240 = USB (émulation « USB legacy » du BIOS). `SYSTEM.INI` `type=4` testé : inutile.
>
> **27/10/2026, correction (ISO test16 dans QEMU)** : le `KEYB.COM` de ME (MS-DOS 8) affiche « Version de MS-DOS incorrecte » sous le DOS 7.1 de 98 et **ne se charge pas**. Il a donc été retiré du pack (copie dans `_a_supprimer\keyb_me_2026-10-27`). Le test du GX240 montre en fait que Dungeon Keeper marche **quand aucun KEYB n'est chargé** au démarrage de Windows. Le pack garde le `KEYB.COM` français d'origine de 98 SE (ligne du SP3.0 toujours en commentaire). Option à valider par l'utilisateur : ne charger KEYB qu'en mode MS-DOS (voir `Test GX240 - clavier DOS`).
>
> **28/10/2026, validé et intégré** : testé sur le GX240 (`KEYBDOS.BAT`), Dungeon Keeper marche, plus de blocage. Nouvelle étape du pack, à la fin (`:FINOK`, dossier `05_EXTRA\clavier`) : la ligne `keyb` passe d'`AUTOEXEC.BAT` (copie dans `C:\W98FR\AUTOEXEC.KBK`) à `DOSSTART.BAT` (mode MS-DOS) et à `C:\WINDOWS\CLAVDOS.BAT`, que le raccourci « Commandes MS-DOS » lance (`CMDMSDOS.PIF` : `COMMAND.COM /K C:\WINDOWS\CLAVDOS.BAT`, paramètres à +0x28 de la section WINDOWS 386 3.0). Disposition choisie (FR ou BE) conservée. Vérifié dans QEMU : plus de KEYB au démarrage, AZERTY dans « Commandes MS-DOS » et en mode MS-DOS.

| 3/10 | winsub_b.reg, Shell98 FR 2007, Q918547 FR, copie363 | — |
| 4/10 | KB823353, KB887797, Q931768 (IEUPDATE.EXE) | — (Essentiel : fin ici) |
| 5/10 | Extras : depuis `sp30\` NUSB, meview, Me-Progs, euro, TweakUI ; depuis `extras\` KernelEx, NTFS, Plus! 98, Taskbar Shuffle, thème W2K, tweaks (3.66 puis SP3.0), filtres Paint, ASPI, perso, MS Agent O/N | — |
| 6/10 | Optionnels O/N : WinTop, Invite de commande ici, logos animés, WSH 5.6.8834 (SP3.0) ; MMC, RegClean, SharedDLLs, fuseaux FR, Zip FR, TTF | — |
| 7/10 | DirectX au choix : rien, 8.1, 8.2, 9.0b, 9.0c (aussi en Essentiel) | — |
| 8/10 | .NET 1.1 FR / .NET 2.0 dotnet9x (O/N) | — |
| 9/10 | Chipset (détection du pont hôte PCI + menu) | oui |
| 10/10 | Rappel ESS Allegro, puis PATCHMEM + FIX95CPU (O/N) | fin |

**Reprise automatique** (voir aussi « Marqueurs » ci-dessous) : au premier lancement, `install.bat` mémorise la
lettre et le dossier du pack (astuce DOS `PROMPT $n:` / `$p`), écrit
`C:\W98FR\GO.BAT` (retour dans `w\` + `call install.bat`) et
`C:\W98FR\RUNONCE.REG`, importé avant chaque redémarrage
(`HKLM\...\RunOnce`, valeur `command.com /c C:\W98FR\GO.BAT`). Le script
se relance aussi lui-même avec un environnement de 4 Ko
(`%COMSPEC% /e:4096`) pour éviter « Espace d'environnement insuffisant ».

**Marqueurs** (mise à jour après le 1er test réel) : `C:\W98FR\ETxx.TXT`
posé au début de chaque étape, RunOnce réarmé à chaque reprise, menu
« R = reprendre à une étape ». `SHELL98.INF` et `Q918547.INF` : ajout de
`SmartReboot=N` (leur absence a provoqué une demande de redémarrage
d'ADVPACK bloquée par la fenêtre DOS à l'étape 3).

**Dépendances vérifiées (après le 1er test réel)** : tous les binaires PE du
pack ont été contrôlés (DLL importées présentes + fonctions exportées) contre
Windows 98 SE FR + SP3.0 + Couche 1. Corrigé : `MSVCP50.DLL` (5.00.7051,
SP3.0) ajoutée à `extras\divers\` et à `MMC.INF` (`[MMCSF]`, drapeau 32) —
absente de Windows 98, SP3.0 ne la copie que si elle existe déjà (1056) →
« Erreur d'inscription MMCNDMGR.DLL » au test ; `SNMPAPI.DLL` 5.0.2195.6811
(3.63) ajoutée à `copie363` (exigée par le `SNMP.EXE` 3.63) ; destinations de
`copie.bat` corrigées comme dans SP3.0/3.66 (`HH.EXE`, `SNMP.EXE`,
`SNMPAPI.DLL` dans `WINDOWS`, `MSCONV97.DLL` dans
`Fichiers communs\Microsoft Shared\TextConv`, le reste dans `SYSTEM`).

**Fin du 1er test réel (2026-10-13)** :
- **FIX95CPU retiré** (`_retires_Win98FR\rloew\`) : d'après son README, c'est
  une image de disquette de démarrage pour **Windows 95** (erreurs IOS/NDIS des
  processeurs rapides) ; inutile sous 98 SE (SP3.0 fournit `NDIS.VXD` corrigé),
  et il réclamait une disquette au test.
- **PATCHMEM** lancé en `/I` (installation seule, sans question), puis
  `materiel\rloew\SYSINI.INF` retire `MaxPhysPage` ([386Enh], écrit par SP3.0)
  et `MaxFileCache` ([vcache], s'il existe) de SYSTEM.INI, comme le demande le
  manuel PATCHMEM après un Service Pack. (SP3.0 n'écrit pas `MaxFileCache` :
  normal de ne pas le trouver.)
- **Redémarrage automatique** en fin d'installation (15 s, N pour annuler).
- **`extras\tweaks\TWEAKS.INF`** : fusion de `TWEAKS366.INF` et de `tweaks.inf`
  SP3.0 en un seul INF FR (un seul appel). La désinstallation ne retire pas
  « Envoyer vers ». `TWEAKS366.INF` retiré vers `_retires_Win98FR\tweaks\`.

**DirectX au choix [7/10]** (2026-10-13, demande après le 2e test) :
DirectX 9.0b n'est **plus installé d'office** en phase 2 (il empêchait
d'installer DirectX 8.x, DirectX ne revenant jamais en arrière). Il est déplacé
de `maj2004\directx9b\` vers `materiel\directx\dx90b\` et devient un choix du
menu : 1 = rien (DirectX 6.1 d'origine), 2/3 = 8.1/8.2, 4 = 9.0b,
5 = 9.0c officiel, 6 = 9.0c communautaire. DirectX 8.0 retiré (8.1 le
remplace), dossier `dx80` déplacé vers `_retires_Win98FR\directx\`. Le menu DirectX est aussi proposé en
mode Essentiel.

**Q931768 (2e test réel)** : « syntaxe incorrecte dans la section
IExploreLDID ». Les 4 INF `Q931768*.INF` du paquet `IE6_918899 Fr` avaient
`;RequiredEngine=Setupapi` **commenté** (l'INF officiel q828750 l'a actif) :
ADVPACK utilisait alors le moteur 16 bits de Windows 98, incapable de lire ces
INF de type NT. Ligne réactivée dans les 4 (originaux dans
`_retires_Win98FR\ie_oe_inf_origine\`).

**Reprise (2e test réel)** : une reprise après redémarrage n'a pas eu lieu.
`GO.BAT` attend désormais jusqu'à 60 s que le dossier du pack soit accessible
(lecteur pas encore prêt quand RunOnce s'exécute), et `install.bat` tient un
journal `C:\W98FR\JOURNAL.TXT` (lancements, étapes, redémarrages, dossier du
pack) pour diagnostiquer.

**WSH 5.6.8834 (2e test réel)** : `scr56.inf` réclamait `cscript.exe` puis
`dispex.dll` « sur Inconnu ». Son `CopyFiles` appelait une section `Copy.Inf`
absente du fichier (seul défaut de ce type parmi tous les INF lancés, vérifié).
Appel retiré, et les 10 fichiers WSH de `SP2.CAB` (tailles identiques à
`SLAYOUT1.INF`) placés à plat dans `sp30\`.

**3e test réel** :
- Q931768 toujours en erreur IExploreLDID malgré `RequiredEngine` : le
  texte `IEFolderPrompt`, traduit par le reconditionneur (108 caractères ;
  Microsoft le laisse en anglais, 79 caractères, même dans q828750 FR),
  raccourci à 52 caractères dans les 4 INF. Hypothèse de limite de longueur
  du moteur, à confirmer.
- Reprise : clé `Run` permanente au lieu de RunOnce ré-armé (double reprise),
  verrou `ENCOURS.TXT`, `GO.BAT` inerte sans étape, bug « N au redémarrage →
  abandon » corrigé.
- `copie363` : `_CP.BAT` ne remplace un fichier que s'il existe déjà (plus de
  « Fichier introuvable », plus de `SNMP.EXE` posé sans SNMP installé).

**Q931768 : nouvel INF `ie_oe\IE6Q9317.INF` (4e test réel)** : l'erreur
IExploreLDID persistait. Constats : `ie_oe` est l'extraction exacte de
`WIN9X\Mise a jour\IE6_918899 Fr.exe`, un **reconditionnement
communautaire** (titre « …pour Windows 98/98 SE/NT4 SP6a/ME » ; Microsoft n'a
plus publié de correctif IE pour 98 après juillet 2006) dont la commande
`IEUPDATE.EXE /D Q918899` ne correspond même pas à ses INF Q931768 ; et les
sauvegardes saines n'ont jamais eu ce correctif (MSHTML 6.00.2800.1264 =
q828750). Les 16 DLL (FR pour celles qui ont une interface, 6.00.2800.1593 /
.1907) importent uniquement des fonctions présentes sous Windows 98 + SP3.0 +
IE6 (vérifié). `IE6Q9317.INF` les installe directement : sections
`[System.Files]` (drapeau 32), `[Actsetup.Reg]`, `[User.AddReg]`,
`[User.DelReg]`, `[Strings]` reprises de `Q931768_D.INF`, sans
CustomDestination ni RequiredEngine. `install.bat` [4/10] l'appelle à la place
d'`IEUPDATE.EXE`.

**Étape [10/11] Applications (`extras\applis\`)** :
- `vc2008\VC_R_9X.EXE` : Visual C++ 2008 pour 98/ME (retrosystemsrevival,
  copié de `WIN9X`). `MSVCR90.DLL` et `MFC90.DLL` importent
  `GetSystemWindowsDirectoryW` / `GetFileSizeEx` : **KernelEx indispensable**,
  d'où l'étape placée après le redémarrage qui suit le chipset. Contient
  `MFC90FRA.DLL`. Lancé en `/q:a /r:n`.
- `firefox\FirefoxPortableESR\` : Firefox Portable 31.8.0 ESR (version adaptée
  98/ME du même blog, `WIN9X\Logiciel\FirefoxPortable31.8ESR.7z`), **sans** le
  profil utilisé qu'elle contenait (`Data\` exclu). Ajouts dans
  `App\DefaultData\profile\` : module de langue officiel Mozilla
  `fr.xpi` 31.8.0 (ftp.mozilla.org) et `user.js` (locale fr, module activé,
  police Tahoma). Copié dans `C:\FIREFOX` par `xcopy` ; `FIREFOX.INF` met
  `C:\FIREFOX\APP\FIREFOX\XUL.DLL` en mode KernelEx `WINXP` (XP SP2 : KernelEx
  4.5.2 n'a pas de mode XP SP3, celui que demande la version portable — **à
  valider**) et crée le raccourci Bureau.
- `qres\` : QRes 1.0.9.5 autonome (`QRES.EXE` + `QRES32.DLL`, Berend
  Engelbrecht, BSD, SourceForge `qres-setup1090.zip` → `patches\qres1095.zip`),
  installé par `QRES.INF` avec un mode d'emploi FR `C:\WINDOWS\QRES.TXT`.
- **Logiciels de `WIN9X\Logiciel`** (2026-10-13), tous vérifiés sans
  KernelEx (imports présents dans Windows 98), renommés en 8.3 :
  `7zip\7Z920.EXE` (NSIS, `/S` ; langue choisie d'après Windows → français),
  `winrar\WRAR393F.EXE` (SFX, `/s` ; FR ; le lien publicitaire
  `Vodelic_mode_d_emploi_video.html` du paquet est supprimé après coup),
  `imgburn\IMGBURN.EXE` (NSIS, `/S` ; + `FRENCH.LNG` officiel, traduction faite
  pour la 2.5.7.0, copié dans `ImgBurn\Languages`), `retrozil\RZ23.EXE` (installeur Mozilla, `-ms` —
  validé aux tests QEMU ; anglais ; puis `RETROZIL.REG` : **navigateur par défaut**,
  avec les mêmes clés que RetroZilla quand on répond Yes, relevées dans le registre
  de la VM test12 le 2026-10-20, et `Check_Associations=no` pour IE), `daemon\DAEMON.MSI` (le .msi qu'extrait
  `daemon347.exe`, repris de « Sauvegarde Saine » ; `MSIEXEC /qb
  REBOOT=ReallySuppress` ; anglais, aucune traduction trouvée), `aida32\AIDA393.EXE` (Inno Setup 3.0.5, `/VERYSILENT /SP-` ;
  se met seul en français d'après l'utilisateur).
- **Jeux** : le « Unofficial Windows 98 SE Game Pack 1.2 » (`GAMEPACK.EXE`)
  est écarté. Son `GAMES.BAT` vise `%PF%\PROGRA~1` et
  `%WINDIR%\STARTM~1\PROGRAMS\ACCESS~1\GAMES` : ces chemins anglais n'existent
  pas sur un Windows français (`Menu Démarrer\Programmes\Accessoires\Jeux`),
  donc aucun raccourci n'est créé. Ses Pinball (XP 5.1) et Spider sont en anglais.
  À la place : **Spider Solitaire FR** = composant de Plus! 98 (avec son aide
  FR), activé dans `MSBATCH.INF` ; **Pinball 3D FR** 4.90.3000.1 (copie de
  `WIN9X\Logiciel\Plus98 (decompresse, themes FF7-FF8)\PINBALL`) par `extras\jeux\PINBALL.INF`
  → `Program Files\Plus!\Pinball` + raccourci `Accessoires\Jeux`, sans aide
  (pas de `PINBALL.CHM` FR).
- **Certificats racine** (`systeme\rootsupd\`, étape [3/11]) : SP3.0 installe ceux
  d'avril 2009 ; on applique ensuite ceux de **septembre 2020** de U98SESP3.66
  (`ROOTSUPD.INF` : AUTHROOTS/UPDROOTS/ROOTS/DELROOTS, puis `RVKROOTS.INF` :
  DISALLOWEDCERT, comme le SPUPDATE.INF de la 3.66), plus récents que le paquet
  BWC de mars 2020. `UPDROOTS.EXE` (2012) : imports présents dans 98. Utile au
  magasin Windows (signatures Authenticode, IE/OE, WinINet) ; sans effet sur
  Firefox/RetroZilla (magasin NSS propre) ni sur la limite TLS 1.0 d'IE6.
- **Jeux dans `C:\Jeux` (options [10/11])** — raccourcis dans `Accessoires\Jeux` :
  - `applis\jeux\` : **Hover! FRANÇAIS** (CD Windows 95 OSR2.5 FR `W95_OSR25FR.bin`,
    `FUNSTUFF\HOVER`, remplace l'anglais du Game Pack), SkiFree et Échecs (anglais,
    Game Pack 1.2, aucune version FR). xcopy + `JEUX.INF` (raccourcis).
    Jeux Internet de XP écartés : en ligne seulement, serveurs fermés en 2019.
  - `applis\tarot\` : **Jeu de Tarot** (Sybex 2000, FR, Visual Basic 6). L'installeur
    InstallShield 3 d'origine (`_INST32I`, `_SETUP.1`) est écarté : extrait avec
    `scratchpad\is3unz.py` (décodeur PKWARE DCL), il embarquait des DLL système
    de 1996-1999 toutes plus anciennes que Windows 98 + SP3.0 (dont `COMDLG32.DLL`
    4.0.951 de Windows 95). On ne garde que les 19 composants VB6 absents de 98
    (OCX + DLL de langue FR), copiés avec le drapeau 32 et enregistrés par
    `TAROT.INF` ; `VB6DockOCX.ocx` (nom long) copié/enregistré par install.bat.
    Original dans `_retires_Win98FR\tarotFr_installeur_origine\`.
  - `applis\puzzle\` : **Microsoft The Puzzle Collection** complète (1997,
    multilingue, DLL + aides FR), contenu de `msentpack_puzzle.iso` ;
    installeur Microsoft interactif (`SETUP.EXE`, langue d'après Windows),
    l'utilisateur choisit `C:\Jeux\Puzzle`.
  - L'ancien `applis\jeuxen\` (Hover! anglais) est dans `_retires_Win98FR\jeuxen_anglais\`.
- **Logiciels (lot 3, Win3x.org, sommes SHA vérifiées)** :
  `winamp\WINAMP29.EXE` + `WAMPFR.EXE` (Winamp 2.91 + patch FR, NSIS 1.x, `/S`
  **à valider**), `xnview\XNVIEW18.EXE` (XnView 1.80.3, Inno 4.2.6,
  `/VERYSILENT /SP-`, module `xnviewfr.dll` inclus), `foxit\FOXIT13.EXE` (Foxit
  Reader 1.3 sans installation, **anglais**, copié par `FOXIT.INF`),
  `klcodec\KLCP345F.EXE` (K-Lite 3.4.5 Full, Inno 5.1.13, sélection par défaut,
  `/VERYSILENT /SP- /NORESTART`, inclut Media Player Classic et ffdshow FR).
  **VLC 3.0.24 via KernelEx** (`applis\vlc\`, option expérimentale) : VideoLAN
  conseille KernelEx pour 98. `scratchpad\kexcover.py` compare les imports aux
  exports de Windows 98 + aux tables d'API de KernelEx 4.5.2019.24 : cœur de VLC
  entièrement couvert ; 15 modules sur 368 retirés (Direct3D 11, dav1d, Blu-ray,
  WASAPI/MMDevice, UPnP, RIST, archive, XML, caca, QSV, ARIB) → 31 fonctions
  manquantes, toutes fournies par KernelEx. Traductions : français seul (129 Mo).
  Copie directe (l'installeur NSIS exigerait XP), `VLC.INF` : mode KernelEx
  `WINXP3` pour `vlc.exe`, `libvlc.dll`, `libvlccore.dll`, `Lang=fr`, raccourcis
  Programmes\VideoLAN et Bureau. Repli si échec : VLC 0.8.6i (dernier officiel 98).
- **Outils de test** (`applis\bench\`, installations guidées, O/N séparés) :
  `FRAPS19D.EXE` (Fraps 1.9D, NSIS 1.x, dernière version citée pour 98),
  `3DM2001.EXE` (3DMark2001 SE, InstallShield 6), `3DM03.EXE` (3DMark03 3.60,
  InstallShield 2009 : moteur `setup.exe`/`ISSetup.dll`/`_Setup.dll` 15.0, imports
  tous présents dans 98, **à valider** ; exige DirectX 9). Pas d'installation
  silencieuse sans fichier réponse : lors du test, `Setup.exe -r` enregistrerait
  un `setup.iss` réutilisable avec `-s`.
- Marqueurs : `ET10.TXT` = Applications, `ET11.TXT` = matériel/PATCHMEM ;
  menu R : A = applications, 0 = matériel.

**Commentaires REM** : COMMAND.COM applique `<`, `>` et `|` même dans les REM.
Cause des deux « Fichier non trouvé » (`REM ... < 127`) et du fichier `GO.BAT)`.
5 commentaires reformulés, contrôle ajouté au vérificateur.

**Séparation en deux packs (2026-10-13, après le test du soir).**
Le pack ne tenait plus sur un CD (1,1 Go) et la Puzzle Collection / 3DMark2001
exigent 256 couleurs ou 16 bits : impossible avant le pilote graphique.
- **Pack 1 `Win98FR\`** (585 Mo) : installation de base inchangée ; l'étape [10/11]
  ne propose plus que VC++ 2008, QRes, 7-Zip, **RetroZilla** (navigateur jugé
  indispensable par l'utilisateur) et le **Jeu de Tarot**. Message final : installer
  les pilotes puis lancer le pack 2.
- **Pack 2 `Win98FR_Plus\`** (512 Mo) : `PLUS.BAT` (une question O/N par élément,
  pas de reprise ni de redémarrage automatique, redémarrage proposé à la fin si
  KernelEx ou DAEMON Tools ont été installés). `applis\` : firefox, vlc, winrar,
  imgburn, daemon, aida32, winamp, xnview, foxit, klcodec, jeux, puzzle, bench,
  kernelex (`KEX2019.EXE`, installé par `KEXCHK.BAT` si Firefox ou VLC est choisi
  et que `%WINDIR%\KERNELEX\KERNELEX.DLL` manque).
- Corrections du test : `PINBALL.INF` (liste de fichiers remplacée par du code
  Python par erreur de génération), `md` conditionnels (« répertoire existe
  déjà »), dossier **Programmes\Jeux** à la racine (`DEPLJEUX.VBS` y déplace
  Accessoires\Jeux et Microsoft Plus! 98\Jeux, dont Spider), **DirectX 9.0c**
  officiel = version de décembre 2006 déjà décompressée (`Win98FR_v2\07_DX\dx90c (copie de bkpWin98\cd\dx, supprimee)`,
  `DXSETUP.EXE /silent` direct), **Winamp** : pause le temps de fermer Winamp
  avant le patch FR, **Foxit** : dossier `Program Files\Foxit` (un dossier entre
  guillemets dans DestinationDirs n'était pas créé), **VLC** : `LIBQT_PLUGIN.DLL`
  aussi en mode XP SP3 (erreur de division à la fermeture, à valider),
  **Firefox** : DuckDuckGo Lite par défaut (`searchplugins\ddg-lite.xml`), barre
  de titre classique, accélération matérielle coupée.
- Test de nuit : **DAEMON Tools** plante au démarrage avec KernelEx →
  `applis\daemon\DAEMON.REG` : `AppSettings\Flags` `*\D-TOOLS\DAEMON.EXE` = 1
  (`KRF_KEX_DISABLE`). **VLC** plante encore à la fermeture même `vlc.exe` en XP SP3
  → `applis\vlc\VLCKEX.REG` : Flags = 2 (`KRF_OVERRIDE_PROC_MOD`, même mode pour tous
  les modules du processus, dont l'interface Qt) ; repli envisagé : VLC 2.2.8 (version
  réglée par jumper dans `KERNELEX.REG`). **3DMark03 3.60** : ne démarre pas sans
  KernelEx, et avec KernelEx `DLLHOST` plante dans `FMSI.DLL` (Futuremark SystemInfo
  2008) → chercher une version antérieure de 3DMark03 (build 3.2.0 à 3.4.0).
  Winamp 5.2 Full : imports tous présents dans 98 (sans KernelEx), anglais.
- **KernelEx désactivé par défaut** (choix de l'utilisateur) : `KEXOFF.REG`
  (`HKLM\Software\KernelEx` `DisableExtensions`=1), importé à la toute fin du pack 1
  (`:FINOK`, tout le pack 1 s'installe encore avec le réglage par défaut BASE, comme
  lors des tests validés) et par `KEXCHK.BAT` du pack 2. KernelEx ne s'applique plus
  qu'aux programmes réglés (`AppSettings\Configs` : Firefox, VLC, réglages de jumper)
  ou réglés à la main (onglet KernelEx des propriétés).
- **Benchmarks** (pack 2, `applis\bench\`, clés publiées par UL sur
  benchmarks.ul.com/legacy-benchmarks, copiées dans `C:\WINDOWS\BENCH_CLES.TXT` et
  affichées avant chaque installation) : 3DMark99 Max et 3DMark2000 (téléchargés sur
  UL), 3DMark2001 SE, **3DMark03 3.4.0** (InstallShield 7 de 2002, remplace la 3.60 de
  2008 → `_retires_Win98FR\3dmark03_360\`), PCMark2002 + Pro Pack, Fraps 1.9D.
- 2026-10-14 : **Fraps 1.9D** passe dans le pack 1 (`extras\applis\fraps`, étape
  [10/11]) ; **Winamp** : menu S/F/A/N = 5.2 Standard, 5.2 Full (anglais, imports tous
  présents dans 98, NSIS `/S`, pack de langue FR jugé mauvais) ou 2.91 FR ;
  **PCMark2002** retiré (plante pendant le test) → `_retires_Win98FR\pcmark2002\`.
  Battlefield 1942, 1280x1024 tout au maximum, DX 8.1 : 20 i/s en combat, 40 i/s
  sur la Bataille des Ardennes (sauvegarde `bkpWin98\Sauvegarde 4 aprés gros patch`).
  Navigateurs Pale Moon / lun3r : XP minimum + Visual C++ 2010, impossibles même
  avec KernelEx ; K-Meleon 74 (g22, build Win2000) fonctionne.
- 2026-10-14 (suite) : **3DMark03 3.4.0 validé** sous 98 sans KernelEx. **K-Meleon 74**
  (Goanna, build Win2000 g22) ajouté au pack 2 (`applis\kmeleon\`, 66 Mo) : profil
  d'origine (déjà utilisé) et langues autres que fr écartés, `zz_win98fr.js` (fr,
  DuckDuckGo Lite, sans accélération), KernelEx `BASE` + Flags 2 (le mode avec lequel
  l'utilisateur l'a testé), raccourcis Programmes et Bureau. Pack 2 : 620 Mo.
  3DMark2001 SE (1024x768, réglages de base, qualité haute) : 5 500 à 5 800 points.
- 2026-10-14 : **essai d'installeur à cases à cocher pour le pack 2** dans
  `Win98FR_Plus_Installeur/` (pack 2 inchangé pendant les tests) : `PLUS.nsi` (NSIS
  2.46, MUI2 français, page Composants groupée Navigateurs / Multimédia / Utilitaires
  / Jeux / Outils de test, descriptions) → `INSTALLER_PLUS.EXE` (64 Ko, imports 98
  vérifiés). Aucun logiciel embarqué : utilise `applis/` à côté de lui, sinon
  `../Win98FR_Plus/applis`. Mêmes actions que PLUS.BAT ; Winamp : une seule version
  installée (Full > Standard > 2.91) ; KernelEx installé en dernier si Firefox,
  K-Meleon ou VLC est coché et qu'il manque ; redémarrage proposé en fin si besoin.
- 2026-10-14 : **DAEMON Tools 3.47 passe dans le pack 1** (`extras/applis/daemon`,
  étape [10/11] après 7-Zip, `DAEMON.REG` = KernelEx désactivé pour lui ; son pilote
  s'active au redémarrage final). Retiré de PLUS.BAT et de l'installeur NSIS.
  **Alcohol 120% 2.0.3 écarté** : pilote SPTD et service StarWind (NT seulement),
  fonctions XP absentes même avec KernelEx (`RegisterServiceCtrlHandlerExA`,
  `CMP_WaitNoPendingInstallEvents`, `QueryServiceConfig2W`).
- 2026-10-14 : **archives 7z dans le pack 2** (solution 1) : FIREFOX.7Z (70→31 Mo),
  VLC.7Z (127→30), KMELEON.7Z (60→19), JEUX.7Z (16→4), PUZZLE.7Z (26→6), LZMA
  dictionnaire 16 Mo, décompressées par `applis/outils/7Z.EXE` + `7Z.DLL` (7-Zip 9.20,
  imports 98 vérifiés ; archives testées avec ce 7Z.EXE). Pack 2 : 620 → 391 Mo.
  Dossiers de travail non compressés : `win98se/_construction_pack2/` (sources texte
  de ces arbres dans scratchpad `src_stage`). **Puzzle Collection installée sans son
  installeur** : dossier `C:\Jeux\Puzzle Collection` repris de la Sauvegarde 4
  (fichiers identiques au CD), `PUZZLE.REG` = clés `MEP Puzzle\1.0` et Uninstall
  relevées dans son SYSTEM.DAT (lecteur CREG `creg_find.py`), `PUZZLE.INF` =
  raccourci Programmes\Jeux. Contenu du CD d'origine → `_retires_Win98FR/puzzle_cd_installeur/`.
- 2026-10-14 : `INSTALLER_PLUS.EXE` copié à la racine de `Win98FR_Plus` à côté de
  PLUS.BAT (utilisables séparément, même dossier applis). Source NSIS :
  `_construction_pack2/installeur/PLUS.nsi` (compiler puis recopier l'EXE dans le
  pack 2). L'ancien dossier d'essai `Win98FR_Plus_Installeur` est à supprimer.
- Puzzle Collection : l'utilisateur saisit sa clé ; une installation manuelle à
  partir d'une sauvegarde de l'utilisateur est envisagée.

**Mise à jour du 2026-10-13 : installeur unique.** `extras\kernelex\` ne contient
plus que `KernelEx-4.5.2019.24-FR.exe`, compilé (NSIS 2.46) depuis le dépôt
github.com/JasonHababou/KernelEx-4.5.2-FR : dossier `maj2019\` (fichiers de Jumper
+ `build_maj2019.py` qui produit les traductions et `core.ini`/`.reg` ci-dessous),
`.nsi` avec bascule `/DKEX452` pour l'ancien 4.5.2 seul. En plus : les 4 messages
d'erreur de `KernelEx.dll` traduits ; désinstallation des valeurs api-ms-win.
L'ancien `KernelEx-4.5.2-FR.exe` et `maj2019\` (INF/REG) sont dans
`_retires_Win98FR\kernelex_avant_installeur_unique\`.

**KernelEx 4.5.2019.24 de Jumper (`extras\kernelex\maj2019\`)** :
source `WIN9X\KernelEx-4.5.2019.24-TMT`. C'est un **kit de mise à jour** (pas
d'enregistrement du VxD, `UPDATE.BAT` « Updating KernelEx 4.5.2015 ») : il
s'applique par-dessus KernelEx 4.5.2 FR, juste après lui à l'étape [5/11],
avant tout redémarrage (fichiers pas encore en service).
- Apports : DLL du noyau 4.5.2016.18 à .24 (beaucoup plus d'API : `KEXBASES`
  569 Ko au lieu de 219 Ko), nouveaux modes **WINXP3** (XP SP3, requis par
  Firefox 31.8), WIN7A, WIN8/8.1, WIN10, réglages par programme étendus
  (Firefox portable, VLC, 7-Zip, Opera, Office…), DLL « api-ms-win » des
  programmes Windows 7.
- Repris : `KERNELEX.DLL` (v17, la v18 étant signalée cassée par Jumper),
  `KEXBASES`, `KEXBASEN`, `KEXCOM`, `MSIMG32`, `VKRNLEX.VXD`, `LICENSE.TXT` (GPL).
  Identiques à la 4.5.2, donc non repris : `PDH`, `PSAPI`, `UXTHEME`,
  `WTSAPI32`, `USERENV` ; `UNICOWS.DLL` = celui de SP3.0.
- **Traduit en français** : `SHEET.DLL` (onglet Compatibilité ; les identifiants
  de contrôles ayant changé, boîte refaite sur la mise en page de Jumper à partir
  de la traduction 4.5.2, + messages 2 et 6 restés en anglais traduits) et
  `VERIFY.EXE`, via Resource Hacker (sources `maj2019\src_fr\*.rc`) ;
  `CORE.INI` : 11 libellés de modes traduits.
- Corrigés : `CORE.INI` sans mode **NT2K** alors que `KERNELEX.REG` et la 4.5.2
  l'utilisent (Flash, Office, Google Earth…) → alias `[NT2K] inherit=WIN2000D`
  ajouté, comme dans le `CORE.20I` de Jumper ; `API-MS-W.REG` : 5 lignes aux
  guillemets mal formés.
- Écartés : `LZDLL.REG` (redirige `Dbghelp`, `Winhttp`… vers `LZ32.dll`),
  la redirection du gestionnaire de raccourcis (déjà faite par la 4.5.2), le
  `InstallDir` codé en dur, les fichiers de développement (`.C`, `.PDB`, `.MAP`,
  `APILOG`, `APIHOOK`).
- `FIREFOX.INF` : `xul.dll` en `WINXP3`.

### `maj2004\updates\` : 18 correctifs sur 23 retirés

Extraction des 23 correctifs et comparaison des versions avec SP2.CAB/SUPP.CAB
de SP3.0 : 18 sont **entièrement contenus dans SP3.0**, en version identique
ou plus récente et dans la même langue (238453, 245729, 249973, 256015,
259728, 273727, 273991, 274548, 314147, 314941, 323172, 323255, 329048,
329115, 811630, 823559, TelnetUp, js56mfr). `wuinfo.inf` de SP3.0 les
déclare installés pour Windows Update. Restent les 5 qui apportent quelque
chose d'absent de SP3.0 : **q240308, q313829, q330994 (OE6), q828750 (IE6),
KB819639 (WMP9)**.

Remarque `hhctrlui.dll` : 323255 et 811630 l'installent bien
(4.74.9273.0 FR), et c'est **exactement** celui de SP3.0 (`SUPP\HHCTRLUI.DLL`,
92 160 o) : aucune différence, aucune action.

### `sp30\` (nouveau) : mise à jour principale SP3.0 B4 FR

Absente jusqu'ici alors que le manifeste la supposait installée. Contient
les fichiers racine de `Sources\AfterLife Fr\SP30B4FR` utiles à `spupdate.inf` :
`SP2.CAB`, `SUPP.CAB`, `SLAYOUT1/2.INF`, `nircmd.exe`, `preserve.inf`,
`wuinfo.inf`, `tweaks.inf`, `w2kcolor.inf`, `instmsia.exe`, `q329414.exe`,
`rootsupd.cab`, `2_4date.exe`, `ADVPACK.DLL`, `W95INF16/32.DLL`.
`spupdate.inf` adapté (3 lignes neutralisées, commentées `[Win98FR]`) :
pas de fuseaux EN de SP2.CAB, pas de `TIMEZONE.EXE 02-0-2-03 02-0-1-11`
(dates d'heure d'été **américaines** appliquées au fuseau courant).
SP3.0 ne rétrograde rien : drapeaux 32/1056 = le fichier le plus récent
est conservé (IE6 n'est pas remplacé par ses fichiers IE5).

### Réorganisation : SP3.0 intact dans `sp30\`, lancé en natif

`sp30\` contient désormais **toute la racine de `SP30B4FR.EXE`** (CAB,
`MLAYOUT*/SLAYOUT*`, INF d'origine). Les composants SP3.0 ne sont plus
extraits dans `extras\` : `install.bat` les lance depuis `sp30\` avec leurs
INF d'origine, qui trouvent leurs fichiers dans les CAB (`NUSB.CAB`,
`meview.CAB`, `ADDITIONS.CAB`, `SP2.CAB`, `SUPP.CAB`).

| Composant SP3.0 (`infex.ini`) | INF lancé depuis `sp30\` | Étape |
|---|---|---|
| 0 Mise à jour principale | `spupdate.inf` (3 lignes neutralisées) | 2/10 |
| 10 Maximus Decim USB 3.3 FR | `NUSB.INF` | 5/10 |
| 9 Apparence Web Windows Me | `meview.INF` | 5/10 |
| 7 Utilitaires Windows Me | `ME-PROGS.inf` (ligne `scandskw.exe` EN neutralisée) | 5/10 |
| 8 Outil de conversion de l'euro | `euro.INF` (installé dans Program Files\EuroTool) | 5/10 |
| 4 TweakUI 1.33 FR | `tweakui.inf` | 5/10 |
| 14 Réglages de performance | `tweaks.inf` (après `extras\tweaks\TWEAKS366.INF`) | 5/10 |
| 5 WinTop | `wintop.inf` (identique à `wintop30.inf`) | 6/10, O/N |
| 6 Invite de commande ici | `doshere.inf` | 6/10, O/N |
| 13 Logos animés | `logo.inf` | 6/10, O/N |
| 1 WSH 5.6.8834 | `scr56.inf` : binaires EN comme ceux d'IE6 ; le FR vient des DLL de langue d'IE6 (`jsfr`, `vbsfr`, `wshfr`…), non touchées | 6/10, O/N |
| 12 Thème Windows 2000 | **exception** : `extras\w2kcolor\` (sur le Shell32 FR 2007) | 5/10 |
| 2 ASPI 4.60 | non utilisé (ASPI 4.71.2 Adaptec dans `extras\aspi\`) | — |
| 11 Notification mises à jour critiques | non utilisé (Windows Update n'existe plus pour 98) | — |
| 3 Désinstaller la MV Java | non utilisé | — |

`ADDITI~1.CAB` est renommé en **`ADDITIONS.CAB`**, le nom attendu par
`MLAYOUT2.INF` (Me-Progs et euro). Retirés d'`extras\` vers
`_retires_Win98FR\extras_issus_de_SP30\` : `nusb\`, `meview\`, `additi1\`
(dont `additi1.bat`), `tweakui\`, `tweaks.inf`. Les paragraphes
« `extras\nusb\`, `extras\meview\` » et « `extras\additi1\` » ci-dessous
sont donc **caducs**.

**WinTop** : l'ancienne mention « déjà ajouté manuellement, rien à faire »
plus bas était erronée (WinTop est le moniteur de tâches des PowerToys, pas
un remplacement du Bureau). Il est maintenant proposé en O/N.

### `systeme\copie363\` : 8 fichiers au lieu de 18

Retirés car **régression FR → EN** : `HYPERTRM.DLL` (FR 5.0 → EN XP),
`HTML32.CNV` (FR → EN), `XENROLL.DLL` (FR → EN), + `HYPERTRM.EXE/CHM/HLP`,
`HTICONS.DLL` (jeu HyperTerminal cohérent), `JSCRIPT.DLL` 5.7 EN
(contredisait le choix de garder WSH 5.6). Retirés car **identiques à
SP3.0** : `HHCTRL.OCX`, `SSDPAPI.DLL`, `SSDPSRV.EXE`, `UPNP.DLL`. Restent
(EN dans les deux versions, 3.63 plus récent) : `DUNZIP32`, `DZIP32`,
`HH.EXE`, `HHSETUP`, `ITIRCL`, `ITSS`, `MSCONV97`, `SNMP.EXE`.
`copie.bat` réécrit en COMMAND.COM, sauvegardes dans `C:\W98FR\BAK`.

### Utilitaires Windows Me (ex-`extras\additi1\`)

`SCANDISK.EXE` (3.63) et `scandskw.exe` ne sont plus installés : ils sont
**anglais**, et Windows 98 FR possède déjà les deux en français (ce
n'était pas un fichier « manquant »). Désormais via `sp30\ME-PROGS.inf`
(ligne `scandskw.exe` neutralisée).

### 6 INF tirés du 3.63/3.66 (+ WINTOP.INF, désormais remplacé par celui de SP3.0)

`PNTFS`, `MMC`, `REGCLEAN`, `SHAREDLL`, `ZIPFLDR`, `TTFEXT`, `WINTOP` :
source `SUPP.CAB` remplacée par `1=,,0` (fichiers livrés à plat).
Ajoutés dans `divers\` : `CIC.DLL`, `MMCNDMGR.DLL`, `MMCSHEXT.DLL`
(3.66 `SUPP`), `DUNZIP32.DLL`, `DZIP32.DLL` (mêmes versions que copie363,
évite un dialogue de conflit de version) et **`ZIPFLDR.DLL` FR**
(192 784 o, SP3.0 `SUPP`) à la place de la version EN du 3.66.

### Fuseaux horaires en français (`divers\TIMEZONE.INF` + `GMT.INF`)

SP3.0 n'a pas de fuseaux FR (son `timezone.inf` 2008 est en anglais).
Les INF du 3.66 (règles d'octobre 2020, 143 zones) ont été **traduits** :
libellés `Display` en français, et noms `Std`/`Dlt` repris de
`timezone.inf` de Windows 98 SE FR d'origine (`PRECOPY1.CAB`) quand la
zone existait (ex. « Paris, Madrid » / « Paris, Madrid (heure d'été) »).
L'appel `TIMEZONE.EXE /s 02:0:2:03 02:0:1:11` de `GMT.INF` est supprimé
(il imposait les dates d'été US). `install.bat` ouvre ensuite Date/Heure
pour re-sélectionner le fuseau. Originaux EN : `Sources\AfterLife Fr\U98SESP3.66`.

### `extras\plus98\`

L'appel direct de `Pls98Thm.inf` ne pouvait pas marcher (`layoutp.inf`
absent, LDID 42876 défini uniquement par l'installeur Plus!, et la
section `[Themes]` n'installe aucun thème). Remplacé par l'installeur
officiel du CD FR (`Plus! pour Windows 98.iso`, dossier `PLUS98\`) :
`INSTALL.EXE`, `LAYOUTP.INF`, `PLUS98.INF`, `PLUS98.CAB` (vérifié
identique au CD), et un **`MSBATCH.INF`** (lu automatiquement) qui ne
garde que « Thèmes du Bureau ». **Saisir votre clé** après `ProductID=` ;
laissée vide, l'installeur la demande. Section **`[Plus]`** (et non
`[Setup]`, qui n'était pas lue au 1er test réel) : retrouvée dans le code
d'`INSTALL.EXE`, qui lit `ProductID`, `Express`, `ShowEula`, `VirusScan`
et `AutoReboot` dans la section « Plus ». `AutoReboot=0` ajouté.

### `extras\w2kcolor\`

Le « patch en place » était inexact : les scripts ResHack visent des
copies dans le dossier courant (dans SP3.0, `spupdate` les extrait et
`runpost.bat`/`SHELL.INF` les installent). Nouveau `w2kcolor.bat` :
copie dans `C:\W98FR\W2K` du **Shell32 FR 2007** (`systeme\`), d'`EXPLORER.EXE`
4.72.3612.1710 FR et `MYDOCS.DLL` (SP2.CAB, dans `base\`), patch ResHack
(`W2K_EX/MD/SH.TXT`, chemins absolus), puis installation par
`W2KSHELL.INF` (remplacement au démarrage). `w2kcolor.inf` ne garde que
les couleurs et la purge du cache d'icônes. Ajoutés : `_sh_162.avi`,
`_sh_163.avi` (racine SP3.0).

### Autres corrections

- `ie_oe\` : KB823353/KB887797 étaient toujours sautés (test d'un `.inf`
  qui est dans l'exe). Q931768 est lancé par son installeur officiel
  `IEUPDATE.EXE Q931768` (l'argument est obligatoire : c'est ainsi que l'installeur officiel de q828750 lance `"ieupdate.exe" Q828750` ; signature `$Windows NT$` de l'INF probablement à
  l'origine de « Fichier INF non valide » via un appel direct).
- `extras\aspi\` : `ASPIINST.EXE` lancé directement (le `install.bat`
  Adaptec exigeait l'argument `X86` et n'installait rien sans).
- `extras\msagent\msagent_install.bat` : réécrit en COMMAND.COM.
- `materiel\directx\` : les deux 9.0c sont des archives IExpress →
  extraction `/Q /T:C:\W98FR\DX /C` puis `DXSETUP.EXE /silent`.
- `materiel\pilotes_phil\` : noms réels (`pentiumTo2\SETUP.EXE`,
  `vlatency\vlatency_v020_beta21.exe`, `5598_113\win98\SETUP.EXE`) ;
  `detect_chipset.vbs` lit le **pont hôte** (`BUS_00&DEV_00&FUNC_00`)
  au lieu du premier fabricant trouvé ; `VIA_HyperionPro_V524A\` retiré.
- `.NET 1.1` : `dotnetfx.exe /q:a /c:"install /q"`. Windows Installer 2.0
  est désormais installé par SP3.0 (`extras\dotnet\instmsia.exe` retiré).
- Nettoyage : dossier `config\` vide supprimé ; retirés vers
  `_retires_Win98FR\` : `Win98FR_squelette.zip`, `extras\dotnet\instmsia.exe`,
  `extras\nusb\_Start.bat` (appelait un `_nusb.inf` absent), et dans
  `extras\aspi\` le `install.bat` Adaptec + les fichiers XP/64 bits
  (`reg_xp.exe`, `aspixp.sys`, `wnaspixp.dll`, `aspi64.sys`, `wnaspi64.dll`).
- `extras\perso\perso.bat` est maintenant appelé **depuis son propre dossier**.

**Abandonné cette session : `extras\word97\` et `extras\office2000\`** —
retirés de la structure. Les seuls exemplaires trouvés (win3x.org) sont
des images ISO demandant une clé de CD que vous n'avez pas ; sans clé,
rien n'est installable. Si une clé ou une version sans protection est
trouvée un jour, le dossier pourra être réintroduit, mais `install.bat`
ne les appelle plus du tout pour l'instant.

---

## `maj2004\` — Couche 1 (chaîne officielle Microsoft, sécurité fév. 2004) — ✅ RÉSOLU cette session

**Changement important** : `install.bat` ne délègue plus à `W9XSetup.exe`.
D'après `WSEsetup.inf`/`WSEresume.inf`/`WSEfinish.INF` que vous avez
fournis, ces fichiers s'appuient sur `%49700%` (= `QSSourcePath`, écrit
dans le registre par le lanceur officiel du CD) pour reconstruire des
chemins absolus du type `content\win9x\common\...` — ça suppose l'arbo
exacte du CD d'origine, pas votre dossier `maj2004\` aplati, et la reprise
après chaque redémarrage repose sur des clés `Run` que Microsoft
réinscrit lui-même. Plutôt que de recréer artificiellement l'arbo du CD,
`install.bat` reproduit maintenant **lui-même, directement**, exactement
la même séquence de commandes que ces trois `.INF` (mêmes fichiers, mêmes
commutateurs silencieux, même ordre, mêmes 2 redémarrages), avec son
propre système de marqueurs de reprise déjà utilisé ailleurs dans le
script.

**Structure attendue, à la racine de `maj2004\`** (aplatie, sans le
`content\win9x\` d'origine) :
```
maj2004\
├── ie6sp1\        ← tout le contenu de content\win9x\common\IE6SP1\
│   └── ie6setup.exe (+ tous les .cab)
├── wmp9\          ← tout le contenu de content\win9x\common\WMP\WMP9\
│   └── MPSetup.exe
├── directx9b\     ← tout le contenu de content\win9x\common\DirectX9b\
│   └── DX9_98.EXE
├── mdac28\        ← MDAC_TYP.EXE **remplacé par la version SP1 FR** (cf.
│   └── MDAC_TYP.EXE   décision MDAC plus bas, ne pas utiliser l'EXE 2004)
├── updates\       ← les 23 fichiers ci-dessous UNIQUEMENT, aplatis
│   └── (voir liste exacte plus bas)
└── winsub_b.reg   ← fourni, équivalent de WSEfinish.INF (marque le
                      système comme mis à jour), appliqué automatiquement
                      en tête de la Couche 2
```

**Les 23 fichiers exacts à mettre dans `updates\`** (strictement ceux
listés dans `[UPD_INST_Post]` de `WSEresume.inf`, rien d'autre) :
`238453fr8.EXE`, `245729fr8.exe`, `256015FRN8.EXE`, `259728FRN8.EXE`,
`273727FRN8.EXE`, `314147FRN8.EXE`, `329048FRN8.EXE`, `249973FRN8.exe`,
`274548FRN8.EXE`, `323172FRN8.EXE`, `329115FRN8.EXE`, `811630FRN8.EXE`,
`823559FRN8.EXE`, `273991FRN8.EXE`, `314941FRN8.EXE`, `323255FRN8.EXE`,
`TelnetUp.EXE`, `q240308.exe`, `q313829.exe`, `q330994.exe`,
`q828750.exe`, `js56mfr.exe`, `KB819639.EXE` — provenance : `maj2004\
Win98\updates\` tel que vous l'aviez déjà extrait.

**À retirer de `maj2004\`** (plus utilisés par le script) :
- `W9XSetup.exe` et `NoPM.exe` — plus appelés, la séquence est reproduite
  directement
- **Tout le dossier `WinME\`** — mauvais OS cible (Windows Me, pas 98 SE),
  à supprimer entièrement
- **4 fichiers orphelins** trouvés dans `Win98\updates\` mais **jamais
  appelés** par `WSEresume.inf` : `168115fr8.exe`, `KB817787.EXE`,
  `wm320920_71.exe` (idem pour `common\WMP\WMP7_1\MP71.exe`, superflu
  puisqu'on installe WMP9) et `wucsp.exe` (confirme le doute déjà noté :
  ce n'est pas dans la chaîne officielle, donc redondant/inutile — ne pas
  l'ajouter)

Côté `install.bat` : l'étape `[1/9]` est désormais en 2 phases avec son
propre couple de marqueurs de reprise (`C:\W98FR_C1P2_T.TXT` /
`C:\W98FR_C1P2_E.TXT`, distincts des marqueurs `C:\W98FR_T.TXT` /
`C:\W98FR_E.TXT` qui gèrent la bascule vers la Couche 2) :
- **Phase 1** (avant 1er redémarrage) : `ie6sp1\ie6setup.exe /Q:C /R:N`
  puis `wmp9\MPSetup.exe /Q:U /R:N`
- **Phase 2** (après le 1er redémarrage, reprise auto) : les 23
  correctifs avec `/q:u /r:n` (ou `/q:a /r:n` pour les 4 que Microsoft
  installe en mode tout-silencieux : 329048, 274548, 314941, KB819639,
  conformément à `WSEresume.inf`), puis `directx9b\DX9_98.EXE /q:a /r:n`,
  puis `mdac28\MDAC_TYP.EXE /Q /C:"DASETUP /Q /N"`
- Au tout début de la Couche 2 (`:COUCHE2_SYSTEME`) : import de
  `maj2004\winsub_b.reg` (`HKLM\Software\Microsoft\Windows\CurrentVersion
  \SubVersionNumber = "B"`), équivalent exact de ce que faisait
  `WSEfinish.INF` pour marquer le système à jour.

### ❌ Retiré de cette couche : Y2K_1.exe / Y2K_2.exe

Décision changée (vous aviez raison de douter) : **Windows 98 Second Edition
intègre déjà les correctifs Year 2000** au moment de sa sortie (mai 1999,
postérieure aux patches Y2K distribués pour le Windows 98 d'origine/FE).
Ces deux exécutables, repérés dans `updates_win98fr.zip`, étaient prévus
pour les utilisateurs qui mettaient à niveau un Windows 98 première édition
vers SE — ils sont sans objet ici puisque vous partez d'un Windows 98 **SE**
d'origine propre. Ne pas les ajouter à `maj2004\`. (Si un doute subsiste,
vérifiable via le Panneau de configuration Ajout/Suppression de programmes
après installation propre : aucune icône de patch Y2K n'apparaît sur un
SE vierge, signe qu'il n'y a rien à appliquer par-dessus.)

### ❌ Confirmé exclu : `Service Pack (Vanilla).exe` (= wucsp.exe)

Présent dans `maj2004\Win98\updates\` mais **absent de la liste
`[UPD_INST_Post]` de `WSEresume.inf`** (vérifié ligne à ligne cette
session) : il ne fait pas partie de la chaîne officielle Microsoft. Ne
pas l'ajouter à la Couche 1 reconstruite — redondant par hypothèse,
confirmé non nécessaire par son absence du script officiel.

## `systeme\` — Couche 2 : corrections système post-2004

- `SHELL98.INF` + `SHELL32.DLL` — **Provenance : "Shell98 FR révisé"**
  (paquet FR daté du 2007-05-03, cf. journal §1)
- `Q918547.INF` + `GDI.EXE` + `GDI32.DLL` — **Provenance : "Q918547 FR"**
  (daté 2006-04-10/2007-05-05, cf. journal §1)
- Dans `systeme\copie363\` : les fichiers où le 3.63 l'emporte —
  **Provenance : `SP3.CAB` / `SUPP.CAB` de U98SESP3.63 (EN)** :
  `SNMP.EXE`, `DUNZIP32.DLL`, `DZIP32.DLL`, `HTICONS.DLL`, `HYPERTRM.DLL`,
  `HYPERTRM.EXE`, `XENROLL.DLL`, `HTML32.CNV`, `MSCONV97.DLL`, `SSDPAPI.DLL`,
  `SSDPSRV.EXE`, `UPNP.DLL`, `JSCRIPT.DLL`, `HH.EXE`, `HHCTRL.OCX`,
  `HHSETUP.DLL`, `ITIRCL.DLL`, `ITSS.DLL`
  **⚠️ NE PAS inclure `hhctrlui.dll`** — garder celui déjà présent dans
  Windows (**provenance : votre SP3.0 Beta 4 FR**, 92160 octets, confirmé
  identique au patch officiel KB811630/323255 FR, cf. journal §1)
- Créez `copie363\copie.bat` : un script simple qui copie chaque fichier
  listé ci-dessus vers `%WINDIR%\SYSTEM` (avec sauvegarde `.bak` de
  l'original avant écrasement, par prudence)

## `ie_oe\` — Couche 2 : IE/OE plus récents que la couche 1

- `KB823353-OE6sp1.exe` — **Provenance : correctif officiel Microsoft FR**
  (contient `Q823353.inf`, juin 2004)
- `KB887797-OE6sp1.exe` — **Provenance : correctif officiel Microsoft FR**
  (contient `Q887797.inf`, octobre 2004 — s'applique **après** KB823353)
- Le contenu de `IE6_918899 Fr.zip` — **Provenance : votre archive FR**
  (contient en réalité `Q931768.inf`, 2007-02-19 — comble aussi
  `SHDOCVW/SHLWAPI/URLMON/MSHTML.DLL`)

## `extras\nusb\` et `extras\meview\` — ✅ vérifié cette session : complets, il manquait juste le `.INF` racine

**Provenance : `SP30B4FR.EXE`** (SP3.0 Beta 4 FR). Vérification croisée
faite entre `NUSB.INF`/`meview.INF` (sections `[Copy.*]`) et le listing
réel `Win98FR-12102026.txt` fourni cette session :

- **`extras\nusb\`** : les 31 fichiers de données listés par `NUSB.INF`
  (`QFECheck.exe`, `explorer.exe`, les `.SYS` 1394/USB/NTMAP, `ios.vxd`,
  `hotplug.dll`, `systray.exe`, `user.exe`/`user32.dll`, les `.pdr`,
  `DISKTSD.VXD`, `cdvsd.vxd`, les `.hlp`, et les INF secondaires
  `1394.INF`/`ntmap.inf`/`usbstor.inf`/`usbntmap.inf`/`NODRIVER.INF`/
  `usb2.inf`/`_usb2un.inf`) sont **tous présents** — l'extraction était
  bien complète. Seul **`NUSB.INF` lui-même** (le point d'entrée
  `DefaultInstall` appelé par `install.bat`) manque à la racine du
  dossier : copiez-le depuis `SP30B4FR\NUSB.INF` (fichier déjà fourni,
  lu et vérifié cette session). Pas de contenu visible en FR/EN dans ce
  fichier (que des sections INF), donc aucune question de langue.
- **`extras\meview\`** : les 27 fichiers Web View listés par
  `meview.INF` section `[Copy.Web]` (`CONTROLP.HTT`, `default.htt`,
  `DESKMOVR.HTT`, `dialup.htt`, `FOLDER.HTT`, `ftp.htt`, `IEJIT.HTM`,
  `JITALERT.GIF`, `MYCOMP.HTT`, `nethood.htt`, `OFFLINE.HTM`,
  `PRINTERS.HTT`, `recycle.htt`, `RELATED.HTM`, `SAFEMODE.HTT`,
  `schedule.htt`, `TIP.HTM`, `TIPS.GIF`, `webview.css`, `WUICON1/2.GIF`,
  `WULOGO.GIF`, `WUM.HTM`, `WVBACK.GIF`, `wvleft.bmp`, `wvline.gif`,
  `WVLOGO.GIF`) plus `winMeIco.dll` sont **tous présents** — extraction
  complète confirmée, mon signalement précédent de fichiers manquants
  était une erreur de ma part. Seul **`MEVIEW.INF`** manque à la racine :
  copiez-le depuis `SP30B4FR\meview.inf`.
  - Note : `meview.INF` contient sa propre section `[AddReg.Win2KColor]`,
    identique octet pour octet à celle de `w2kcolor.inf` ci-dessous —
    appliquer les deux revient à réécrire deux fois les mêmes clés de
    thème. Sans danger, juste redondant.

**Sur la proposition « ne garder que le `.CAB` + le `.INF` et laisser
Windows extraire à l'installation »** : techniquement valide (le
mécanisme `[SourceDisksNames]`/`[SourceDisksFiles]` d'un INF peut
pointer vers un `.CAB` et extraire à la volée), mais **pas retenu** ici :
nos deux `.INF` utilisent `[SourceDisksNames]` avec un `%nn%\Precopy` ou
un chemin CD d'origine selon les cas, pas un chemin relatif portable —
il faudrait les réécrire pour pointer proprement vers un `.CAB` local
livré à côté du `.INF`, ce qui ajoute un risque de régression pour un
gain nul (les fichiers déjà extraits fonctionnent et pèsent peu). On
garde donc l'extraction à plat, juste complétée par le `.INF` manquant.

## `extras\additi1\`

**Provenance principale : `ADDITI~1.CAB` de `SP30B4FR.EXE`**, complété par
**`SCANDISK.EXE` récupéré du 3.63** (mode texte, seul fichier réellement
manquant de ce lot, cf. journal §3). Créez `additi1.bat` pour copier
`DEFRAG.EXE`, `Regedit.exe`, `scandskw.exe`, `SCANDISK.EXE`, `Mypics.scr`,
`Netpptp.sys`, `WUCrtUpd.exe` vers les bons dossiers.

## `extras\kernelex\` — ✅ RÉSOLU cette session (mis à jour vers 4.5.2 FR)

**Provenance : `KernelEx-4.5.2-FR.exe`**, traduction française maison de
KernelEx **4.5.2** réalisée et testée par vos soins :
[github.com/JasonHababou/KernelEx-4.5.2-FR](https://github.com/JasonHababou/KernelEx-4.5.2-FR).

Contrairement à la 4.5 Final FR (traduction de l'installeur NSIS
lui-même), cette traduction procède par **transplant de ressources** :
elle part des DLL/EXE **précompilés officiels** de la 4.5.2 (anglaise) et
remplace leurs ressources (boîtes de dialogue, chaînes) par des versions
françaises via Resource Hacker, avant de reconstruire l'installeur avec
NSIS 2.46 (toolchain Docker fournie dans le dépôt : `build_res.sh` →
`inject_all.ps1` → compilation du `.nsi`). Remplace l'ancienne version
`KernelEx-4.5-Final-FR.exe`, qui n'est plus utilisée dans le pack.
`install.bat` appelle désormais `extras\kernelex\KernelEx-4.5.2-FR.exe`
à l'étape `[4/9]`.

## `extras\ntfs\`

- **Changé le 26/10/2026** : le pilote est maintenant **Paragon UFSD corrigé par
  SweetLow** (`UFSD.VXD`, qui corrige les fuites de mémoire et le nom ou numéro de volume),
  avec `PNTFSHLP.VXD`. Ce sont les mêmes fichiers que l'option NTFS de QuickInstall
  et le pack WinMeFR, et le même `PNTFS.INF` que le pack ME. Les notices sont
  `UFSD.TXT` et `PNTFSHLP.TXT`, en noms 8.3 (avec deux points dans le nom, le CD
  ne les trouvait pas). L'ancien `PNTFS.VXD` de 2003 est dans
  `_a_supprimer\ntfs98_2026-10-26`. Le configurateur `NTFSCFG.VBS` ne change pas :
  il ne touche que la Corbeille.
- `PNTFS.INF`, `PNTFS.VXD` (remplacé, voir ci-dessus), `DELPART.EXE`, `PNTFS.ICO` —
  **Provenance : `SUPP.CAB` du 3.63, section Paragon**
- `PNTFS.VBS` — **déjà traduit en français par vos soins** dans ce projet
  (9 chaînes remplacées, cf. journal §3 "Lecteur NTFS ✅ TERMINÉ") — pensez
  à harmoniser le libellé du raccourci Bureau dans `PNTFS.INF` section
  `[UIS]` en même temps
- ⚠️ **Remplacé (2026-10-20, test QEMU de l'ISO test12)** : `PNTFS.VBS` passait par
  WMI (`GetObject("winmgmts:…StdRegProv")`). WMI échoue sous 98 avec l'erreur
  800A01B0, même avec le composant WMI du CD, la mise à jour WMI 1.5 du SP3.0 ou
  WMI Core 1.5. Il est remplacé par **`NTFSCFG.VBS`**, écrit pour le pack. Le
  résultat est le même : le bit « supprimer directement » de chaque lecteur choisi
  dans `BitBucket\PurgeInfo`. Le script lit la valeur avec `WScript.Shell.RegRead`
  et l'écrit avec un `.REG` importé par `REGEDIT /S`, sans WMI. Testé : bits E et F
  écrits (0x30). `PNTFS.VBS` et `WMICORE.EXE` sont dans
  `_retires_Win98FR\ntfs_wmi_2026-10-20`.

## `extras\msagent\`

⚠️ **Remplacé (2026-10-13, après le 1er test réel)** : le build 3427
décrit ci-dessous est **incompatible Windows 98** (`AGENTSVR.EXE` et
`AGENTPSH.DLL` importent `GetSystemDefaultUILanguage`, absent du KERNEL32
de 98 → erreur « exportation manquante » au test). Ce n'était pas non plus
« le même build que le 3.66 » : 3.66 utilise **2.00.0.2202**. Le dossier
contient désormais les installeurs officiels Microsoft pour Win9x :
`MSAGENT.EXE` (moteur 2.00.0.2202, `Microsoft_Agent.iso` →
« Microsoft Agent Core Components.zip », même `AGENTSVR.EXE` que 3.66) et
`AGTX040C.EXE` (langue FR 2.00.0.2115, identique dans `Sources\AfterLife Fr\` et
dans l'ISO ; l'ancienne mention « incompatible » plus bas était fausse).
`msagent_install.bat` lance les deux en `/q:a /r:n`. Fichiers 3427 retirés
vers `_retires_Win98FR\msagent_3427_XP\`. Ancien texte :

**Provenance : `MsAgent3427.zip`** (= le même build que celui embarqué dans
le 3.66, cf. journal §3). Copiez le dossier `msagent\` complet, avec son
sous-dossier `intl\` — **ne pas retirer `intl\agt040c.dll`**, c'est lui qui
assure le français automatiquement, sans traduction supplémentaire
nécessaire.

**✅ RÉSOLU cette session** : confirmé que `MsAgent3427.zip` est bien un jeu
de DLL brutes sans installeur. `msagent_install.bat` est fourni (copie
`agent*.dll`, `agtctl15.tlb`, `agtintl.dll`, `mslwvtts.dll` et le
sous-dossier `intl\` vers `%WINDIR%\msagent\`, puis enregistre
`agentctl.dll` via `REGSVR32 /S`). `install.bat` l'appelle désormais à
l'étape `[4/9]`, **optionnel** (case à cocher O/N à chaque installation,
comme demandé).

## `extras\plus98\` — ✅ corrigé cette session (ma consigne précédente était fausse)

**Correction importante** : après lecture du vrai `PLUS98.INF` que vous
avez fourni, mon instruction précédente (`RUNDLL32 ADVPACK.DLL,
LaunchINFSection PLUS98.INF,DefaultInstall`) était fausse et n'aurait
rien fait. `PLUS98.INF` **n'a pas de section `[DefaultInstall]`** : c'est
le manifeste maître du CD retail Plus! 98, lu par l'assistant
`INSTALL.EXE` lui-même, pas un petit INF autonome comme `NUSB.INF`. Il ne
contient que `[SetupInstall]` (juste de l'enregistrement registre) et des
sections par composant (`BaseInstall`, `WebCD`, `Tuneup`, `Cleanup`,
`ZipFldr`, etc.) — **aucune d'entre elles n'installe les Thèmes du
Bureau**. Cette partie-là est déléguée à un fichier compagnon,
`Pls98Thm.inf` (section `[Themes]`), référencé dans `PLUS98.INF` via
`Components.Reg` mais jamais fourni séparément — regardez dans
`PLUS98.CAB`, il doit y être avec `Pls98Gam.inf`/`Pls98App.inf` (listés
dans `[Plus.Files.Inf]`).

**Ce qu'il faut réellement dans `extras\plus98\`** :
- `PLUS98.CAB` (déjà présent)
- `Pls98Thm.inf` — à extraire de `PLUS98.CAB` (c'est lui qui compte,
  section `[Themes]`)
- `PLUS98.INF`, `LayoutP.inf`, `MSBATCH.INF` que vous avez fournis **ne
  sont plus nécessaires** dans cette approche minimaliste : `LayoutP.inf`
  ne sert qu'à `INSTALL.EXE` pour localiser les CAB du CD complet (pas
  utile si on cible juste `Pls98Thm.inf`), et `MSBATCH.INF` est un
  fichier de réponses pour une installation complète non assistée via
  `INSTALL.EXE` (désélectionne juste "Golf 1998 Lite", probablement un
  fragment incomplet d'un fichier plus large) — on n'en a pas besoin
  puisqu'on n'appelle pas `INSTALL.EXE` du tout.

`install.bat` a été corrigé pour appeler :
```
RUNDLL32 ADVPACK.DLL,LaunchINFSection "extras\plus98\Pls98Thm.inf",Themes
```
à la place de l'ancien appel erroné sur `PLUS98.INF`. Il ne me manque
plus que le contenu de `Pls98Thm.inf` — si vous pouvez l'extraire de
`PLUS98.CAB` et me le montrer, je peux vérifier que la section `[Themes]`
correspond bien à ce qu'on veut (pas de dépendance à `BaseInstall` pour
les fichiers communs type `logo.sys`, etc.).

## `extras\taskbarshuffle\`

**Provenance : `ts2.5_setup.exe` repéré dans `WUPG98.EXE\w\`** (pack
AfterLife/WUPG98).

## `materiel\pilotes_phil\` — fichiers reçus cette session, menu corrigé

- **`intel\pentiumTo2\`** — paquet Intel INF Update Utility couvrant
  uniquement Pentium / Pentium MMX / Pentium Pro / Pentium II, ajouté
  comme 3e choix du sous-menu Intel (`install.bat` [8/9], option C).
- **`intel\3201008\` et `intel\6301007\`** — correction : le fichier
  présent dans ces deux dossiers est `infinst_enu.exe` (pas `SETUP.EXE`
  comme précédemment écrit dans `install.bat` — corrigé cette session).
  Switch silencieux de `infinst_enu.exe` non encore vérifié : à tester en
  VM, pour l'instant il s'exécute avec son assistant visible.
- **`sis\530_5598\530_108\` et `\5598_113\`** — ce sont deux chipsets
  SiS différents (SiS530 et SiS5598/5597), gardés tous les deux à raison :
  le sous-menu SiS a été scindé en conséquence (`install.bat` [8/9],
  désormais A=530, B=5598, C=agp121, D=ide204a). Le 530 a un
  `530_108\Win98\REGMOD.EXE` (installeur silencieux classique de l'époque,
  utilisé). Le 5598 n'a **aucun installeur** dans `5598_113\win98\` (juste
  les `.DLL`/`.SYS` bruts) : installation manuelle uniquement via le
  Gestionnaire de périphériques (Mettre à jour le pilote → pointer vers ce
  dossier) — `install.bat` l'indique à l'écran au lieu de deviner un
  exécutable qui n'existe pas.
- **`via\hyperion\`** — contient `VIAHyperion4in1456v.exe` (le pilote
  classique compatible Win9x, c'est celui-là qu'`install.bat` appelle) et
  un sous-dossier `VIA_HyperionPro_V524A\` : **⚠️ à supprimer**, c'est un
  paquet chipset moderne (installeur MSI, DIFXAPI, signature de pilotes,
  dossiers Vista/7/x64/Server2003) totalement incompatible avec Windows
  98 — rien à voir avec l'ancien "Hyperion Pro" 9x malgré le nom, ne le
  gardez pas dans le pack.

## `materiel\ess_allegro\`

**Provenance : vos propres pilotes ESS Allegro** (VXD 4.12.00.713 ou
4.12.01.7130) déjà testés et validés sur votre machine réelle, + les
pilotes DOS (TSR SB Pro). Ce dossier n'est pas appelé automatiquement par
`install.bat` (installation manuelle recommandée) — gardez-le ici pour
archive/réinstallation future.

## `materiel\rloew\`

**Provenance : `rudolph_r._loew_patches.zip`** : `PATCHMEM.EXE`,
`SPLIT8MB.EXE`, `FIX95CPU.EXE`. **Rappel impératif** : ces outils doivent
être lancés en tout dernier, après un redémarrage avec tout le reste déjà
installé — `install.bat` le rappelle et demande confirmation avant de les
lancer.

## `extras\aspi\` — ✅ RÉSOLU

**Provenance : `aspi_471a2.exe`** (Adaptec officiel, touslesdrivers.com).
Ce n'est pas un simple exécutable : c'est une archive auto-extractible
contenant `aspiinst.exe` (le vrai installeur) + ses fichiers d'appui, et
surtout **son propre `install.bat` officiel** qui appelle `aspiinst.exe`
avec les bons paramètres. Extrayez **tout le contenu** de l'archive dans
`extras\aspi\` (`aspiinst.exe`, `install.bat`, les `.sy_`/`.vx_`/`.dl_`
compressés, `include\`, `Docs\`, etc.) — `w\install.bat` appelle
maintenant `extras\aspi\install.bat` directement (`call`), qui se charge
lui-même d'invoquer `aspiinst.exe` correctement. Plus besoin de deviner
des paramètres de ligne de commande.

⚠️ Note de cohérence : SP3.0 Beta 4 FR et U98SESP3.66 embarquent *chacun*
déjà un ASPI plus ancien (`aspi.inf` + `ASPIENUM.VXD`/`WINASPI.DLL`/
`WNASPI32.DLL`, datés 2005-11-30 pour le FR et 1999/2002 pour le 3.66).
Le `WNASPI32.DLL` du 3.66 est daté du **2002-07-17**, exactement la même
date que les fichiers de votre `aspi_471a2.exe` — confirmation que
4.71.2 est bien la version "de référence" déjà utilisée par ces deux
packs. **Décision : utiliser uniquement `aspi_471a2.exe`**, ne pas
dupliquer avec l'ASPI plus ancien du SP3.0B4FR (`aspi.inf`), qui reste
inutilisé.

## `extras\mspaintfilter\` — nouveau, ✅ RÉSOLU

**Provenance : `WUPG98.EXE\mspaintfilter\`** (AfterLife/WUPG98). Ce
dossier existe déjà tout prêt dans votre archive WUPG98 et correspond
exactement à l'élément "Microsoft Paint Graphic Filters + Image Preview
5.50.4134.100" que vous aviez repéré comme manquant. Copiez-y :
`EPSIMP32.FLT`, `GIFIMP32.FLT`, `JPEGIM32.FLT`, `TIFFIM32.FLT`,
`WMFIMP32.FLT` et `install filter.reg` (avec l'espace dans le nom,
respectez-le). `install.bat` importe ce `.reg` puis copie les `.FLT`
vers `%WINDIR%\SYSTEM\` à l'étape `[4/9]`.

## `extras\dotnet\` — **optionnel**, 2 choix indépendants (✅ net10 retiré cette session)

Sources exactes localisées dans votre dossier `New\` :

- **`InstMsiA.exe`** (racine de `extras\dotnet\`) — **Provenance : racine
  de `SP3.0 Beta 4 FR`** (`instmsia.exe`, Windows Installer 2.0 officiel
  Microsoft, daté 2001-03-01, build 2.0.2600.2). Egalement présent à
  l'identique à la racine de `U98SESP3.66` et dans `WUPG98.EXE\ups\
  instmsia.exe` — les trois sont la même version, prenez celui du
  SP3.0B4FR par cohérence de provenance. Prérequis commun installé une
  seule fois si au moins un des deux choix .NET ci-dessous est pris.
- ~~`extras\dotnet\net10\`~~ — **retiré** : vous n'avez gardé que 1.1 et
  dotnet9x à disposition, `install.bat` ne pose plus la question .NET 1.0.
- **`extras\dotnet\net11\`** — **Provenance : `New\net-framework11\`** :
  `dotnetfx.exe`, `langpack.exe`, `KB867460-X86.exe`,
  `KB886903-X86.exe`, dans cet ordre précis (celui que vous avez donné).
  .NET Framework **1.1** — supporté officiellement par Windows 98 SE.
  Plus `NOPOSTNG.INF` (ajouté le 26/10/2026, repris du pack ME) : retire de
  RunOnce la précompilation `NetFxUpdate_v1.1.4322` (« Postngen »), qui ne
  finissait jamais sous 9x et bloquait l'arrêt de Windows.
- **`extras\dotnet\net20\`** — **Provenance : à télécharger depuis les
  Releases GitHub d'[itsmattkc/dotnet9x](https://github.com/itsmattkc/dotnet9x)**,
  fichier `dotnet9x.exe`. ⚠️ **Ce n'est PAS le contenu actuel de votre
  dossier `New\net-framework20\`** (`dotnetfx.exe`/`langpack.exe`
  standards Microsoft) — ces fichiers-là sont le redistribuable .NET 2.0
  classique, qui ne fonctionne pas sur Windows 98 sans le patch du
  projet dotnet9x. Il faut le fichier `dotnet9x.exe` distinct, propre au
  projet. **Point de vigilance** : la documentation du projet
  (lue cette session) décrit surtout des prérequis pour **Windows 95**
  (IE 5.01, Microsoft USB Supplement patchant VMM32.VXD) et ne confirme
  pas explicitement la compatibilité Windows 98 — le .NET 2.0 y est
  qualifié de "largement fonctionnel", le 3.5 de "tout juste commencé".
  **À tester en VM avant la machine réelle**, `install.bat` l'affiche
  d'ailleurs comme "EXPÉRIMENTAL" à l'écran.

`install.bat` pose maintenant 3 questions indépendantes (1.0 FR ? / 1.1 ?
/ 2.0 expérimental ?) à l'étape `[7/9]`, chacune optionnelle, jamais
automatique même en mode Tout.

## `materiel\pilotes_phil\` — nouveau, détection automatique du fabricant

**Détection** : `detect_chipset.vbs` est fourni — il exporte la clé
registre `HKLM\Enum\PCI` via `regedit /e` (pas de dépendance WMI, non
garantie présente sur un Win98 SE propre), cherche les préfixes
`VEN_8086` (Intel) / `VEN_1106` (VIA) / `VEN_1039` (SiS), et écrit le
résultat dans `C:\CHIPSET.BAT` (`set CHIPSET=...`) qu'`install.bat` relit
ensuite — même mécanisme que le marqueur de reprise de la Couche 1.
**Limite assumée** : la détection s'arrête au fabricant, pas au modèle
exact de chipset (440BX vs 915, KT133 vs KT400, etc.) — après détection,
`install.bat` affiche directement votre tableau de paquets par fabricant
et vous laissez choisir le bon modèle à la main à l'étape `[8/9]`.

Dossiers reçus cette session, exécutable réel entre parenthèses (`install.bat`
mis à jour en conséquence) :

| Dossier | Paquet | Exécutable |
|---|---|---|
| `intel\3201008\` | Intel 3.20.1008 (2001) — 440BX/LX/GX, 810, 815 | `infinst_enu.exe` |
| `intel\6301007\` | Intel 6.3.0.1007 (2004) — série 800 + 915/925 et suivants | `infinst_enu.exe` |
| `intel\pentiumTo2\` | Intel — Pentium/Pentium MMX/Pentium Pro/Pentium II uniquement | `infinst_enu.exe` |
| `via\4in1_435v\` | VIA 4in1 4.35v (2001) — chipsets anciens (KT133, KT266) | `SETUP.EXE` |
| `via\hyperion\` | VIA Hyperion 4.56v — chipsets récents (KT400+, P4X400+) | `VIAHyperion4in1456v.exe` (⚠️ retirer `VIA_HyperionPro_V524A\`, incompatible 9x, cf. plus haut) |
| `via\vlatency\` | VIA vlatency — seulement si problèmes son/USB/IDE sur chipset VIA | `SETUP.EXE` |
| `sis\530_5598\530_108\` | SiS 530 — graphique intégré SiS530 | `Win98\REGMOD.EXE` |
| `sis\530_5598\5598_113\` | SiS 5598 — graphique intégré SiS5597/5598 | aucun, pilote manuel (Gestionnaire de périphériques) |
| `sis\agp121\` | SiS agp121 — AGP SiS 6xx/7xx | `setup.exe` |
| `sis\ide204a\` | SiS ide204a — IDE SiS 96x, 630, 730 | `SETUP.EXE` |

Toute cette couche reste **optionnelle**, demandée à chaque fois.

---

## `extras\w2kcolor\`, `extras\tweakui\`, `extras\tweaks\` — nouveau, ✅ RÉSOLU cette session

### Thème Windows 2000 (`w2kcolor`)

**Conflit confirmé entre les deux versions** (lecture complète des deux
fichiers cette session) :

- **`W2KCOLOR366.INF`** (SP3.66) : `[DefaultInstall]` fait d'abord
  `RunPreSetupCommands=ESF:1` → `EXTRACT.EXE /Y /E SP3.CAB EXPLORER.EXE
  MYDOCS.DLL SHELL32.DLL` (ressort les 3 binaires **d'origine 2000-2001**
  du vieux `SP3.CAB`), les copie sous `EXPLORER.TMP`/`MYDOCS.TMP`/
  `SHELL32.TMP`, puis `RunPostSetupCommands=PSF:1` lance `W2KCOLOR.BAT`
  qui patch leurs ressources (`RESHACK.EXE`) puis les **substitue aux
  vrais fichiers**. Résultat : `SHELL32.DLL`/`EXPLORER.EXE`/`MYDOCS.DLL`
  seraient **remplacés** par de vieux binaires EN ressourcés, écrasant le
  Shell98 FR 2007 déjà installé plus haut dans `install.bat`. **Écarté.**
- **`w2kcolor30.inf`** (SP3.0 B4 FR) : `[DefaultInstall]` ne fait que
  `AddReg` (couleurs/polices, blob identique aux deux autres versions) +
  `RunPostSetupCommands` → `RESHACK.EXE -script _EX.TXT` / `_MD.TXT` /
  `_SH.TXT` (patch de ressources **en place**, sur les fichiers déjà
  installés — pas de copie/substitution) + `DelFiles=Del.Windows`
  (supprime le cache d'icônes `Shelli~1` pour forcer sa reconstruction).
  **Ne touche jamais au contenu binaire** de Shell32/Explorer/Mydocs.
  **Retenu.**

**Fichiers nécessaires**, tous déjà présents **à la racine de votre dump
`SP30B4FR`** (vérifié dans `SP30B4FR.txt` cette session — pas besoin
d'extraire quoi que ce soit d'un CAB) : `w2kcolor.inf`, `reshack.exe`,
`_ex.txt`, `_md.txt`, `_sh.txt`. Copiez ces 5 fichiers tels quels dans
`extras\w2kcolor\`. Les icônes/bitmaps référencés par les scripts
ResHack dans la version 366 (`EX100.ICO`, `SH18.ICO`, `WIN2000.BMP`,
etc.) ne sont pas présents séparément à la racine du SP3.0 B4 FR — ils
sont vraisemblablement encodés directement dans `_EX.TXT`/`_MD.TXT`/
`_SH.TXT` eux-mêmes (le format `-script` de ResHack accepte des
ressources en hexadécimal inline). Si après test en VM le thème
n'applique pas les icônes, c'est le premier endroit à vérifier.

`install.bat` appelle `extras\w2kcolor\w2kcolor.inf,DefaultInstall` à
l'étape `[4/9]`, avant TweakUI et les réglages de performance.

### TweakUI — confirmé : oui

**Provenance : `tweakui.inf`** (SP3.0 B4 FR, confirmé FR — infobulle
*"Changer differents reglages de l'interface utilisateur."*), **pas**
`TWEAKUI366.INF` (confirmé EN — *"Change various user interface
settings."*, étiquette de désinstallation EN *"Tweak UI (Remove
Only)"*). Copiez `tweakui.inf` + `TWEAKUI.CPL`/`TWEAKUI.HLP`/`TWEAKUI.CNT`
(mêmes noms listés dans `[SourceDisksFiles]`) dans `extras\tweakui\`.
`install.bat` l'appelle juste après le thème Windows 2000.

### WinTop

⚠️ **Caduc (2026-10-13)** : WinTop est proposé en O/N à l'étape [6/10]
via `sp30\wintop.inf`. Ancien texte, erroné :
✅ Déjà ajouté manuellement par vos soins en suivant le guide précédent —
rien à faire côté `install.bat` (WinTop est un remplacement de Bureau
alternatif, à activer manuellement par l'utilisateur final s'il le
souhaite, pas à imposer à l'installation).

### Réglages de performance (`tweaks`) — les deux versions combinées

Lecture complète des deux fichiers cette session : elles partagent **la
même clé de désinstallation** (`...\Uninstall\ServicePackTweaks`), donc
l'ordre d'installation détermine quelle étiquette reste visible dans
Ajout/Suppression de programmes.

- **`tweaks.inf`** (SP3.0, FR) : `Max Cached Icons=2048` +
  `ConservativeSwapfileUsage=1` + `DMABufferSize=64` **+
  `LocalLoadHigh=1`** (absent du 3.66) + étiquette FR *"Réglages du
  Service Pack non-officiel (Supprimer uniquement)"*.
- **`TWEAKS366.INF`** (3.66, EN) : mêmes réglages `system.ini` (sans
  `LocalLoadHigh`) + `Max Cached Icons=2048`, **plus** l'enregistrement
  des gestionnaires de menu contextuel **Copier vers / Déplacer vers /
  Envoyer vers** (classes `*`, Directory, Drive, Folder,
  AllFilesystemObjects, AllFilesystemEditObjects) + `msdos.sys
  systemreg=0` — absents de la version 3.0. Étiquette EN *"Service Pack
  3 Tweaks"*.

`install.bat` installe **`TWEAKS366.INF` d'abord** (pour récupérer les
menus Copier/Déplacer/Envoyer vers), **puis `tweaks.inf` par-dessus** :
comme les deux écrivent la même clé `DisplayName`, l'étiquette finale
visible sera bien la FR, et `LocalLoadHigh=1` sera présent. Les valeurs
`system.ini` communes aux deux sont simplement réécrites deux fois, sans
effet néfaste.

### Pour mémoire : les `[RunPost]` d'`infex30.ini` (question posée cette session)

```
[RunPost]
0=crlupd.cab,0,0,0
1=verinst.exe q240308,SHDOCVW.DLL,5.0.2723.2900,0
2=wbem15up.inf,WBEMPROX.DLL,1.50.1085,0
3=runpost.bat,0,0,0
```

Ce sont des actions de fin d'installation que le programme `InfEx.exe`
original (le petit installeur à cases à cocher de SP3.0) déclenche après
avoir traité les composants cochés, indépendamment du menu — on ne les
reproduit pas via `InfEx.exe` puisqu'on pilote tout nous-mêmes dans
`install.bat`, mais voici ce que chacun fait :

- **0 — `crlupd.cab`** : met à jour la liste de révocation de
  certificats (CRL) utilisée par Internet Explorer. Sans objet ici : la
  chaîne IE6 SP1 + Q931768 FR qu'on installe déjà gère ses propres
  certificats/CRL.
- **1 — `verinst.exe q240308,SHDOCVW.DLL,5.0.2723.2900,0`** : vérifie la
  version de `SHDOCVW.DLL` sur le système, et si elle est antérieure à
  5.0.2723.2900, relance l'installeur `q240308.exe`. C'est un simple
  garde-fou de version — `q240308.exe` est déjà dans
  `maj2004\updates\` et s'installe inconditionnellement dans notre
  script, donc ce `RunPost` est redondant chez nous.
- **2 — `wbem15up.inf,WBEMPROX.DLL,1.50.1085,0`** : même logique,
  pour WBEM/WMI 1.5 (`WBEMPROX.DLL`) — si la version installée est trop
  ancienne (ou absente), installe WBEM 1.5. **C'est le composant qui
  pourrait simplifier `detect_chipset.vbs`** (actuellement volontairement
  écrit sans dépendance WMI, cf. journal) si on décidait de l'ajouter au
  pack ; non fait pour l'instant, à garder en tête comme piste
  d'amélioration future plutôt que de réécrire le script maintenant.
- **3 — `runpost.bat`** : script de nettoyage interne à SP3.0 (purge des
  fichiers temporaires de l'installeur, marquage de fin
  d'installation dans son propre suivi). Spécifique au mécanisme
  `InfEx.exe`/SP3.0, sans équivalent utile pour notre `install.bat` qui
  gère sa propre logique de reprise par marqueurs.

Aucune action requise de ces 4 lignes pour notre pack : les cas utiles
(0, 1) sont déjà couverts ailleurs, et 2/3 sont soit une piste future
(WBEM) soit un mécanisme propre à `InfEx.exe` qu'on ne réutilise pas.

## `extras\divers\` — nouveau, composants optionnels demandés cette session

Dossier à créer ; tous les composants y sont **optionnels** et demandés
un par un par `install.bat` à l'étape `[5/9]` (aucun n'est installé
automatiquement). Aucune version FR trouvée pour aucun d'entre eux sauf
les Dossiers Compressés.

| Fichier(s) à copier | Provenance | Langue | Notes |
|---|---|---|---|
| `MMC.INF` + binaires associés | `U98SESP3.66` | EN | Console d'administration MMC 1.2, UI technique peu traduisible |
| `REGCLEAN.INF`, `REGCLEAN.EXE`, `REGCLEAN.TXT` | `U98SESP3.66` | EN | Nettoyeur de registre officiel Microsoft — prudence, toujours relire le rapport avant de valider un nettoyage |
| `SHAREDLL.INF`, `SHAREDLL.TXT` | `U98SESP3.66` | EN | Éditeur de compteurs SharedDLLs, mineur |
| `TIMEZONE.INF` + `GMT.INF` | `U98SESP3.66` | EN, invisible | `TIMEZONE.INF` réécrit toute la table des fuseaux (règles DST modernes, ~700 lignes AddReg lues cette session) puis appelle `GMT.INF` via `RunPostSetupCommands=TZU:1` pour réappliquer le fuseau courant — **les deux fichiers sont nécessaires ensemble**, `GMT.INF` doit être copié à côté même s'il n'avait pas été identifié séparément au départ |
| `ZIPFLDR.INF` + **`zipfldr.dll` du SP3.0 B4 FR** (192 784 o, pas la version du 3.66 à 188 688 o) | SP3.0 B4 FR pour le `.dll` (tailles différentes à date quasi identique = chaînes localisées), `U98SESP3.66` pour l'`.inf` | **FR** (dll) | Dossiers Compressés (.zip natif dans l'Explorateur) |
| `TTFEXT.INF`, `TTFEXT.DLL`, `TTFEXT.HLP` | `U98SESP3.66` | EN | Extension TrueType (aperçu/installation rapide de polices) |

**Archiveur (WinRAR/7-Zip)** : non fourni dans aucune des archives du
projet — `install.bat` affiche juste un rappel de l'installer
manuellement. Dites-moi lequel vous préférez si vous voulez que je
l'intègre à l'installation silencieuse plus tard (il faudra l'installeur
exact).

**WSH 5.7 (`SCR579X.INF`) — examiné, non retenu** : c'est une version
plus récente que le WSH 5.6 FR (`js56mfr.exe`) déjà dans
`maj2004\updates\`, mais entièrement EN et avec de nombreuses chaînes
visibles (descriptions de types de fichiers ".VBS", ".JS", etc. dans
l'Explorateur). Contrairement à MMC/SharedDLLs/fuseaux horaires, ce
n'est pas invisible à l'usage — passer à la 5.7 reviendrait à régresser
en anglais une UI aujourd'hui FR pour un gain fonctionnel mineur. **On
garde le WSH 5.6 FR existant.**

## `materiel\directx\` — versions DirectX additionnelles optionnelles — ✅ RÉSOLU cette session (structure réelle confirmée)

DirectX 9.0b reste installé **automatiquement** via `maj2004\` en
Couche 1, comme demandé. Ce dossier ajoute un **menu optionnel**
(étape `[6/9]`, 6 choix) pour empiler par-dessus une autre version si
besoin pour un jeu/logiciel précis.

**Structure réelle constatée dans vos dossiers** (différente de ce qui
avait été supposé au départ — pas de simples `DX80_98.EXE` isolés) :

| Sous-dossier | Contenu réel | Exécutable appelé | Switch | Statut |
|---|---|---|---|---|
| `dx80\` | Redistribuable DX8.0 déjà extrait (CAB + `dxsetup.exe`) | `dxsetup.exe` | `/silent` | ✅ confirmé présent |
| `dx81\` | Redistribuable DX8.1 déjà extrait (CAB + `dxsetup.exe`) | `dxsetup.exe` | `/silent` | ✅ confirmé présent |
| `dx82\` | Redistribuable DX8.2 déjà extrait (CAB + `dxsetup.exe`) — dossier non prévu au départ, ajouté par vous | `dxsetup.exe` | `/silent` | ✅ confirmé présent |
| `dx90c\` | Redistribuable officiel Microsoft déc. 2006, un seul .exe autoextractible | `directx_dec2006_redist.exe` | `/silent` **non vérifié** | ✅ confirmé présent |
| `dx90Cunofficial\` | Build communautaire 2007 (alternative si le précédent échoue), un seul .exe autoextractible | `DX90C2007.EXE` | `/silent` **non vérifié** | ✅ confirmé présent |

`/silent` est le switch standard documenté pour les installeurs
`dxsetup.exe` (confiance haute pour dx80/dx81/dx82). Pour les deux
9.0c (`directx_dec2006_redist.exe` et `DX90C2007.EXE`), `/silent` est
appliqué par défaut mais **non vérifié indépendamment** — si l'un des
deux affiche malgré tout une fenêtre lors du test réel, relancez-le une
fois sans switch et regardez s'il propose `/?` pour trouver son vrai
mode silencieux.

`install.bat` vérifie l'existence de chaque fichier avant de lancer
l'installeur (`if exist`), donc rien ne casse si une version manque.
Installer une version plus récente par-dessus la 9.0b est sans risque ;
en installer une plus ancienne après n'a aucun effet (DirectX refuse de
rétrograder).

## `extras\perso\` — nouveau, point d'extension personnel — ✅ ajouté cette session

Dossier prévu pour que vous puissiez ajouter vous-même, **sans jamais
modifier `install.bat`**, n'importe quel logiciel/installeur futur :
déposez simplement un fichier `extras\perso\perso.bat` qui fait ce que
vous voulez (copier des fichiers, lancer un installeur silencieux,
etc.). `install.bat` l'appelle automatiquement via
`call "..\extras\perso\perso.bat"` juste après l'étape ASPI de
`[4/9]` (Couche 2 Extras), **seulement s'il existe** (`if exist`) — si
le dossier/fichier n'existe pas, cette ligne ne fait rien et ne casse
rien. Vide pour l'instant, à vous de le remplir au fil du temps.

---

## Décision mise à jour : MDAC 2.8 SP1 FR

**✅ RÉSOLU** : source exacte trouvée — `New\mdac28sp1-fr\MDAC_TYP.EXE`.
Comme vous l'avez proposé, la solution la plus simple est de
**remplacer directement** `maj2004\mdac28\MDAC_TYP.EXE` (même nom de
fichier) par cette version SP1 FR — `install.bat` l'appelle désormais
lui-même directement en fin de Couche 1, phase 2 (cf. section `maj2004\`
plus haut), plus besoin de la chaîne `WSEsetup → WSEresume → WSEfinish`.

## Réanalyse SP3.0 Beta 4 FR / U98SESP3.66 / WUPG98 (cette session)

Vous aviez raison de soupçonner des manques — en reprenant les trois
listings en entier, plusieurs éléments existent déjà tout prêts dans vos
archives, juste jamais extraits vers `Win98FR\` :

- **`InstMsiA.exe`** (Windows Installer 2.0) : présent à la racine du
  SP3.0 Beta 4 FR **et** du U98SESP3.66 — maintenant intégré dans
  `extras\dotnet\` (voir ci-dessus)
- **ASPI** (ancienne version, 1999-2002) : présent dans les deux via
  `aspi.inf` + `SUPP.CAB` — superflu, votre `aspi_471a2.exe` séparé
  couvre déjà ce besoin en mieux (voir ci-dessus)
- **`reshack.exe`** (Resource Hacker) : présent à la racine du SP3.0 Beta
  4 FR **et** du U98SESP3.66. Reste un outil de travail pour vous
  (traduction de ressources), pas un composant à installer dans Windows
  — si vous en voulez une copie sous la main, elle est déjà disponible
  sans téléchargement supplémentaire à ces deux emplacements
- **`WINTOP.EXE`/`WINTOP.VXD`** : présent dans `SUPP.CAB` du SP3.0 Beta 4
  FR (+ `WINTOP.INF` dans le U98SESP3.66 pour une installation propre par
  INF). Correspond à l'item "WinTop" du menu optionnel de `W9XSetup.ini`
  — vous pouvez l'ajouter à `extras\additi1\` si vous le voulez, non
  scripté pour l'instant faute de demande explicite de votre part
- **Microsoft Paint Graphic Filters** : absent de SP3.0B4FR et 3.66,
  mais présent dans `WUPG98.EXE\mspaintfilter\` — réglé ci-dessus

## Éléments volontairement exclus (ne pas ajouter)

Pour mémoire (voir le journal complet pour le détail des raisons) :
`OUTLOOK.CAB` du 3.66/3.63 (2009-2010, EN — OE non utilisé par
l'utilisateur, priorité FR), `dma_on.inf`, `upnp.inf` (activation du
service, pas les DLL), `WIN98_54.CAB`, `agtx040C.exe` (ancien pack MS
Agent 2000, incompatible), `VCACHE.VXD` de Xeno86 (redondant avec
`MaxFileCache` déjà en place côté Couche 1, puis retiré par PATCHMEM en
toute fin), **`Y2K_1.exe` / `Y2K_2.exe`** (Windows 98 SE déjà Y2K
compliant nativement, cf. ci-dessus), **`Service Pack (Vanilla).exe`**
(wucsp — absent de `WSEresume.inf`, confirmé non nécessaire, cf.
ci-dessus), et **`extras\word97\`/`extras\office2000\`** (ISO avec
clé de CD manquante, abandonné cette session).

## Prochaine étape suggérée

Une fois les dossiers remplis selon ce manifeste, tester dans une VM
(snapshot avant chaque couche) en suivant l'ordre : Couche 1 (2 phases,
2 redémarrages, reprise automatique d'`install.bat` à chaque fois) →
Couche 2 système → Couche 2 IE/OE → Extras
(avec filtres Paint, ASPI, MS Agent optionnel) → .NET (optionnel) →
pilotes chipset (optionnel) → pilotes ESS/Phil + RLoew en tout dernier.

Points encore ouverts (mis à jour 2026-10-13) :
- ~~`Pls98Thm.inf`~~ : résolu autrement (installeur Plus! 98 + `MSBATCH.INF`,
  cf. révision ⭐) — reste à saisir votre clé dans `MSBATCH.INF`.
- ~~Audit `infex.ini`~~ : fait. SP3.0 = 15 composants (le n° 0
  `spupdate.inf` est maintenant installé en [2/10]) ; 3.66 = 42 composants,
  ceux retenus sont dans `extras\divers\`.
- ~~`aspi_471a2.exe`~~ : extrait, `ASPIINST.EXE` lancé directement.
- Liste des points à valider au premier test : voir `CONTEXTE_IA.md` §5.

**2026-10-14 — Windows Script 5.7 (`05_EXTRA\wsh57`)** : JScript 5.7.0.16535,
VBScript 5.7.0.5730, WSH 5.7 pris dans `U98SESP3.66\SUPP` (tous les imports existent
sous 98). Ces moteurs n'existent qu'en anglais : ceux du SP3.0 FR (5.6) et de XP SP3 FR
le sont aussi, donc aucune perte de FR. La 5.7.0.16599 de XP SP3 est refusée
(`GetUserDefaultUILanguage` absent de 98). `WSH57.INF` remplace le `SCR579X.INF` de la
3.66 : pas de `WSCRIPT -REGSERVER` ni de clés HKCR (menus FR du `scr56.inf` gardés),
pas d'aide anglaise, pas de `DYNWRAPX.DLL`. **Lancé à l'étape [6/11], juste après
`SCR56.INF`** (même question O/N) : testé sur la GX240, la 5.6 installée après la 5.7
provoquait 8 « conflits de versions » (cscript, dispex, jscript, scrobj, vbscript,
wscript, wshext, wshom) et écrasait la 5.7 si l'on répondait Non.

- 2026-10-25 : « Raccourci de jeu » renommé « Raccourci de jeu (affichage et carte son) » (QRES.INF) + raccourci sur le Bureau (10_APPLI\qres\LIENBUR.VBS, lancé après QRES.INF). LISEZMOI : exemple Messiah (DDHELP avec l'ESS, OK sur la SoundMAX).
