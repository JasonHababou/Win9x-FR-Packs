# Surveille la machine virtuelle pendant le pack (redemarrages successifs).
# QEMU (TCG) gere mal les redemarrages A CHAUD de Windows 98 : APIC local laisse
# masque, plus d'interruption d'horloge, boucles d'attente infinies (tests du
# 2026-10-18). Donc QEMU tourne avec -no-reboot : chaque redemarrage de Windows
# ferme QEMU, et ce script le relance A FROID (demarrage sur le disque).
# Toutes les 2 min : capture archive/NNN.png + EIP dans surveiller.log.
# Blocage connu (boucle PIT) 3 fois de suite : QEMU tue puis relance.
# Arret : fichier STOP. Usage : surveiller.py <iso> [memoire Mo]
import re
import subprocess
import sys
import time
from pathlib import Path

ICI = Path(__file__).parent
ISO, MEM = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "1024")
# ISO.TXT (facultatif) : chemin de l'ISO relu a chaque demarrage a froid ("changer de CD")
def iso():
    f = ICI / "ISO.TXT"
    return f.read_text().strip() if f.exists() else ISO

# DISQUE.TXT (facultatif) : image disque a utiliser au lieu de win98.img (test pack 1 sur la Clean install)
def disque():
    f = ICI / "DISQUE.TXT"
    return f.read_text().strip() if f.exists() else "win98.img"


(ICI / "archive").mkdir(exist_ok=True)
WHPX = len(sys.argv) > 3 and sys.argv[3] == "whpx"        # acceleration Hyper-V (QEMU x86_64)
QEMU = r"C:\Program Files\qemu\qemu-system-" + ("x86_64.exe" if WHPX else "i386.exe")
ARGS = ["-machine", "pc,acpi=off,hpet=off", *([] if WHPX else ["-cpu", "pentium3"]), "-m", MEM,
        "-accel", "whpx" if WHPX else "tcg",
        "-drive", "DISQUE",
        "-drive", "CDROM", "-boot", "c",
        "-vga", "cirrus", "-audiodev", "none,id=muet", "-device", "sb16,audiodev=muet", "-nic", "none", "-rtc", "base=localtime",
        "-display", "none", "-no-reboot", "-monitor", "tcp:127.0.0.1:4444,server,nowait"]


def mon(*cmd):
    r = subprocess.run(["python", str(ICI / "pilote.py"), *cmd], capture_output=True, text=True, cwd=ICI)
    return r.stdout


def log(m):
    with open(ICI / "surveiller.log", "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + m + "\n")


qemu, n, bloque, demarrages, dernier, dernier_ecran = None, 0, 0, 0, None, None
log(f"debut ({ISO}, {MEM} Mo)")
# QEMU deja lance par un surveillant precedent : on attend qu'il se ferme
while "qemu-system" in subprocess.run(["tasklist"], capture_output=True, text=True).stdout:
    time.sleep(10)
while not (ICI / "STOP").exists():
    if qemu is None or qemu.poll() is not None:
        demarrages += 1
        log(f"demarrage a froid n{demarrages}")
        args = [a if a != "CDROM" else f"file={iso()},media=cdrom,if=ide,index=2,readonly=on" for a in ARGS]
        args = [a if a != "DISQUE" else f"file={disque()},format=raw,if=ide,index=0" for a in args]
        qemu = subprocess.Popen([QEMU, *args], cwd=ICI, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                creationflags=0x4000)   # priorite basse (ne pas gener le PC hote)
        time.sleep(30)
        continue
    try:
        out = mon("cmd", "info registers")
        eip = int(re.search(r"EIP=([0-9a-f]+)", out).group(1), 16)
        cs = re.search(r"CS =([0-9a-f]+)", out).group(1)
    except Exception as e:
        log(f"moniteur indisponible ({e})")
        time.sleep(30)
        continue
    n += 1
    mon("ecran", f"archive/{n:03d}.png")
    try:                                                 # ecran noir = redemarrage fige
        from PIL import Image, ImageStat
        noir = ImageStat.Stat(Image.open(ICI / "archive" / f"{n:03d}.png").convert("L")).mean[0] < 3
    except Exception:
        noir = False
    try:                                                 # ecran identique a la verification precedente
        import hashlib
        ecran = hashlib.md5((ICI / "archive" / f"{n:03d}.png").read_bytes()).hexdigest()
    except Exception:
        ecran = None
    meme_ecran = ecran is not None and ecran == dernier_ecran
    dernier_ecran = ecran
    # redemarrage a chaud reste coince dans le BIOS (segment ffff/f000 hors POST) : meme traitement
    fige = (cs, eip) == dernier and (cs, eip) != ("0108", 0x6a2a)   # meme instruction (hors attente normale)
    dernier = (cs, eip)
    # BIOS ou meme EIP : blocage seulement si l'ecran est fige aussi (repos APM = faux positif)
    if meme_ecran and ((cs == "0028" and 0xc0053479 <= eip <= 0xc0053510) or fige or cs in ("ffff", "f000")):
        bloque += 1
        log(f"{n:03d} bloque ? ({bloque}) ecran fige{' (noir)' if noir else ''} EIP={cs}:{eip:08x}")
        if bloque >= 3:
            log("QEMU arrete, relance a froid")
            qemu.kill()
            qemu.wait()
            bloque = 0
            continue
    else:
        bloque = 0
        log(f"{n:03d} EIP={cs}:{eip:08x}")
    for _ in range(12):                                  # 2 min, en suivant QEMU
        if qemu.poll() is not None or (ICI / "STOP").exists():
            break
        time.sleep(10)
if qemu and qemu.poll() is None:
    qemu.kill()
log("fin")
