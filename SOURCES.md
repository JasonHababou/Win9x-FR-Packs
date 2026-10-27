# Sources et crédits

Liste de tout ce que les packs et les images utilisent, avec l'auteur ou l'éditeur, le site d'origine et la licence. Elle a été établie le 28/10/2026 à partir des fichiers eux-mêmes (Lisez-moi, licences, versions). **« à confirmer »** signale une information que je n'ai pas pu vérifier : corrections bienvenues (issue ou pull request).

Tous ces fichiers restent la propriété de leurs auteurs. La licence MIT du dépôt ne couvre que les scripts et la documentation du projet. La liste fichier par fichier, avec les empreintes SHA-1, est dans `BINAIRES_*.csv`.

## Service Packs non officiels

| Composant | Version | Auteur | Où | Remarque |
|---|---|---|---|---|
| Service Pack non officiel Windows 98 SE, version FR | 3.0 B4 FR | à confirmer | 98 : `02_SP30` | compilation de mises à jour Microsoft. Origine : http://win9x4ever.online.fr/ (pages de téléchargement hors ligne) |
| Couche U98SESP (Unofficial Windows 98 SE Service Pack) | 3.63 et 3.66 (filtrée FR par ce projet) | à confirmer | 98 : `03_SYST/copie363`, `03_SYST/sp366fr` | fichiers anglais écartés, détail dans `RAPPORT_366FR.TXT`. Sources : https://www.htasoft.com/u98sesp/ et https://techtalk.cc/viewtopic.php?t=65 |
| Windows Me Service Pack non officiel FR | 2.02 Beta 9 (2007, fichier `MESP1FR_2.02b9_2007.EXE`) | à confirmer | Me : `02_MESP` | compilation de mises à jour Microsoft. Origine : http://win9x4ever.online.fr/ (comme `MESP202B5V2_FR.EXE`, version b5 ; pages de téléchargement hors ligne) |
| Pack de mises à jour WUPG98 (AfterLife) | - | projet wupg98 | 98 : provenance de Taskbar Shuffle et des filtres de Paint | https://github.com/wupg98/wupg98-AFLl_en |

Sources générales :
- forum MSFN Windows 9x/Me : https://msfn.org/board/forum/8-windows-9xme/ ;
- MDGx : https://www.mdgx.com/ ;
- Phil's Computer Lab : https://www.philscomputerlab.com/ ;
- Win3x.org (mises à jour de sécurité, Plus! 98, Pack98ME) : http://www.win3x.org/ ;
- Win9x4ever : http://win9x4ever.online.fr/ (Service Packs FR, pages de téléchargement hors ligne).

## Logiciels libres ou gratuits de la communauté

| Composant | Version | Auteur | Site | Licence |
|---|---|---|---|---|
| KernelEx (traduction FR) | 4.5.2019.24 FR | Xeno86 et contributeurs ; mise à jour 2019 : jumper (MSFN) ; FR : ce projet | https://sourceforge.net/projects/kernelex/ ; FR : https://github.com/JasonHababou/KernelEx-4.5.2-FR | GPL v2 |
| patcher9x | 0.9.91 | JHRobotics | https://github.com/JHRobotics/patcher9x | GPL v2 (fichier `LICENCE.TXT` fourni) |
| PATCHMEM | à confirmer | Rudolph R. Loew | rloew.net (archivé) | à confirmer |
| Lecteur NTFS Paragon UFSD corrigé + PNTFSHLP | à confirmer | Paragon Software ; corrections : SweetLow | MSFN | pilote propriétaire de Paragon, corrigé |
| Pilotes USB 2.0 pour Me (USBPORT, USBEHCI…) | à confirmer | Microsoft ; adaptation : SweetLow | MSFN | Microsoft |
| QuickInstall (DVD QuickInstall) | 1.1.0 | E. Voirin (oerg866) | https://github.com/oerg866/win98-quickinstall | voir le dépôt d'origine |
| RetroZilla | 2.3 | rn10950 et contributeurs | https://github.com/rn10950/RetroZilla | MPL / GPL / LGPL |
| 7-Zip | 9.20 | Igor Pavlov | https://www.7-zip.org/ | GNU LGPL |
| QRes | 1.0.9.5 | Berend Engelbrecht | SourceForge (qres) | BSD |
| MODEAFF (Raccourci de jeu) | - | ce projet (source NSIS dans `construction`) | - | MIT |
| CuteMouse (`CTMOUSE.EXE`, mode MS-DOS de Me) | 2.1 beta 4 | projet CuteMouse (distribution FreeDOS) | https://www.freedos.org/ | GPL |
| UIDE (`UIDE.SYS`, CD-ROM sous DOS, Me) | 2020-07-07 | Jack R. Ellis (distribution FreeDOS) | https://www.freedos.org/ | à confirmer |
| GSAR (`GSAR.EXE`) | à confirmer | à confirmer | à confirmer | GPL |
| Mode MS-DOS pour Me (`DOSMODE.INF`, IO.SYS modifié, `WINOA386.MO_`) | à confirmer | soporific (Pack98ME, base « TPC ») | http://www.win3x.org/ | à confirmer |
| Resource Hacker (thème Windows 2000) | à confirmer | Angus Johnson | https://www.angusj.com/resourcehacker/ | freeware |
| NirCmd (Service Pack Me) | à confirmer | NirSoft | https://www.nirsoft.net/ | freeware |

## Gratuiciels et logiciels propriétaires

| Composant | Version | Éditeur | Où |
|---|---|---|---|
| DAEMON Tools | 3.47 | Disc Soft / DT Soft | 98 et Me : `10_APPLI/daemon` |
| Fraps | 1.9D | Beepa | `10_APPLI/fraps` |
| SIV (System Information Viewer) | 5.88 | Ray Hinchliffe (rh-software.com), gratuit pour un usage personnel | `10_APPLI/siv` |
| Jeu de Tarot | version CD Sybex (source : https://www.abandonware-france.org/ltf_abandon/ltf_jeu.php?id=3829) | Laurent Pellenc ; une nouvelle version, sans les voix, est sur son site : http://www.pellencsoftware.com/ | `10_APPLI/tarot` |
| Taskbar Shuffle | 2.5 | à confirmer (provenance : pack WUPG98) | `05_EXTRA/taskbarshuffle` |
| ASPI | 4.71.2 | Adaptec | `05_EXTRA/aspi` |
| Filtres graphiques Paint | à confirmer | Microsoft (filtres d'Office) ; provenance : pack WUPG98 | `05_EXTRA/mspaintfilter` |

## Microsoft

Mises à jour et composants officiels de Microsoft, en français quand la version existe :
- Internet Explorer 6 SP1, Windows Media Player 9, MDAC 2.8 SP1 ;
- correctifs q240308, q313829, q330994, q828750, KB819639, KB823353, KB887797, Q931768, Q918547 ;
- Shell32 2007 ; certificats racine et révoqués (rootsupd, rvkroots, 2020) ;
- Windows Script 5.7 ; .NET Framework 1.1 avec SP1 (KB867460) et KB886903 ;
- Visual C++ 2005 et 2008 ; fuseaux horaires, dossiers compressés, extension TrueType ;
- Plus! 98 FR, Pinball 3D, TweakUI 1.33.

Pack 2 et extras QuickInstall : DirectX 8.1, 8.2 et 9.0c ; MS Agent 2.0 FR ; Microsoft Puzzle Collection ; MMC, RegClean, SharedDLLs ; Office 2000 SR1 et SP3 (extras QuickInstall seulement).

## Pilotes chipset et matériel

| Composant | Version | Éditeur | Où |
|---|---|---|---|
| Intel Chipset INF | 3.20.1008 et 6.3.0.1007 ; PIIX (pentiumTo2) | Intel | `09_CHIP/intel` |
| VIA 4in1 | 4.35v ; Hyperion ; vlatency | VIA | `09_CHIP/via` |
| SiS AGP, IDE, 530/5598 | AGP 1.21, IDE 2.04a | SiS | `09_CHIP/sis` |
| Correctif d'arrêt NVIDIA (VXD 81.85 à 82.69) | - | NVIDIA ; correctif : ce projet (`NVFIX.VBS`) | `09_CHIP/nvidia` |
| QuickInstall 98/Me : NVIDIA 77.72, ESS ES1988 (Dell), SoundMAX AD1885 (Dell R45973), Intel Chipset 6.3 | - | NVIDIA, ESS, Analog Devices, Dell, Intel | pilotes intégrés aux DVD |

## Pack 2 : logiciels, jeux et outils

| Composant | Version | Éditeur | Licence |
|---|---|---|---|
| Firefox ESR (FR) | 31.8 | Mozilla | MPL 2.0 |
| VLC (FR) | 3.0.24 | VideoLAN | GPL v2 |
| Winamp | 5.2 Standard et Full (EN), 2.91 + traduction FR | Nullsoft | freeware |
| WinRAR (FR) | 3.93 | RARLAB | shareware (version d'essai) |
| ImgBurn (FR) | 2.5.8.0 | LIGHTNING UK! | freeware |
| AIDA32 | 3.93 | Tamás Miklós | freeware |
| CPU-Z | 1.78 | CPUID | freeware |
| XnView | 1.80 | Pierre-Emmanuel Gougelet | gratuit pour un usage privé |
| Foxit Reader (EN) | 1.3 | Foxit Software | freeware |
| K-Lite Codec Pack | 3.4.5 | Codec Guide | freeware |
| OpenOffice.org (FR) | 2.4.2 | Sun Microsystems / communauté OpenOffice.org | GNU LGPL v3 |
| AbiWord + dictionnaire FR | à confirmer | projet AbiWord | GPL |
| Nvu (FR) | 1.0 | Linspire | MPL / GPL |
| Spread32 | à confirmer | à confirmer | freeware |
| Flash Player (IE et Netscape/Firefox) | 9 | Adobe | propriétaire, gratuit |
| UltimateZip (EN) | 2.7 | à confirmer | freeware |
| FTP Commander (EN) | à confirmer | InternetSoft | freeware |
| Hover!, SkiFree, Échecs | - | Microsoft ; SkiFree : Chris Pirih | - |
| 3DMark 99, 2000, 2001, 03 | - | Futuremark (UL) ; clés publiées par l'éditeur | freeware |

## Outils de construction (non distribués sur les images)

Python, pycdlib, FATtools, pyfatfs, 7-Zip, NSIS 2.46 et QEMU, chacun sous sa propre licence.
