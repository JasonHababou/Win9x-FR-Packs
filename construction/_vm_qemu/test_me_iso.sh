#!/bin/sh
# Test de l'ISO WinMe_FR sur un disque vierge (me_iso2.img, port 4448), sequence relevee
# le 27/10/2026 : menu du CD -> FDISK, redemarrage, FORMAT, pages de Setup (Entree),
# copie (Hyper-V), puis me_iso_relance.sh (tcg) pour les demarrages suivants.
# Les pages Utilisateur / Licence / Cle / Terminer et l'ouverture de session restent a
# valider a la main (QEMU_PORT=4448 python pilote.py ...). Captures : mi_<etape>.png
# Usage : test_me_iso.sh <iso>
cd "$(dirname "$0")"
I=$1
export QEMU_PORT=4448
w(){ python -c "import time; time.sleep($1)"; }
k(){ python pilote.py touches "$@" > /dev/null; }
t(){ python pilote.py texte "$1" > /dev/null; }
e(){ python pilote.py ecran "mi_$1.png" > /dev/null 2>&1; }
cd_me(){ "/c/Program Files/qemu/qemu-system-x86_64.exe" -machine pc -accel whpx -m 512 \
  -drive file=me_iso2.img,format=raw,if=ide,index=0 \
  -drive file="$I",media=cdrom,if=ide,index=2,readonly=on -boot d -no-reboot \
  -vga cirrus -audiodev none,id=muet -device sb16,audiodev=muet -nic none -rtc base=localtime \
  -display none -monitor tcp:127.0.0.1:4448,server,nowait > qemu_meiso.log 2>&1; }
rm -f me_iso2.img STOP_MEISO
"/c/Program Files/qemu/qemu-img.exe" create -f raw me_iso2.img 8G > /dev/null
echo "$(date +%H:%M:%S) test ISO ME : $I" >> me_relance.log
cd_me & w 75; e a1; t p; w 8; k ret; w 5; k ret; w 5; k ret; w 10; k ret; w 15; e a2
k esc; w 5; python pilote.py cmd quit > /dev/null 2>&1; w 5
cd_me & w 90; e b1; t f; w 4; t o; k ret; w 60; k ret; w 60; e b2; k ret; w 90; e b3
t q; w 90; e c0
for i in 1 2 3 4 5 6 7 8 9; do k ret; w 12; e c$i; done
echo "$(date +%H:%M:%S) copie de Setup lancee" >> me_relance.log
sh me_iso_relance.sh "$I"
