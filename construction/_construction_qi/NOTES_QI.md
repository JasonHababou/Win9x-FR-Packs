# QuickInstall Windows 98 SE FR (pack Win98FR) : comment l'ISO est construite

Première ISO : `ISO\Windows98\Win98SE_FR_QI_test1.iso` (942 Mo, 21 octobre 2026).

## 1. VM de référence

- Installée depuis l'ISO **test14** dans QEMU (`_vm_qemu\chaine_qi.sh`), après avoir copié `CD\WIN98` dans `C:\WIN98`. QuickInstall exige les CAB sur le disque dur.
- Pack complet, puis import de `reference\SOURCE.REG` : SourcePath = `C:\WIN98\`.
- Arrêt propre de Windows (« Postngen ne répond pas » : terminer la tâche, voir plus bas).
- Image gardée : `_vm_qemu\win98_ref_qi_test14.img`.

## 2. Capture (sysprep.py), trois contournements

1. **Chemin sans espace.** `sysprep.py` passe ses chemins à un émulateur DOS. On le lance donc depuis la jonction `C:\QIFW`, qui pointe vers `framework`.
2. **`FATTOOLS_VFSENC=cp850`.** Les noms courts DOS d'un Windows français sont en cp850, par exemple « É » = 0x90. FATtools les lisait en cp1252 et s'arrêtait.
3. **`QI_REGEDIT_PRECALC`.** `registry\msdos.exe`, l'émulateur DOS de QuickInstall, plante sur ce PC (0xC0000417). On fait donc tourner le vrai REGEDIT DOS dans une petite VM DOS :
   - disquette de démarrage 98 de l'ISO ;
   - disque FAT16 contenant `SYSTEM.DAT`, `SLOW.REG`, `FAST.REG` et `JOB.BAT` ;
   - le script produit `S1.DAT` et `S2.DAT`.

   `sysprep.py` (fonction `run_regedit`, modifiée) reprend ces deux fichiers après avoir vérifié que la source et les .REG sont identiques.

Commande :

```
cd /c/QIFW
QI_REGEDIT_PRECALC=<dossier regjob> FATTOOLS_VFSENC=cp850 venv_qi/Scripts/python.exe sysprep.py \
  --osroot "<win98_ref_qi_test14.img>" "Windows 98 SE FR (pack Win98FR)" --iso "<ISO de sortie>"
```

## 3. Test (VM neuve, `_vm_qemu\phase_qi.sh` et `qi_relance.sh`)

- Au démarrage du CD, appuyer sur **Entrée** à « ENTER to start QuickInstall ». Sinon le CD rend la main au disque.
- Menu `[DISK]` : partitionner (cfdisk, type `c` W95 FAT32 LBA, amorçable, Write), puis `[INSTALL]`.
- **Copie en moins d'une minute.** Ensuite, détection du matériel par Windows et redémarrage.
- Bureau complet du pack environ 5 minutes plus tard, sous émulation Pentium III lente : thème, Fraps, DAEMON Tools, RetroZilla, etc.

## QuickInstall Windows ME FR

Première ISO qui s'installe : `ISO\WindowsMe\WinMe_FR_QI_test3.iso`, 820 Mo.

### VM de référence (`_vm_qemu\me_ref.img`, copie `me_ref_qi.img`)

1. Disque formaté depuis la disquette ME (`me_ref_floppy.img` = disquette EN + `MSBATCH.INF`).
2. Le CD ME OEM n'a pas de `setup.exe` : on lance `E:\win9x\install A:\MSBATCH.INF`. MSBATCH est bien pris en compte (clé, composants, Paris).
3. Il reste à saisir le nom d'utilisateur (« Utilisateur ») et à accepter le contrat.
4. QEMU ne fournit pas de BIOS Plug-and-Play à ME : il faut ajouter « Bus PCI » à la main, puis redémarrer pour avoir le lecteur CD.
5. `xcopy D:\WIN9X C:\WIN9X /e /i`, puis le kit `_vm_qemu\me_ref_kit.iso` (`_construction_me\make_me_ref.py`), trois étapes avec redémarrage :
   - `ETAPE1.BAT` : IE6 SP1 FR et WMP9 FR ;
   - `ETAPE2.BAT` : correctifs, MDAC 2.8 SP1, Me SP 2.02 Beta 9 FR (sans ROOTSUPD/CRLUPD). Deux conflits de versions WMP9 (dxmasf.dll, npwmsdrm.dll) : répondre Oui pour garder le fichier plus récent ;
   - `ETAPE3.BAT` : certificats 2020, KernelEx, VC++ 2005/2008, QRes, 7-Zip, RetroZilla (navigateur par défaut), SIV, SourcePath `C:\WIN9X\`, puis mode MS-DOS FR (dosmode_fr ; sa question de redémarrage est en anglais, à cause de l'ADVPACK de TPC).

### Capture

Même méthode que pour 98, avec en plus :
- `reference\oeminfo_me.ini`, copié dans `framework\_OEMINFO_` le temps de la capture ;
- `QI_EXCLURE_ARBRES=_restore` : **obligatoire**. Avec le dossier `_RESTORE` de la Restauration du système, l'installeur s'arrêtait sur « identicalFileCount <= MERCYPAK_V2_MAX_IDENTICAL_FILES » (tests 1 et 2) ;
- `QI_EXCLURE=*$*` : retire `$WinMgmt.CFG` (WMI, recréé par Windows) et `$PluginPing.dll` (Shockwave). Ce n'était pas la cause du plantage, mais ces fichiers sont inutiles.

## Points à revoir

- **.NET 1.1** : la valeur RunOnce `NetFxUpdate_v1.1.4322` (précompilation « Postngen ») reste en attente et bloque l'arrêt de Windows (« Postngen ne répond pas »). Elle se relancera sur chaque PC installé. C'est à corriger dans le pack : laisser NetFxUpdate finir, ou retirer la valeur RunOnce.
- DAEMON Tools démarre avec `-lang 1033`, donc en anglais.
- Les options QuickInstall CREGFIX, NTFS et LBA64 sont laissées sur NON par défaut. À choisir selon le PC.

## DVD QuickInstall 98 (27 octobre 2026)

ISO : `ISO\Windows98\Win98SE_FR_QI_DVD_test1.iso` (3,0 Go), validée dans une VM neuve : copie avec l'option « Copy extras folder » en moins de 2 minutes, puis bureau complet du pack, `C:\extras` présent.

- VM de référence : ISO **test15** + pack complet (`_vm_qemu\win98_ref_qi_test15.img`). Les CAB sont déjà dans `C:\WINDOWS\OPTIONS\CABS` (CABS.VBS du pack), donc plus de `C:\WIN98` ni de SOURCE.REG. `KEYB.COM` remplacé hors ligne par celui de ME (clavier USB, voir le manifeste du pack).
- Extras : `--extra` vers un dossier de jonctions (Pack 2, Pilotes, Office 2000 SR1 + SP3 + clé).
- Pilotes ajoutés dans `_DRIVER_` : NVIDIA 77.72, ESS ES1988 Dell, SoundMAX AD1885 Dell, chipset Intel 6.3 (ich2\win98se). Corrections pour la capture (originaux dans `_a_supprimer\qi98_pilotes_2026-10-27`) :
  - NVAML.INF : 26 fichiers absents retirés de [SourceDisksFiles] (seulement effacés par DelFiles) ;
  - Intel : `845.cat` manquant, repris de ich2-m\win98se (même 845.inf) ;
  - ESS A1.INF : partie modem ES1989 en commentaire (es56cvmp.vxd absent du paquet Dell).
- `makeiso.py` : **Rock Ridge** (le CD Office 2000 dépasse les 8 niveaux ISO9660), fichiers en mode r-xr-xr-x (sinon Linux ne lance plus `lunmercy`), et `add_file` au lieu de tout charger en mémoire.

## Doublons de périphériques et écrans bleus sur le GX240 (29 octobre 2026)

Retour du DVD QI Me test1 sur le Dell GX240 : périphériques système en double avec un point d'exclamation (Bus PCI, DMA, PIC, horloges, coprocesseur, haut-parleur, port souris PS/2, 8 « IRQ Holder ACPI »), puis 3 écrans bleus NDIS/TCPIP pendant le pack 2.

- Cause : les références sont installées dans QEMU, sans BIOS Plug-and-Play. Setup y détecte ces périphériques à l'ancienne (`Enum\Root\*PNP0000`, `*PNP0100`, `*PNP0200`…), et sous Me on ajoute le Bus PCI à la main (`Enum\Root\System\0000`). QuickInstall, avec l'option par défaut « Skip legacy non-PnP hardware detection », applique `fastpnp.reg`, qui garde `Enum\Root`. Sur le vrai PC, l'ACPI (ou le BIOS PnP) détecte tout une seconde fois, y compris un second bus PCI.
- Correction : `framework\registry\fastpnp.reg` supprime aussi `Enum\Root\` `*PNP0000`, `*PNP0100`, `*PNP0200`, `*PNP0400`, `*PNP0500`, `*PNP0600`, `*PNP0700`, `*PNP0800`, `*PNP0B00`, `*PNP0C04`, `*PNP0F0E`, `*PNPB003`, `*PNPB02F` et `System` (original : `fastpnp.reg.orig`). Le clavier `*PNP0303` est gardé : l'ACPI du GX240 n'en déclare pas.
- Les jobs REGEDIT ont été refaits (dossiers `regjob_*_v2`). DVD reconstruits : 98 test4, Me test2, et les deux versions publiques.
- Dans QEMU, Me n'a plus de bus PCI après l'installation (« carte graphique pas configurée », 16 couleurs). C'est attendu : sur un vrai PC, le bus PCI vient de l'ACPI ou du BIOS PnP.
- Contournement sans nouveau DVD : mettre l'option « Skip legacy non-PnP hardware detection » sur **NO** (`slowpnp.reg` vide tout `Enum`).


## Retours Windows Me sur le GX240 (30 octobre 2026)

- **MFC42.DLL** : Me SP 2.02 installe la 6.6.8063, qui importe `DelayLoadFailureHook`, absent de KERNEL32 sous Me : aucun programme MFC ne démarre sans KernelEx. Le pack recopie la 6.2.4131 (SP 3.0 de 98) au début de l'étape 3. Corrigé dans le pack et les images de référence, validé dans une VM et sur le GX240. SFP ne la remplace pas.
- **UPnP** : Explorer plante dans UPNPUI.DLL dès qu'il y a des appareils UPnP sur le réseau. `FINRUN.INF` retire `UPnPMonitor` et `SSDPSRV` (pack) ; REGEDIT DOS fait de même dans les images QI (`"valeur"=-`).
- **Installation « Bad file descriptor »** : `lunmercy` lit par blocs de 1 Mio et échoue si l'en-tête d'un groupe de fichiers de `FULL.866` chevauche une limite de bloc. Sur 6 paquets comparés, les 2 en échec avaient un tel en-tête, les 4 valides aucun. Le hasard de la disposition suffisait à casser un DVD : l'ancien MFC42 passait, le nouveau non. `mercypak.py` réordonne désormais les groupes (`v2_order`). Toujours tester l'installation après une capture.
