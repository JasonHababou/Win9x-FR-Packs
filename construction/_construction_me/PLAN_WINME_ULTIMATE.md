# Windows ME « ultimate » FR — inventaire et plan

Rédigé le 20 octobre 2026 (nuit), à partir de tes dossiers. Rien n'a été modifié dans `WinMe` ni dans `bkpWin98\SauvegardeWinME`.

## Ce que tu as déjà

| Élément | Où | Rôle |
|---|---|---|
| Windows Millénium OEM FR (ISO, 370 Mo) | `ISO\WindowsMe\Windows Millenium OEM FR.iso` (la copie identique de `WinMe` est partie dans `_a_supprimer` le 2026-10-20) | base d'installation |
| CD ME décompressé (CAB `win9x\`) | `WinMe\WInMEdecompressé\win9x` | base pour une ISO « slipstreamée », comme pour 98 |
| Disquette de démarrage ME | `WinMe\WindowsME.img` | démarrage |
| winMEtiny.iso (158 Mo) | `WinMe\` | ME allégé (à examiner) |
| Me SP 2.02 b5 FR (2006) | `WInMEdecompressé\addon\Me SP v2.02 b5.zip` | Service Pack non officiel, équivalent du SP3.0 de 98 |
| IE6 + KB918899 FR | `addon\IE6_918899 Fr.exe` | navigateur et correctifs |
| KernelEx 4.5 Final FR | `addon\KernelEx v4.5 Final FR.exe` | à remplacer par ta KernelEx 4.5.2019.24 FR du pack 98 |
| ShellMe FR | `addon\ShellMe Fr.exe` | shell32 corrigé |
| TPC-WinMe-DOSMODE 0.9.1 | `WInMEdecompressé\` | rend le vrai mode MS-DOS à ME (iMic, MSFN), installeur INF avec désinstallation |
| Corruption Crucible (Tools-master, 2025) | `WInMEdecompressé\` | outils bas niveau : vmm4gfix, nvme9x, lba64hlp, ramdrv4m, APMDisable… |
| CD de sécurité Microsoft FR (février 2004) | `ISO\Logiciels\Security9_fra_13.iso` | **mises à jour officielles ME en français** : 14 correctifs `…FRNM.EXE` (273727, 273991, 290700, 314757, 323172, 323255, 329048, 329115, 811630, 812709, 823559, 825119), KB828026, Q330994, IE6 SP1, et les INF d'installation automatique `Win9x\WinME\WME*.inf` (même CD que celui utilisé pour 98) |
| Correctifs ME officiels anglais (44) | `Windows\Mises à jour\WinUpdates_95-XP32.iso` | à ne prendre que s'il n'existe pas de version FR (ROOTSUPD, MDAC, KB891711, KB918547…) |
| ME installé (9,4 Go) | `bkpWin98\SauvegardeWinME` | référence : KernelEx, Plus!, DirectX, RetroZilla, 7-Zip, ImgBurn, VLC, DAEMON Tools, jeux |

## Ce qu'on peut reprendre du pack 98 (déjà testé)

Tout ce qui ne dépend pas du noyau 98 se réutilise tel quel :
- **pack 2 entier** : DirectX 8.1 / 8.2 / 9.0c, MS Agent, MMC, logiciels, jeux, 3DMark, CPU-Z ;
- **applications du pack 1** : Visual C++ 2005/2008, 7-Zip, RetroZilla, DAEMON Tools, QRes, Fraps, SIV, WinTop, Tarot ;
- **KernelEx 4.5.2019.24 FR**, .NET 1.1 FR, certificats racine 2020, fuseaux horaires FR 2020 ;
- **PATCHMEM** (RLoew) : prend en charge ME ;
- **patcher9x** : prend en charge ME (VMM32.VXD de ME).

## Ce qui est propre à ME

- **Service Pack** : Me SP 2.02 b5 FR à la place du SP3.0 ; vérifier s'il existe plus récent (mdgx.com).
  Il a la même structure que le SP3.0 de 98 (SPUPDATE.INF, SP2.cab, SUPP.cab, NIRCMD, PRESERVE.INF, WUINFO.INF, Q329414). Il appelle SPUPD-2.INF, puis SPUPD-3.INF, puis RUNPOST.BAT, qui installe des certificats avec ROOTSUPD.EXE. Or, sur 98, c'est cette étape « certificats » qui figeait le SP3.0. À vérifier en priorité, et à remplacer par les certificats de 2020, comme pour 98.
- **Mode MS-DOS** : TPC-WinMe-DOSMODE (facultatif, case à cocher). Utile pour les vieux jeux DOS, mais encore « pre-release » : à tester à fond (hibernation, restauration du système).
- **Restauration du système** (`_RESTORE`) : proposer de la désactiver (gain de place et de vitesse) ou la garder.
- **Pas de couche 3.66** : elle vise 98 SE ; certains fichiers sont communs, à trier comme on l'a fait pour 98.

## Sources conseillées par toi

- mdgx.com, section Windows ME : https://www.mdgx.com/web.htm#WME
- Forum MSFN Windows 9x/ME : https://msfn.org/board/forum/8-windows-9xme/
- win9x4ever (page « Windows ME », site mort) : copie à chercher sur web.archive.org

## Plan proposé (même méthode que l'ISO 98)

1. **Inventaire précis** du Me SP 2.02 b5 (fichiers, versions), comparé aux CAB du CD ME.
2. **Pack ME** (comme Win98FR_v3) : INSTALL.BAT en étapes avec reprise automatique, réutilisant les dossiers du pack 98 qui conviennent.
3. **ISO ME tout-en-un** : clé et composants présélectionnés dans le fichier de réponses, cases du pack dans l'écran des composants, pack lancé au premier démarrage (même mécanique que `_construction_iso`).
4. **Tests** dans QEMU (méthode hybride Hyper-V + émulation) et 86Box, puis sur ton GX240.

## Décisions (20 octobre 2026)

- **Clé ME** : XXXXX-XXXXX-XXXXX-XXXXX-XXXXX (fichier de réponses).
- **Restauration du système** : gardée, sauf si elle pose problème aux tests.
- **Mode MS-DOS** : priorité haute, il doit être aussi bon que celui de 98, voire meilleur. TPC DOSMODE est donc à tester à fond. Si ses défauts le demandent, il faudra une autre solution : IO.SYS et COMMAND.COM patchés, ou MSDOS.SYS avec BootGUI.
- **Mises à jour** : en priorité les correctifs FR du CD `Security9_fra_13.iso`, puis le dossier `WIN9X` du pack 98 pour ce qui est commun.
- **Composants Windows** :

| Composant | Choix |
|---|---|
| Jeux Internet | décoché (serveurs morts, pas de mode hors ligne) |
| Multimédia | tout coché, y compris Shockwave et Shockwave Flash |
| Universal Plug and Play | coché |
| Partage de connexion Internet | décoché (Internet par le réseau local) |
| Porte-documents, MSN Messenger, NetMeeting, Numéroteur téléphonique, VPN, Serveur d'accès distant, Carnet d'adresses, Outlook Express, Services en ligne (AOL) | décochés |
| Tout le reste | coché |

- **Pack 2** : commun aux trois éditions (98 classique, ISO 98, ME), sauf avis contraire.

## Service Pack et correctifs : constat du 20 octobre 2026

- **Ton Me SP** (`MESP202B5V2_FR.EXE`) date de juillet 2006. mdgx propose le **Me SP 2.02 Beta 9 FR** de décembre 2007 (`mdgx.com/spx/MESP1FR.EXE`, 20,8 Mo), copié dans `_construction_me\sources\MESP1FR_2.02b9_2007.EXE`. Il est plus complet : 190 fichiers contre 151 dans SP2.cab, avec KERNEL32 (fichiers de plus de 2 Go), HTML Help 2007, Agent, DirectX Transform et WMP. Il ajoute les correctifs 308567, 828026 et 832353. **C'est lui qu'on prendra.**
- Le « ME SP2 » anglais (6 Mo) a été retiré par son auteur pour bogues : on l'écarte.
- **CD de sécurité FR (2004)** : ses 12 correctifs `…FRNM.EXE` sont tous déjà dans le Me SP, en version égale ou plus récente. Par exemple, HTML Help et itircl y sont en version 2005 et 2007, contre 2003 sur le CD. KB828026 (WMP) est dans la Beta 9. Q330994 concerne Windows Messenger, qu'on décoche. **Le CD n'apporte donc rien de plus**, mais il reste une source FR de secours.
- **Point à corriger** : `RUNPOST.BAT` de la Beta 9 lance encore `ROOTSUPD.EXE /q:a /r:n` (certificats 2007). C'est la même étape que celle qui figeait le SP3.0 sous 98. On la retire et on la remplace par les certificats 2020 du pack 98.
- **Mode MS-DOS (TPC DOSMODE 0.9.1)** : il patche COMMAND.COM et REGENV32.EXE, installe un IO.SYS « réel » (tiré de `TOOLS\NETTOOLS\FAC\CBS.DTA` du CD), WINOA386/PIFMGR de ME DR1, WIN.COM de 98 SE, IO8EMMOK (pour EMM386) et SYS/FORMAT complets. Limites connues :
  - « Utiliser la configuration MS-DOS actuelle » éteint le PC ;
  - la sortie du mode DOS vers Windows n'est que partiellement réglée (via WIN.COM de 98) ;
  - la mise en veille prolongée et la restauration du système ne sont pas testées ;
  - le correctif KB311561 (IO.SYS) n'est pas intégré ;
  - la protection des fichiers système (SFP) bloque `C:\WINDOWS\COMMAND`.

  Le WINBOOT.SY_ fourni a ses messages en anglais. On prendra plutôt l'IO.SYS **FR** de `cbs.dta`, présent sur ton ISO OEM FR. **À tester à fond dans la VM**, et à comparer au mode DOS de 98.
- **Jeux DOS : comment tu t'en sers sous 98** (relevé dans `bkpWin98\Sauvegarde 8`) :
  1. **Dans Windows**. Alone in the Dark : le raccourci du bureau `Indark.pif` lance `C:\WINDOWS\QRESJEUX\INDARK.BAT`, créé par l'outil du pack « Raccourci de jeu » (QRESJEUX.HTA, MODEAFF, choix de la carte son), puis `start /w INDARK.EXE`. Torin DOS se lance par `TORINDOS\TORIN.BAT`. **ME le fait d'origine** : on reprend « Raccourci de jeu » tel quel.
  2. **Vrai mode MS-DOS**. Windows 98 fournit « Mode MS-DOS pour jeux.pif » et « … (EMS) et étendue (XMS).pif » (configuration spécifique, EMM386) et « Sortie de Dos.pif » (configuration actuelle). Sous ME, il faut TPC DOSMODE, avec trois adaptations :
     - **le SHELL32 de ME FR cherche « Sortie de Dos.pif »**, comme 98 FR, et non le « Exit to DOS.pif » fourni par TPC : à renommer ;
     - dans les PIF « Mode MS-DOS pour jeux », remplacer HIMEM.SYS par IO8EMMOK.SYS placé avant EMM386, car l'IO.SYS de ME contient déjà son pilote XMS ;
     - corriger le cas « configuration actuelle », qui éteint le PC.
  3. **Tests prévus dans la VM ME** : Alone in the Dark (`Sauvegarde 8\INFOGRAM\INDARK`) et Torin DOS (`SIERRA\TORINDOS`), copiés sur un CD de test sans toucher aux sauvegardes. Chacun sera lancé dans Windows puis en mode MS-DOS, avec contrôle du retour à Windows.
- **Mode MS-DOS FR : premier test réussi** (VM QEMU, 2026-10-20). Le paquet est `_construction_me\dosmode_fr`, généré par `make_dosmode_fr.py` :
  - **IO.SYS FR** : `winboot.lf` des outils d'usine du CD FR, décompressé par IO8DCOMP de RLoew, message de démarrage adapté ;
  - « **Sortie de Dos.pif** » à la place de « Exit to DOS.pif » ;
  - installeur en français.

  Résultats :
  - « Redémarrer en mode MS-DOS » réapparaît dans Arrêter ;
  - le PC redémarre en vrai DOS (« Windows Millennium démarre votre programme MS-DOS. », 598 Ko de mémoire conventionnelle libre, XMS) ;
  - `exit` relance Windows ME.

  **Version 2 validée sur une ME propre** (VM QEMU, 2026-10-20, 22 h) :
  - **installation sans intervention**. `INSTALL.BAT` FR applique les correctifs COMMAND.COM et REGENV32 de TPC, règle les attributs (sans la fenêtre ATTRIB bloquée de TPC), ajoute KEYB FR à AUTOEXEC.BAT et COUNTRY à CONFIG.SYS (l'INF ne sait pas le faire sous ME), puis lance `DOSMODE.INF` sans START /W, sinon le redémarrage est bloqué ;
  - **fenêtres DOS de Windows en AZERTY**. Sans KEYB dans AUTOEXEC.BAT, elles passaient en QWERTY, car l'IO.SYS « vrai DOS » ne charge plus le clavier FR depuis le registre ;
  - **mode MS-DOS** (« Sortie de Dos.pif » FR) :
    - 586 Ko de mémoire conventionnelle libre, 32 Mo d'EMS et XMS (IO8EMMOK + EMM386 RAM) ;
    - **CD-ROM** avec **UIDE** (Jack R. Ellis, FreeDOS) et MSCDEX, en D: ;
    - **souris** avec **CuteMouse 2.1 FR** (GPL) ;
    - **AZERTY** avec le KEYB.COM FR de la disquette de démarrage ;
    - retour à Windows avec `exit`.
  - **Deux PIF jeux** : « Mode MS-DOS pour jeux (XMS) » (EMM386 NOEMS) et « Mode MS-DOS sans EMM386 ».
  - **OAKCDROM bloque avec EMM386** sous QEMU, quel que soit l'ordre de chargement. C'est pour ça qu'UIDE le remplace.
  - **Torin DOS en vrai DOS** : le jeu trouve son CD et ses ressources. Il bloque ensuite sur le son : son pilote Sierra sonde une Sound Blaster en 220 ou 240, et la SB16 de QEMU, sans sortie audio, ne lui répond pas. C'est propre à QEMU ; la vérification sera à faire sur le GX240 ou dans 86Box.
  - Les noms ISO du CD de test étaient faux pour MSCDEX (`make_jeux_iso.py` changeait `RESMAP.000` en `RESMAP_0`). C'est corrigé.

  Fichiers :
  - `_construction_me\dosmode_fr` : paquet prêt, généré par `make_dosmode_fr.py`, avec les PIF de `make_pif_dos_fr.py` et les outils de `extras_dos\` ;
  - `_construction_me\sources` : Me SP Beta 9 FR, CuteMouse et UIDE.

  Reste à faire :
  - **PIFMGR.DLL** : celui de ME DR1 fourni par TPC donne des messages en anglais. Le remplacer par celui de **98 SE FR**, avec le correctif de version de TPC ;
  - SYS et FORMAT complets : en anglais pour l'instant (DR1 et 98), le SYS de ME FR étant bridé ;
  - **VM QEMU** : ME n'y trouve pas de BIOS Plug-and-Play (code 24), donc ni PCI ni CD. Solution : ajouter « Bus PCI » à la main (Ajout de matériel > Périphériques système). À prévoir pour les tests de l'ISO ME, sans effet sur le GX240.
- **WMEUPD_23.iso** (`WinMe\Addon`, 675 Mo, décembre 2024) : CD communautaire « Windows Me Update » en **anglais**. Ses 50 correctifs `…USAM.EXE` ne s'installent pas sur un ME FR, et le Me SP FR les couvre déjà. On peut en revanche reprendre :
  - **les composants neutres** : VB runtimes 1 à 6, VC++ 6 SP6, MSXML 2.6, 3.0 et 4.0, Jet 4 SP8, GDI+, unicows, WSH 5.6, WinG, pilote haut-parleur PC ;
  - **les patchs** : RLoew (AHCI, HCDP 48 bits LBA, PATCHMEM, PATCH1TB, PTCHCDFS, PTCHSATA, PTCHDSTR), patcher9x, CREGFIX, NOVOLTRK ;
  - **DirectX 8.2 et 9.0c** : déjà dans le pack 2.
- **ISO ME** : `Windows Millenium OEM FR.iso` **n'est pas amorçable** (pas d'image de démarrage). De plus, `WindowsME.img` est la disquette de démarrage **anglaise** (pays 044, messages en anglais). L'ISO tout-en-un aura donc une disquette de démarrage **FR**, avec le menu « installation depuis le CD » comme pour 98. Sa source est l'EBD FR complet trouvé dans `bkpWin98\SauvegardeWinME\WINDOWS\COMMAND\EBD` (1,4 Mo, KEYB et KEYBOARD.SYS FR). Ces fichiers sont seulement copiés, la sauvegarde n'est pas modifiée.
- **Fichier de réponses** : `make_msbatch_me.py` génère le MSBATCH.INF (clé, fuseau Paris, 68 composants, 11 décochés selon tes choix).
- **win9x4ever** : la page « Windows ME » est archivée (2010-2026) et liste 5 rubriques : Service Packs, Correctifs officieux autonomes, Packs IE6, Revolutions Pack, KernelEx. Les sous-pages ne sont pas archivées, ou archive.org était saturé (erreur 429) : à réessayer.

## Pack WinMeFR : premier test complet (26 octobre 2026, nuit)

ME neuf dans QEMU (`_vm_qemu\me_pack.img`), CD `me_pack_test1.iso` (pack à la racine + `WIN9X`), mode T :
les 8 étapes sont passées, le journal `C:\WMEFR\JOURNAL.TXT` est complet, le mode MS-DOS démarre
(CD, souris, clavier AZERTY) et `EXIT` revient à Windows. Après le pack, `C:\WMEFR\JOURNAL.TXT` et le
bureau (Configurateur NTFS, Raccourci de jeu, DAEMON Tools, RetroZilla, Fraps) sont bons.

Corrigé dans `make_pack_me.py` / `pack\` (pack reconstruit, ancien dans `_a_supprimer\packme_2026-10-26`) :
- Me SP : le drapeau 1056 n'empêchait pas la question « Conflit de versions » (langue) sur `dxmasf.dll` :
  les 7 fichiers Windows Media sont maintenant **retirés** des copies du SP (WMP9 est toujours installé à l'étape 1) ;
- `GMT.INF` manquait : `TIMEZONE.INF` l'appelle à la fin et RUNDLL32 restait bloqué **sans fenêtre** ;
- `README.UFSD.TXT` et `README.PNTFSHLP.TXT` (deux points) introuvables sur le CD : renommés `UFSD.TXT`, `PNTFSHLP.TXT` ;
- reprise après redémarrage : `GO.BAT` ne transmettait pas `WMEDRV`/`WMESUB`, donc après le mode MS-DOS
  `FINRUN.INF` était cherché dans `C:\WMEFR\DOS` (erreur, clé Run laissée). `GO.BAT` les définit maintenant.

Connu, pas corrigé :
- IE6 SP1 réinstalle **Outlook Express** (décoché dans MSBATCH) ;
- la question avant le mode MS-DOS est en **anglais** : `WINOA386.MO_` de TPC est un ME bêta 4.90.2332 anglais.
  Celui de 98 SE FR (4.10.2222) a les textes français, mais n'est pas prévu pour ME : pas remplacé.

À refaire avec le pack corrigé : `_vm_qemu\me_pack_test2.iso`. Disque ME + pack terminé gardé : `_vm_qemu\me_pack_fin_test1.img`.

## Pack WinMeFR : 2e test, pack corrigé (26 octobre 2026, soir)

ME neuf (`_vm_qemu\me_pack2.img`, disquette `me_floppy2.img` avec le nouveau `MSBATCH.INF`), CD `me_pack_test2.iso`, mode T.
**Les 4 corrections sont validées** :
- aucune question pendant le Me SP ;
- les fuseaux horaires ne bloquent plus ;
- aucun fichier NTFS introuvable ;
- aucune erreur `FINRUN.INF` après le mode MS-DOS.

Le journal est complet (ST1 à ST8, nettoyage, redémarrage), `GO.BAT` est supprimé et aucune fenêtre MS-DOS ne s'ouvre au démarrage suivant.

- `MSBATCH.INF` : avec `[NameAndOrg]`, le nom « Utilisateur » est déjà rempli. La page « Informations utilisateur » reste affichée (`Express=0`) : une seule touche Entrée suffit.
- Ajouté ensuite à `make_msbatch_me.py`, **pas encore testé** : `[Network]`, pour sauter la page « Identification réseau ».
- Disque **ME neuf + Bus PCI**, avant le pack : `_vm_qemu\me_vierge.img`, pour les prochains tests.

## ISO Windows Me FR classique (26 octobre 2026, soir) : `ISO\WindowsMe\WinMe_FR_v1.iso` (662 Mo, un CD)

Construite par `make_me_iso.py` à partir de :
- l'ISO OEM d'origine (`WIN9X`) ;
- l'EBD FR de ta sauvegarde ME, lu seulement ;
- le pack `WinMeFR` ;
- le `MSBATCH.INF` de `make_msbatch_me.py`.

- **Démarrage du CD** : disquette FR intégrée (El Torito), menu « 1. Installer Windows Millennium Edition depuis le CD-ROM », choisi par défaut. `WMEFRDOS.BAT` vérifie d'abord le disque C:, car l'installation de Me ne partitionne ni ne formate (« Impossible de créer un répertoire temporaire » sur un disque vierge) :
  - pas de partition : FDISK sur demande, puis redémarrage ;
  - partition non formatée : FORMAT C: sur demande (FORMAT redemande confirmation) ;
  - C: prêt : installation directe.
  Rien n'est effacé sans ton accord. Le test se fait par `WMEFRC.BAT` sous `COMMAND /F` : `IF EXIST` répondait « vrai » sur un disque non formaté, d'où un test par copie de fichier.
- **Piège DOS** : pas de signe « supérieur » dans un `REM`. `COMMAND.COM` y voit une redirection et écrit sur A:, protégée en écriture.
- **Fichier de réponses** : clé, Paris, composants, `[NameAndOrg]`, `[Network]`, et `[Install]` qui pose `RunOnce\WMEFR`. À la première ouverture de session, cette valeur cherche `WMEFRCD.BAT` sur les lecteurs D: à R: et lance le pack (menu T/E/R/Q).
- **Testé dans QEMU sur un disque vierge** : menu FR, FDISK, redémarrage, FORMAT, installation. La page « Identification réseau » est sautée et la valeur RunOnce est bien écrite. La commande, lancée à la main avec le CD visible, ouvre le menu du pack. Dans QEMU, ME ne voit pas le CD avant l'ajout de « Bus PCI », d'où ce test à la main ; un vrai PC n'a pas ce problème.
- **Reste à l'écran**, avec les choix déjà faits :
  - « Informations utilisateur » et la clé de produit, préremplies ;
  - le contrat de licence ;
  - les pages Langue, Pays, Clavier et Fuseau horaire, déjà sur la France (`Express=0`).


## ISO v2, CD correctif et QuickInstall DVD (27 octobre 2026, nuit)

- **`ISO\WindowsMe\WinMe_FR_v2.iso` (662 Mo)**, remplace la v1 :
  - **le pack est lancé par la clé `Run`, plus par `RunOnce`.** Avec `RunOnce`, il n'y avait qu'une tentative : si le lecteur CD n'était pas encore prêt à la première ouverture de session, le pack ne partait jamais (c'est ce qu'on voit dans QEMU, où ME ne voit pas le CD sans « Bus PCI »). Maintenant, la recherche du CD est refaite à chaque ouverture de session. Dès qu'il est trouvé, `WMEFRCD.BAT` efface la valeur (`01_BASE\FINRUN.INF`) puis lance le pack, qui pose ensuite sa propre reprise sous le même nom `WMEFR` et l'efface à la fin. Quitter le menu du pack ne le relance donc plus ;
  - le lanceur du CD correctif (`AUTORUN.EXE` / `AUTORUN.INF`) n'est pas copié à la racine, et le `LISEZMOI.TXT` du pack devient `LISEZMOI_PACK.TXT`, comme sur l'ISO 98.
  - Testé de nouveau dans QEMU sur un disque vierge : menu du CD, FDISK, FORMAT, pages de Setup déjà remplies (français, clavier Français, Paris, composants, clé). Restent affichées : « Informations utilisateur » (nom déjà rempli), le contrat de licence (CD OEM) et « Terminer ». Script : `_vm_qemu\test_me_iso.sh`.
- **CD correctif `ISO\WindowsMe\WinMeFR_Correctif_v1.iso` (292 Mo)** : le dossier `WinMeFR` seul, pour un Windows Me installé depuis le CD d'origine. Le pack a maintenant un menu automatique (`AUTORUN.EXE`, variante `PACK=3` de `_construction_autorun\AUTORUN.nsi`) et un `LISEZMOI.TXT` (sources dans `_construction_me\pack`).
- **QuickInstall DVD `ISO\WindowsMe\WinMe_FR_QI_DVD_test1.iso` (3,0 Go)**, validé dans une VM neuve, avec les extras (pack 2, pilotes, Office 2000). Bibliothèque de pilotes `framework\_DRIVER_ME_` (chipset Intel 6.3 en version `ich2\winme`). Il remplace `WinMe_FR_QI_test3.iso`.
- **Pack 2 sous Me : validé** (toutes les cases par défaut). DirectX 9.0c, Firefox 31.8 (KernelEx) et le reste fonctionnent. Winamp 5.2 Full demande un redémarrage au milieu : répondre Non. Dans QEMU, le premier démarrage après le pack 2 est resté bloqué une fois sur les tâches DirectX (`RunOnce` StreamingDeviceSetup), puis le démarrage suivant a été normal.
