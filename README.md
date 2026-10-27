# Win9x-FR-Packs

Packs correctifs **non officiels** pour **Windows 98 SE français** et **Windows Me français**, plus un pack de logiciels et de jeux commun aux deux.

*English summary: unofficial update packs for French Windows 98 SE and Windows Me (updates, unofficial service packs, IE6 SP1, WMP9, drivers, utilities), plus a shared software/games pack. This repository contains only the install scripts and build tools; the ready-to-burn CD images are on archive.org.*

> Ce dépôt ne contient **que les sources** : scripts d'installation, INF, VBS, sources NSIS, scripts de construction et documentation. Les fichiers de Microsoft et des autres éditeurs ne sont pas ici.
>
> **Les images CD prêtes à graver sont sur archive.org** : <!-- LIENS ARCHIVE.ORG A AJOUTER APRES PUBLICATION -->
> - Correctif Windows 98 SE FR : `Win98FR_Correctif_v3.iso`
> - Correctif Windows Me FR : `WinMeFR_Correctif_v1.iso`
> - Pack 2 (logiciels, jeux, outils) pour 98 et Me : `Win9x_FR_Plus_v1.iso`

## Pour qui ?

Pour un Windows 98 SE ou Me **en français** fraîchement installé depuis le CD d'origine, sur un vrai PC d'époque ou une machine virtuelle. Le pack ne fonctionne pas sur une version anglaise ou une autre langue.

## Installation

1. Installez Windows depuis votre CD d'origine, avec votre propre clé de produit.
2. Insérez le CD correctif : le menu s'ouvre tout seul. Sinon, lancez `AUTORUN.EXE` ou `INSTALL.BAT`.
3. Laissez le CD dans le lecteur jusqu'à la fin : Windows redémarre plusieurs fois et l'installation reprend toute seule. Le journal est dans `C:\W98FR\JOURNAL.TXT` (98) ou `C:\WMEFR\JOURNAL.TXT` (Me).
4. Installez les pilotes de la carte graphique et de la carte son.
5. Insérez le CD du pack 2 pour DirectX, les logiciels, les jeux et les outils de test.

Plus! 98 (pack 98) demande **votre** clé de produit Plus! 98 pendant l'installation.

## Contenu

### Correctif Windows 98 SE FR (`win98/`)

11 étapes, avec un dossier par étape :

| Étape | Contenu |
|---|---|
| 1 | IE6 SP1 FR, Windows Media Player 9 FR, correctifs, MDAC 2.8 SP1 |
| 2 | Service Pack non officiel SP3.0 FR |
| 3 | Shell32 et GDI à jour, fichiers 3.63, certificats racine |
| 4 | Correctifs Internet Explorer et Outlook Express |
| 5 | KernelEx 4.5, lecteur NTFS, Plus! 98 (avec votre clé), Pinball, réglages |
| 6 | Composants optionnels (fuseaux horaires FR, dossiers compressés, TrueType) |
| 8 | .NET Framework 1.1 SP1 FR |
| 9 | Pilotes chipset Intel, VIA, SiS, nVidia (détection automatique) |
| 10 | VC++ 2005/2008, QRes, 7-Zip, DAEMON Tools, RetroZilla, Tarot, Fraps, SIV |
| 11 | Couche U98SESP3.66 filtrée FR, PATCHMEM (plus de 512 Mo), DMA au choix, correctif d'arrêt NVIDIA |

Le clavier DOS (`KEYB`) n'est plus chargé au démarrage de Windows : avec un clavier USB, il faisait figer certains jeux Windows. Il est chargé en mode MS-DOS et dans la fenêtre « Commandes MS-DOS ».

### Correctif Windows Me FR (`winme/`)

8 étapes : IE6 SP1 et WMP9 FR, correctifs, MDAC 2.8, Me SP 2.02 FR (non officiel), certificats, KernelEx, USB 2.0, NTFS, .NET 1.1, pilotes chipset, applications, PATCHMEM et **vrai mode MS-DOS** comme sous Windows 98.

### Pack 2 (`pack2/`)

Installeur à cases à cocher (`INSTALLER_PLUS.EXE`, source NSIS dans `construction/_construction_pack2`) : DirectX 8.1, 8.2 ou 9.0c, Firefox 31.8 ESR FR, VLC, Winamp, WinRAR, ImgBurn, OpenOffice.org 2.4, jeux, 3DMark, outils système.

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `win98/pack`, `winme/pack`, `pack2/pack` | Fichiers texte du projet, aux mêmes emplacements que sur le CD |
| `BINAIRES_*.csv` | Liste de tous les autres fichiers de chaque CD (chemin, taille, SHA-1), pour vérifier ou reconstituer un CD |
| `construction/` | Scripts Python de construction (ISO, packs, couche 3.66 FR, QuickInstall), sources NSIS, scripts de test QEMU |

Les fichiers texte des packs sont en **cp1252 avec fins de ligne CRLF**, et les batch suivent les règles de `COMMAND.COM` (DOS 7). Gardez cet encodage si vous les modifiez.

## Remerciements

Ce projet assemble le travail de nombreuses personnes :
- les auteurs des Service Packs non officiels : SP3.0 FR pour 98, U98SESP 3.6x, Me SP 2.02 FR ;
- **KernelEx** (Xeno86 et contributeurs) ;
- **patcher9x** (JHRobotics) ;
- **Rudolph R. Loew** (PATCHMEM) ;
- **SweetLow** (lecteur NTFS UFSD corrigé, USB 2.0) ;
- **oerg866** (QuickInstall) ;
- **RetroZilla**, **7-Zip**, **QRes** et les autres logiciels inclus.

Les fichiers de Microsoft et des autres éditeurs restent leur propriété.

## Avertissement

Projet non officiel, sans lien avec Microsoft. Windows, Internet Explorer et Plus! sont des marques de Microsoft. Utilisez vos propres licences. Sauvegardez vos données avant d'installer : vous utilisez ces packs à vos risques.

## Licence

Les scripts et la documentation écrits pour ce projet sont sous licence **MIT** (voir `LICENSE`). Cette licence ne s'applique pas aux fichiers de tiers distribués sur les images CD.
