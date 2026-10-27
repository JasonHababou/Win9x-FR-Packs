#!/bin/sh
# Test complet d'une ISO Win98FR dans QEMU (sequence validee sur test11, 2026-10-20) :
# partition (Hyper-V), pages de Setup, copie, DRVWQ117 renomme, puis surveiller.py.
# Usage : test_iso_complet.sh <iso> <prefixe captures>
cd "$(dirname "$0")"
I=$1; P=$2
w(){ python -c "import time; time.sleep($1)"; }
k(){ python pilote.py touches "$@"; }
e(){ python pilote.py ecran "${P}_$1.png" >/dev/null 2>&1; }
"/c/Program Files/qemu/qemu-img.exe" create -f raw win98.img 8G >/dev/null
echo "=== $I : test complet, 1 Go, hybride ===" >> surveiller.log
./phase_whpx.sh $I d 1024 & w 10; k ret; w 35; k ret; w 6; k ret; w 6; k down ret; w 8; k ret; w 10
while tasklist | grep -qi qemu-system-x86_64; do sleep 5; done
./phase_whpx.sh $I d 1024 & w 10; k ret; w 240; e a1; k ret; w 60; e a2
k ret; w 20; k ret; w 15; k ret; w 15; e a3
python pilote.py texte 'Test'; k ret; w 15; e a4; k ret; w 8
for i in 1 2 3 4 5; do k ret; w 15; done; e a5
while tasklist | grep -qi qemu-system-x86_64; do sleep 10; done
echo "$(date +%H:%M:%S) copie terminee (Hyper-V)" >> surveiller.log
./phase_cd.sh $I 1024 & sleep 12; k 2 ret; sleep 40
python - <<'PY'
import subprocess
m = {" ": "spc", ":": "shift-semicolon", "\\": "backslash", ".": "dot"}
cmd = r"ren c:\windows\system\iosubsys\drvwq117.vxd drvwq117.old"
subprocess.run(["python", "pilote.py", "touches"] + [m.get(c, c) for c in cmd] + ["ret"])
PY
sleep 5; python pilote.py cmd quit; sleep 3
echo "$(date +%H:%M:%S) DRVWQ117 renomme" >> surveiller.log
python surveiller.py $I 1024
