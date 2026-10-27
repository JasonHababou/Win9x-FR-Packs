# QuickInstall (pack Win98FR) : fichiers pour la VM de reference et la capture.
#  - reference\SOURCE.REG : source des CAB = C:\WIN98 (Windows installe depuis le CD,
#    CAB copies avant sur le disque ; QuickInstall exige les CAB sur le disque dur)
#  - reference\oeminfo.ini : informations OEM (page Systeme) en francais
# Usage : make_reference_files.py <dossier _construction_qi>
import sys
from pathlib import Path

base = Path(sys.argv[1]) / "reference"
base.mkdir(exist_ok=True)
reg = [
    "REGEDIT4", "",
    "; VM de reference QuickInstall (pack Win98FR) : les CAB de Windows sont dans C:\\WIN98",
    "; (copies avant l'installation) -> source des pilotes du futur PC = disque dur",
    "[HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Setup]",
    '"SourcePath"="C:\\\\WIN98\\\\"', "",
    "[HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion]",
    '"SourcePath"="C:\\\\WIN98\\\\"', ""]
(base / "SOURCE.REG").write_bytes("\r\n".join(reg).encode("cp1252"))
ini = [
    "[general]", "Manufacturer=Windows 98 SE FR - pack Win98FR",
    "Model=Installation rapide QuickInstall (E.Voirin, oerg866)",
    "[Support Information]",
    "Line1=Pack Win98FR : Windows 98 SE francais a jour (SP3.0, couche 3.66, pilotes, logiciels)",
    "Line2=Installation rapide : Windows 9x QuickInstall, http://github.com/oerg866/win98-quickinstall",
    "Line3=Mises a jour supplementaires : CD Win98FR_Plus (pack 2)", ""]
(base / "oeminfo.ini").write_bytes("\r\n".join(ini).encode("cp1252"))
# Windows ME : a copier dans framework\_OEMINFO_ le temps de la capture ME
ini_me = [
    "[general]", "Manufacturer=Windows Millennium FR - pack WinMeFR",
    "Model=Installation rapide QuickInstall (E.Voirin, oerg866)",
    "[Support Information]",
    "Line1=Windows Me FR a jour (Me SP 2.02 Beta 9 FR, IE6 SP1, WMP9, KernelEx, mode MS-DOS FR)",
    "Line2=Installation rapide : Windows 9x QuickInstall, http://github.com/oerg866/win98-quickinstall",
    "Line3=Mises a jour supplementaires : CD Win98FR_Plus (pack 2)", ""]
(base / "oeminfo_me.ini").write_bytes("\r\n".join(ini_me).encode("cp1252"))
print("ok")
